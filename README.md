# 🧰 Multi-Tool AI Assistant

An end-to-end, tool-calling AI assistant built with LangGraph's ReAct agent architecture, capable of dynamically invoking web search, safe calculation, real-time weather, and date/time tools to answer user prompts — with a Streamlit interface and Groq-hosted LLM inference.

Kullanıcı promptlarına göre gerektiğinde web araması, güvenli hesaplama, gerçek zamanlı hava durumu ve tarih/saat tool'larını dinamik olarak çağırabilen; LangGraph ReAct agent mimarisi, Streamlit arayüzü ve Groq üzerinden çalışan LLM inference kullanan uçtan uca bir tool-calling yapay zeka asistanıdır.

## 🇬🇧 English

### 📌 Overview

Multi-Tool AI Assistant is an agentic chatbot that answers natural-language questions and autonomously decides when to reach for external tools to ground its answers in real, up-to-date data instead of relying solely on model memory.

The application follows a ReAct (Reason + Act) agent workflow. A user prompt is passed to an LLM-driven orchestrator, which reasons about whether the request requires external data. When it does, the orchestrator invokes the relevant tool (web search, calculator, weather, or current date/time), incorporates the tool's output into its reasoning, and produces a final, human-readable answer.

The application provides a single Streamlit-based interface with per-session conversational memory and visible tool-usage tracing.

**Main capabilities**
- Natural-language chat with an LLM-driven agent
- Autonomous tool selection (ReAct pattern)
- Real-time web search (no API key required)
- Safe, sandboxed mathematical calculation (AST-based, no `eval`/`exec`)
- Real-time weather data via a dedicated geocoding + forecast tool
- Current date/time awareness
- Per-session conversational memory
- Transparent tool-call inspection in the UI

### 🏗️ Architecture

```
                     ┌─────────────────────┐
                     │    Streamlit UI     │
                     └──────────┬──────────┘
                                │ user prompt
                                ▼
                     ┌─────────────────────┐
                     │    Orchestrator     │
                     │ (LangGraph ReAct     │
                     │  Agent)              │
                     └──────────┬──────────┘
                                │
                     reasons about tool need
                                │
                 ┌──────────────┼──────────────┬───────────────┐
                 ▼              ▼              ▼               ▼
          ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────────┐
          │ web_search │ │ calculator │ │  weather   │ │ current_datetime │
          └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └────────┬────────┘
                 │              │              │                │
                 └──────────────┴──────────────┴────────────────┘
                                │ tool output
                                ▼
                     ┌─────────────────────┐
                     │   Groq LLM (Chat)   │
                     └──────────┬──────────┘
                                │
                                ▼
                          Final Answer
```

### 🔄 Agent Workflow

The request-handling workflow consists of the following stages:

1. **Prompt Intake**
   The user's message is captured through the Streamlit chat input and appended to the session's conversation history.

2. **Reasoning (ReAct loop)**
   The orchestrator, built with LangGraph's `create_react_agent`, sends the conversation to the LLM together with a system prompt that defines when tool use is required (e.g. any numeric calculation, any weather query, any information beyond the model's knowledge).

3. **Tool Invocation**
   If the LLM determines a tool is needed, it emits a structured tool call. LangGraph routes the call to the corresponding tool implementation.

4. **Tool Execution**
   - `web_search` queries a free, key-less search backend and returns summarized results with sources.
   - `calculator` parses the expression into an AST and evaluates it using only an explicit allow-list of operators/functions — `eval`/`exec` are never used.
   - `weather` resolves a city name to coordinates and fetches live conditions from a free weather API.
   - `current_datetime` returns the current UTC date and time.

5. **History Trimming**
   Before each LLM call, the conversation history is trimmed to a token budget via a `pre_model_hook`, keeping the assistant within the LLM provider's rate limits without discarding the underlying stored memory.

6. **Response Synthesis**
   The LLM incorporates the tool output into a final, natural-language answer, which is streamed back to the Streamlit UI along with a visible trace of which tools were used.

### ✨ Key Features

- 🤖 LLM-driven autonomous tool selection (ReAct pattern)
- 🔎 Free, key-less web search integration
- 🧮 Sandboxed, `eval`-free calculator tool
- 🌤️ Real-time weather via geocoding + forecast API
- 🕒 Current date/time awareness
- 🧠 Per-session conversational memory (LangGraph checkpointing)
- 🎨 Custom-styled Streamlit interface (typography, color palette, iconography)
- 🧱 Modular, production-oriented project structure
- 🪵 Centralized logging with rotating file output
- ✅ Unit-tested tool logic (pytest)

### 🗂️ Project Structure

```
Multi-Tool-AI-Assistant/
│
├── app.py                          // Streamlit application entry point
│
├── config/
│   └── settings.py                 // Centralized, type-safe environment configuration
│
├── src/
│   ├── agents/
│   │   ├── orchestrator.py         // LangGraph ReAct agent construction & execution
│   │   └── tools/
│   │       ├── web_search_tool.py  // Free web search tool
│   │       ├── calculator_tool.py  // AST-based safe calculator tool
│   │       ├── weather_tool.py     // Real-time weather tool
│   │       └── datetime_tool.py    // Current date/time tool
│   │
│   ├── core/
│   │   ├── llm_client.py           // Groq LLM client factory
│   │   ├── memory.py               // LangGraph checkpointer wrapper
│   │   └── logger.py               // Centralized loguru-based logging
│   │
│   ├── models/
│   │   └── schemas.py              // Pydantic data schemas
│   │
│   ├── ui/
│   │   ├── components.py           // Streamlit UI components
│   │   └── styles.py                // Custom CSS (fonts, colors, icons)
│   │
│   └── utils/
│       ├── exceptions.py           // Custom exception hierarchy
│       └── retry.py                // Retry/backoff decorator
│
├── tests/
│   ├── test_tools.py
│   └── test_schemas.py
│
├── .streamlit/
│   └── config.toml                 // Streamlit theme configuration
│
├── requirements.txt
├── .env.example
└── README.md
```

### 🛠️ Technology Stack

**Orchestration / Agentic AI**
- LangGraph (`create_react_agent`, `MemorySaver` checkpointing)
- LangChain Core (tool definitions, message types)

**LLM Provider**
- Groq API (free tier), `openai/gpt-oss-120b`

**Tools**
- DDGS (free, key-less web search)
- Open-Meteo API (free, key-less weather + geocoding)
- Python `ast` module (sandboxed calculator, no `eval`/`exec`)

**Backend / Configuration**
- Python
- Pydantic & Pydantic Settings
- python-dotenv
- Loguru (structured logging)
- Tenacity (retry/backoff)

**Frontend**
- Streamlit (custom theme, typography, iconography)

**Testing**
- Pytest

### 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sena-cetinkaya/Multi-Tool-AI-Assistant.git
   cd Multi-Tool-AI-Assistant
   ```

2. **Create a virtual environment**

   Windows
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Linux / macOS
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### ⚙️ Configuration

Application configuration is managed through a `.env` file at the project root (see `.env.example`).

```
GROQ_API_KEY=your_groq_api_key_here
APP_ENV=development
LOG_LEVEL=INFO
LLM_MODEL=openai/gpt-oss-120b
LLM_TEMPERATURE=0.3
MAX_AGENT_ITERATIONS=10
```

Before running the application, obtain a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys) and set `GROQ_API_KEY`.

### ▶️ Running the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

### 💡 Example Workflow

1. Start the Streamlit application.
2. Ask a question requiring no external data (e.g. a general knowledge question) → the agent answers directly, no tool is invoked.
3. Ask a question requiring current information (e.g. "What is OpenAI's latest released model?") → the agent invokes `web_search` and grounds its answer in retrieved sources.
4. Ask a numeric question (e.g. "What is 847 * 392?") → the agent invokes `calculator` and returns a verified result.
5. Ask about current conditions in a city → the agent invokes `weather` and returns live temperature, humidity, and wind data.
6. Inspect which tools were used for any given answer directly in the chat UI.

### 🧠 Design Decisions

**ReAct Agent via LangGraph**
The application uses LangGraph's prebuilt `create_react_agent`, which implements the Reason + Act loop natively, rather than hand-rolling a custom control loop. This keeps the orchestration logic minimal while remaining fully inspectable and extensible.

**Sandboxed Calculator**
Mathematical evaluation is implemented via Python's `ast` module with an explicit allow-list of operators and functions, rather than `eval`/`exec`, to eliminate arbitrary code execution risk from user or model input.

**Provider-Agnostic LLM Client**
LLM access is isolated inside a single factory module (`llm_client.py`), so the underlying provider (currently Groq) can be swapped — including for a fully local model via Ollama — without touching orchestration or tool code.

**Token-Budget History Trimming**
A `pre_model_hook` trims the conversation history sent to the LLM on every turn, keeping requests within the LLM provider's rate limits without discarding the full history held by the checkpointer.

**Modular Architecture**
Configuration, LLM access, agent orchestration, tools, data schemas, and UI are separated into dedicated modules, making the application easier to understand, test, and extend with additional tools.

### ⚠️ Current Limitations

The current implementation is a portfolio-oriented agentic AI application and has several areas that could be improved for production use:

- No automated tool-call evaluation or agent-quality benchmarking
- No dedicated authentication or authorization layer
- No streaming token-by-token LLM responses in the UI
- Web search results are not independently source-verified beyond prompt-level instructions
- Conversational memory is in-process only (not persisted across application restarts)
- Limited automated test coverage (tool logic only)
- Single-provider LLM configuration (Groq)
- No containerized deployment configuration

### 🔮 Future Improvements

- Automated agent evaluation and tool-call quality metrics
- Source verification layer for web search citations
- Streaming LLM responses in the Streamlit UI
- Persistent (database-backed) conversational memory
- Additional tools (e.g. RAG-based document Q&A, code execution)
- Multi-provider LLM configuration (Groq, OpenAI, local Ollama)
- Authentication and authorization
- Expanded automated test suite (agent and integration tests)
- Structured logging and monitoring
- Docker-based deployment

### 📄 License

This project is licensed under the MIT License.

### 👩‍💻 Author

**Sena Çetinkaya**

Computer Engineer focused on AI Engineering, LLM applications, RAG systems, Agentic AI, and Machine Learning.

GitHub: https://github.com/sena-cetinkaya

LinkedIn: [https://www.linkedin.com/in/sena-çetinkaya-a6493717a/]

---

## 🇹🇷 Türkçe

### 📌 Genel Bakış

Multi-Tool AI Assistant, doğal dilde sorulan sorulara cevap veren ve verdiği cevapları yalnızca model belleğine değil, gerektiğinde gerçek ve güncel verilere dayandırmak için hangi tool'u ne zaman kullanacağına kendi başına karar veren agentic (ajan tabanlı) bir chatbot'tur.

Uygulama, ReAct (Reason + Act / Akıl Yürüt + Eylem Yap) agent iş akışını izler. Kullanıcı promptu, LLM tabanlı bir orchestrator'a iletilir; orchestrator, isteğin harici veriye ihtiyaç duyup duymadığını değerlendirir. İhtiyaç varsa ilgili tool'u (web arama, hesap makinesi, hava durumu veya güncel tarih/saat) çağırır, tool çıktısını akıl yürütme sürecine dahil eder ve son, insan tarafından okunabilir bir cevap üretir.

Uygulama; oturum bazlı konuşma hafızası ve şeffaf tool kullanım izlenebilirliği sunan, tek bir Streamlit tabanlı arayüz üzerinden çalışmaktadır.

**Temel yetenekler**
- LLM tabanlı agent ile doğal dilde sohbet
- Otonom tool seçimi (ReAct pattern)
- Gerçek zamanlı web araması (API key gerektirmez)
- Güvenli, sandbox'lanmış matematiksel hesaplama (AST tabanlı, `eval`/`exec` kullanılmaz)
- Geocoding + forecast tool'u üzerinden gerçek zamanlı hava durumu
- Güncel tarih/saat farkındalığı
- Oturum bazlı konuşma hafızası
- Arayüzde şeffaf tool-çağrısı inceleme

### 🏗️ Mimari

```
                     ┌─────────────────────┐
                     │    Streamlit UI     │
                     └──────────┬──────────┘
                                │ kullanıcı promptu
                                ▼
                     ┌─────────────────────┐
                     │    Orchestrator     │
                     │ (LangGraph ReAct     │
                     │  Agent)              │
                     └──────────┬──────────┘
                                │
                    tool ihtiyacını değerlendirir
                                │
                 ┌──────────────┼──────────────┬───────────────┐
                 ▼              ▼              ▼               ▼
          ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌───────────────┐
          │ web_search │ │ calculator │ │  weather   │ │ current_datetime │
          └──────┬─────┘ └──────┬─────┘ └──────┬─────┘ └────────┬────────┘
                 │              │              │                │
                 └──────────────┴──────────────┴────────────────┘
                                │ tool çıktısı
                                ▼
                     ┌─────────────────────┐
                     │   Groq LLM (Chat)   │
                     └──────────┬──────────┘
                                │
                                ▼
                            Nihai Cevap
```

### 🔄 Agent İş Akışı

İstek işleme süreci aşağıdaki aşamalardan oluşmaktadır:

1. **Prompt Alımı**
   Kullanıcının mesajı Streamlit chat input üzerinden alınır ve oturumun konuşma geçmişine eklenir.

2. **Akıl Yürütme (ReAct döngüsü)**
   LangGraph'in `create_react_agent` fonksiyonuyla kurulan orchestrator, konuşmayı; tool kullanımının ne zaman gerekli olduğunu tanımlayan bir sistem promptuyla birlikte LLM'e gönderir (örn. her sayısal hesaplama, her hava durumu sorgusu, modelin bilgisini aşan her konu).

3. **Tool Çağrısı**
   LLM bir tool'a ihtiyaç olduğuna karar verirse, yapılandırılmış bir tool çağrısı üretir. LangGraph bu çağrıyı ilgili tool implementasyonuna yönlendirir.

4. **Tool Çalıştırma**
   - `web_search`, ücretsiz ve key gerektirmeyen bir arama motorunu sorgular, kaynaklarıyla birlikte özetlenmiş sonuçlar döner.
   - `calculator`, ifadeyi bir AST'ye (soyut sözdizimi ağacı) ayrıştırır ve yalnızca açıkça izin verilen operatör/fonksiyon listesiyle değerlendirir — `eval`/`exec` hiçbir zaman kullanılmaz.
   - `weather`, şehir adını koordinata çevirir ve ücretsiz bir hava durumu API'sinden anlık verileri çeker.
   - `current_datetime`, güncel UTC tarih ve saatini döner.

5. **Geçmiş Kırpma**
   Her LLM çağrısından önce, konuşma geçmişi bir `pre_model_hook` aracılığıyla token bütçesine göre kırpılır; bu sayede asistan, checkpointer'daki tam hafızayı silmeden LLM sağlayıcısının rate limit'leri içinde kalır.

6. **Cevap Sentezi**
   LLM, tool çıktısını nihai, doğal dilde bir cevaba dönüştürür; bu cevap, hangi tool'ların kullanıldığını gösteren görünür bir izle birlikte Streamlit arayüzüne aktarılır.

### ✨ Temel Özellikler

- 🤖 LLM tabanlı otonom tool seçimi (ReAct pattern)
- 🔎 Ücretsiz, key gerektirmeyen web arama entegrasyonu
- 🧮 Sandbox'lanmış, `eval` içermeyen hesap makinesi tool'u
- 🌤️ Geocoding + forecast API üzerinden gerçek zamanlı hava durumu
- 🕒 Güncel tarih/saat farkındalığı
- 🧠 Oturum bazlı konuşma hafızası (LangGraph checkpointing)
- 🎨 Özel tasarlanmış Streamlit arayüzü (tipografi, renk paleti, ikonografi)
- 🧱 Modüler, production odaklı proje yapısı
- 🪵 Dönen (rotating) dosya çıktılı merkezi loglama
- ✅ Birim testli tool mantığı (pytest)

### 🗂️ Proje Yapısı

```
Multi-Tool-AI-Assistant/
│
├── app.py                          // Streamlit uygulamasının giriş noktası
│
├── config/
│   └── settings.py                 // Tip güvenli, tek noktadan konfigürasyon
│
├── src/
│   ├── agents/
│   │   ├── orchestrator.py         // LangGraph ReAct agent kurulumu & çalıştırılması
│   │   └── tools/
│   │       ├── web_search_tool.py  // Ücretsiz web arama tool'u
│   │       ├── calculator_tool.py  // AST tabanlı güvenli hesap makinesi tool'u
│   │       ├── weather_tool.py     // Gerçek zamanlı hava durumu tool'u
│   │       └── datetime_tool.py    // Güncel tarih/saat tool'u
│   │
│   ├── core/
│   │   ├── llm_client.py           // Groq LLM istemci fabrikası
│   │   ├── memory.py               // LangGraph checkpointer sarmalayıcı
│   │   └── logger.py               // loguru tabanlı merkezi loglama
│   │
│   ├── models/
│   │   └── schemas.py              // Pydantic veri şemaları
│   │
│   ├── ui/
│   │   ├── components.py           // Streamlit arayüz bileşenleri
│   │   └── styles.py                // Özel CSS (font, renk, ikon)
│   │
│   └── utils/
│       ├── exceptions.py           // Özel hata hiyerarşisi
│       └── retry.py                // Retry/backoff decorator
│
├── tests/
│   ├── test_tools.py
│   └── test_schemas.py
│
├── .streamlit/
│   └── config.toml                 // Streamlit tema yapılandırması
│
├── requirements.txt
├── .env.example
└── README.md
```

### 🛠️ Teknoloji Stack'i

**Orkestrasyon / Agentic AI**
- LangGraph (`create_react_agent`, `MemorySaver` checkpointing)
- LangChain Core (tool tanımları, mesaj tipleri)

**LLM Sağlayıcı**
- Groq API (ücretsiz tier), `openai/gpt-oss-120b`

**Tool'lar**
- DDGS (ücretsiz, key gerektirmeyen web arama)
- Open-Meteo API (ücretsiz, key gerektirmeyen hava durumu + geocoding)
- Python `ast` modülü (sandbox'lanmış hesap makinesi, `eval`/`exec` yok)

**Backend / Konfigürasyon**
- Python
- Pydantic & Pydantic Settings
- python-dotenv
- Loguru (yapılandırılmış loglama)
- Tenacity (retry/backoff)

**Frontend**
- Streamlit (özel tema, tipografi, ikonografi)

**Test**
- Pytest

### 🚀 Kurulum

1. **Repository'yi klonlayın**
   ```bash
   git clone https://github.com/sena-cetinkaya/Multi-Tool-AI-Assistant.git
   cd Multi-Tool-AI-Assistant
   ```

2. **Virtual environment oluşturun**

   Windows
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Linux / macOS
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Gereksinimleri yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

### ⚙️ Yapılandırma

Uygulama yapılandırması, proje kökündeki bir `.env` dosyası üzerinden yönetilmektedir (bkz. `.env.example`).

```
GROQ_API_KEY=your_groq_api_key_here
APP_ENV=development
LOG_LEVEL=INFO
LLM_MODEL=openai/gpt-oss-120b
LLM_TEMPERATURE=0.3
MAX_AGENT_ITERATIONS=10
```

Uygulamayı çalıştırmadan önce [console.groq.com/keys](https://console.groq.com/keys) adresinden ücretsiz bir Groq API key alıp `GROQ_API_KEY` alanını doldurun.

### ▶️ Uygulamayı Çalıştırma

```bash
streamlit run app.py
```

Uygulama şu adreste çalışacaktır:

```
http://localhost:8501
```

### 💡 Örnek Kullanım Akışı

1. Streamlit uygulamasını başlatın.
2. Harici veri gerektirmeyen bir soru sorun (örn. genel bir bilgi sorusu) → agent doğrudan cevap verir, hiçbir tool çağrılmaz.
3. Güncel bilgi gerektiren bir soru sorun (örn. "OpenAI'nin en son yayınladığı model hangisi?") → agent `web_search` tool'unu çağırır ve cevabını getirdiği kaynaklara dayandırır.
4. Sayısal bir soru sorun (örn. "847 * 392 kaçtır?") → agent `calculator` tool'unu çağırır ve doğrulanmış bir sonuç döner.
5. Bir şehrin güncel hava durumunu sorun → agent `weather` tool'unu çağırır, anlık sıcaklık, nem ve rüzgar verisini döner.
6. Herhangi bir cevap için hangi tool'ların kullanıldığını doğrudan sohbet arayüzünden inceleyin.

### 🧠 Tasarım Kararları

**LangGraph ile ReAct Agent**
Uygulama, özel bir kontrol döngüsü elle yazmak yerine, Reason + Act döngüsünü native olarak uygulayan LangGraph'in hazır `create_react_agent` fonksiyonunu kullanır. Bu, orkestrasyon mantığını minimal tutarken tamamen incelenebilir ve genişletilebilir kalmasını sağlar.

**Sandbox'lanmış Hesap Makinesi**
Matematiksel değerlendirme, `eval`/`exec` yerine Python'ın `ast` modülü ile açıkça izin verilen operatör/fonksiyon listesi kullanılarak yapılır; bu, kullanıcı veya model girdisinden kaynaklanabilecek rastgele kod çalıştırma riskini ortadan kaldırır.

**Sağlayıcıdan Bağımsız LLM İstemcisi**
LLM erişimi tek bir fabrika modülünde (`llm_client.py`) izole edilmiştir; bu sayede mevcut sağlayıcı (Groq) — Ollama üzerinden tamamen yerel bir model dahil — orkestrasyon veya tool koduna dokunmadan değiştirilebilir.

**Token Bütçeli Geçmiş Kırpma**
Her turda LLM'e gönderilen konuşma geçmişi bir `pre_model_hook` ile kırpılır; bu, checkpointer'daki tam geçmişi silmeden istekleri LLM sağlayıcısının rate limit'leri içinde tutar.

**Modüler Mimari**
Konfigürasyon, LLM erişimi, agent orkestrasyonu, tool'lar, veri şemaları ve arayüz ayrı modüllere bölünmüştür; bu yapı, uygulamanın anlaşılmasını, test edilmesini ve ek tool'larla genişletilmesini kolaylaştırır.

### ⚠️ Mevcut Sınırlamalar

Mevcut uygulama portfolio odaklı bir agentic AI uygulamasıdır ve production ortamında kullanılmadan önce geliştirilebilecek çeşitli alanlara sahiptir:

- Otomatik tool-çağrısı değerlendirmesi veya agent kalite benchmark'ı bulunmamaktadır.
- Authentication / authorization katmanı bulunmamaktadır.
- Arayüzde token-token streaming LLM response desteği bulunmamaktadır.
- Web arama sonuçları, prompt seviyesindeki talimatların ötesinde bağımsız olarak kaynak doğrulamasından geçmemektedir.
- Konuşma hafızası yalnızca process içi (in-process) tutulur, uygulama yeniden başlatıldığında kalıcı değildir.
- Otomatik test kapsamı sınırlıdır (yalnızca tool mantığı).
- Tek sağlayıcılı LLM yapılandırması (Groq).
- Container tabanlı bir deployment yapılandırması bulunmamaktadır.

### 🔮 Gelecekte Yapılabilecek Geliştirmeler

- Otomatik agent değerlendirmesi ve tool-çağrısı kalite metrikleri
- Web arama kaynakları için doğrulama katmanı
- Streamlit arayüzünde streaming LLM response desteği
- Kalıcı (veritabanı destekli) konuşma hafızası
- Ek tool'lar (örn. RAG tabanlı doküman soru-cevap, kod çalıştırma)
- Çoklu sağlayıcı LLM yapılandırması (Groq, OpenAI, yerel Ollama)
- Authentication ve authorization
- Genişletilmiş otomatik test suite'i (agent ve entegrasyon testleri)
- Structured logging ve monitoring
- Docker tabanlı deployment

### 📄 Lisans

Bu proje MIT License altında lisanslanmıştır.

### 👩‍💻 Geliştirici

**Sena Çetinkaya**

Yapay Zeka Mühendisliği, LLM uygulamaları, RAG sistemleri, Agentic AI ve Machine Learning alanlarına odaklanan Bilgisayar Mühendisi.

GitHub: https://github.com/sena-cetinkaya

LinkedIn: [https://www.linkedin.com/in/sena-çetinkaya-a6493717a/]
