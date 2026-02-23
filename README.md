# careerlab

Bu repo artık doğrudan kullanabileceğin bir dashboard içerir ve **API ile veri kaydı** destekler.

## API ile Çalıştırma (önerilen)
1. Terminalde repo klasörüne gir:
   - `cd /workspace/careerlab`
2. Dashboard + API server'ı başlat:
   - `python api_server.py`
3. Tarayıcıdan aç:
   - `http://localhost:8000/dashboard.html`
4. API kontrolü:
   - `http://localhost:8000/api/health`
   - `http://localhost:8000/api/state`

> Dashboard'a girdiğin veriler `dashboard_state.json` dosyasına yazılır.

## Sadece statik çalıştırma (fallback)
- `python -m http.server 8000`
- `http://localhost:8000/dashboard.html`
- Bu modda veriler localStorage'da tutulur.

## Ne Göreceksin?
- 10 SMART hedef için canlı KPI tablosu (Güncel/Hedef/%).
- Toplam ilerleme yüzdesi.
- Haftalık snapshot (başvuru, SQL soru, networking).
- Sprint 1 görev checklist'i.
- Cuma review özeti (otomatik hesaplanır).

## Ek Doküman
- Sistem detayları: `career_comeback_system.md`
