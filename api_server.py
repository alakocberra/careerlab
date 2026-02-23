#!/usr/bin/env python3
"""Career dashboard static + API server (no external dependency)."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
from urllib import request, error

HOST = "0.0.0.0"
PORT = 8000
STATE_FILE = Path("dashboard_state.json")


class Handler(SimpleHTTPRequestHandler):
    def _json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/health":
            self._json(200, {"ok": True})
            return
        if self.path == "/api/state":
            if STATE_FILE.exists():
                try:
                    data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    data = {}
            else:
                data = {}
            self._json(200, data)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/coach":
            self.handle_coach()
            return

        if self.path != "/api/state":
            self._json(404, {"error": "not_found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._json(400, {"error": "invalid_content_length"})
            return

        try:
            raw = self.rfile.read(content_length)
            payload = json.loads(raw.decode("utf-8") if raw else "{}")
            if not isinstance(payload, dict):
                raise ValueError("payload must be object")
        except (json.JSONDecodeError, ValueError) as exc:
            self._json(400, {"error": "invalid_json", "detail": str(exc)})
            return

        STATE_FILE.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self._json(200, {"ok": True})

    def handle_coach(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self._json(
                400,
                {
                    "error": "missing_openai_api_key",
                    "detail": "OPENAI_API_KEY ortam değişkeni ayarlı değil.",
                },
            )
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(content_length)
            payload = json.loads(raw.decode("utf-8") if raw else "{}")
            state = payload.get("state", {}) if isinstance(payload, dict) else {}
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "invalid_json"})
            return

        prompt = (
            "Aşağıdaki career dashboard durumuna göre Türkçe, kısa ve uygulanabilir "
            "3 öneri üret. Her öneride bir sonraki adım net olsun. Durum: "
            f"{json.dumps(state, ensure_ascii=False)}"
        )

        body = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a practical career coach."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.5,
        }

        req = request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=30) as resp:
                response_payload = json.loads(resp.read().decode("utf-8"))
                text = (
                    response_payload.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "Öneri üretilemedi.")
                )
                self._json(200, {"ok": True, "advice": text})
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            self._json(502, {"error": "openai_http_error", "detail": detail[:400]})
        except error.URLError:
            self._json(502, {"error": "openai_connection_error"})


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serving dashboard at http://localhost:{PORT}/dashboard.html")
    print(f"API health: http://localhost:{PORT}/api/health")
    print(f"API state:  http://localhost:{PORT}/api/state")
    server.serve_forever()
