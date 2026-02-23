# careerlab

Bu repo doğrudan kullanabileceğin bir dashboard içerir ve API ile veri kaydı + AI koç önerisi destekler.

## API ile Çalıştırma (önerilen)
1. Terminalde repo klasörüne gir:
   - `cd /workspace/careerlab`
2. OpenAI anahtarını ortam değişkeni olarak ayarla:
   - `export OPENAI_API_KEY='YOUR_KEY_HERE'`
3. Dashboard + API server'ı başlat:
   - `python api_server.py`
4. Tarayıcıdan aç:
   - `http://localhost:8000/dashboard.html`

## Endpointler
- `GET /api/health`
- `GET /api/state`
- `POST /api/state`
- `POST /api/coach` (dashboard durumuna göre AI aksiyon önerisi üretir)

> Dashboard'a girdiğin veriler `dashboard_state.json` dosyasına yazılır.

## Ne Göreceksin?
- 10 SMART hedef için canlı KPI tablosu.
- Toplam ilerleme yüzdesi.
- Haftalık snapshot + Cuma review.
- "AI Öneri Üret" butonu ile kişisel aksiyon önerisi.

## Ek Doküman
- Sistem detayları: `career_comeback_system.md`
