# Agentic Chatbot

Streamlit tabanlı, tool-calling destekli agentic chatbot. Kullanıcı promptuna
göre gerektiğinde **web arama**, **hesap makinesi** ve **tarih/saat** tool'ları
üzerinden veri çekip cevap üretir.

## Mimari

```
agentic_chatbot/
├── app.py                     # Streamlit giriş noktası
├── .env                        # Ortam değişkenleri (API key vb.)
├── config/
│   └── settings.py            # Tip güvenli, tek noktadan konfigürasyon
├── src/
│   ├── core/
│   │   ├── llm_client.py      # Groq LLM istemcisi (factory)
│   │   ├── memory.py          # LangGraph checkpointer sarmalayıcı
│   │   └── logger.py          # loguru tabanlı merkezi loglama
│   ├── agents/
│   │   ├── orchestrator.py    # LangGraph ReAct agent + hata yönetimi
│   │   └── tools/
│   │       ├── web_search_tool.py
│   │       ├── calculator_tool.py
│   │       └── datetime_tool.py
│   ├── models/
│   │   └── schemas.py         # Pydantic veri şemaları
│   ├── ui/
│   │   ├── components.py      # Streamlit bileşenleri
│   │   └── styles.py          # Özel CSS
│   └── utils/
│       ├── exceptions.py
│       └── retry.py
├── tests/
└── requirements.txt
```

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`.env` dosyasını açıp `GROQ_API_KEY` alanını doldurun (ücretsiz key için
https://console.groq.com/keys).

## Çalıştırma

```bash
streamlit run app.py
```

## Test

```bash
pytest
```

## Kullanılan Ücretsiz Kaynaklar

- **LLM**: Groq API (ücretsiz tier, `llama-3.3-70b-versatile`)
- **Web Arama**: DuckDuckGo Search (API key gerektirmez)
- **Orkestrasyon**: LangGraph `create_react_agent` (prebuilt ReAct döngüsü)
- **Hafıza**: LangGraph `MemorySaver` (in-memory checkpointer)

## Yeni Tool Ekleme

1. `src/agents/tools/` altına yeni bir modül ekleyin, `@tool` dekoratörü ile
   bir fonksiyon tanımlayın.
2. `src/agents/tools/__init__.py` içindeki `get_tools()` listesine ekleyin.

Orchestrator otomatik olarak yeni tool'u agent'a bağlar.
