# Travel Planning Agent

A Travel Planning Agent that finds the **cheapest flight + hotel combinations** using SerpAPI.

## Overview

The Travel Planning Agent is an AI-powered travel assistant that:
- Accepts trip requests (origin, destination, date range)
- Fetches flight and hotel data from **SerpAPI**
- Finds the **cheapest flight + hotel** combination
- Enforces timing constraints: **hotel check-in ≥ flight arrival + configurable gap**

### Architecture

```
┌─────────────────────┐
│   Travel Agent UI   │
│   (React Frontend)  │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│  Travel Supervisor  │
│   (LangGraph)       │
│                     │
│  ┌───────────────┐  │
│  │ Parse Intent  │  │
│  └───────┬───────┘  │
│          ▼          │
│  ┌───────────────┐  │
│  │ Search Flights│──┼──► SerpAPI (Google Flights)
│  └───────┬───────┘  │
│          ▼          │
│  ┌───────────────┐  │
│  │ Search Hotels │──┼──► SerpAPI (Google Hotels)
│  └───────┬───────┘  │
│          ▼          │
│  ┌───────────────┐  │
│  │ Find Best Plan│  │
│  └───────────────┘  │
└─────────────────────┘
```

---

## Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Notes |
|-------------|---------|-------|
| **Python** | 3.13+ | Required for the backend agents |
| **Node.js** | 16.14+ | Required for the frontend UI |
| **Docker** | Latest | Required for containerized setup |
| **Docker Compose** | v2+ | Comes with Docker Desktop |
| **uv** | Latest | Python package manager ([install](https://docs.astral.sh/uv/getting-started/installation/)) |

### API Keys Required

You'll need to obtain the following API keys:

| Service | Purpose | Get Key |
|---------|---------|---------|
| **SerpAPI** | Flight & hotel search | [serpapi.com](https://serpapi.com/) |
| **LLM Provider** | AI language model | See [Supported LLM Providers](#supported-llm-providers) |

---

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone [<repository-url>](https://github.com/AdityaJadhav17/sandhacks-2026-project)
cd sandhacks-2026-project
```

### Step 2: Create Your Environment File

The project uses a `.env` file to store your API keys and configuration. A template file `.env.example` is provided for you.

**Copy the contents of the example file to create your own `.env` file and then add your own API keys. **


### Step 3: Configure Your Environment Variables

Open the `.env` file in your favorite text editor and add your API keys and configuration:

```env
# =============================================================================
# LLM CONFIGURATION (Required)
# =============================================================================
# Choose your LLM provider and model. Uses LiteLLM format: "provider/model-name"
# 
# Examples:
#   - OpenAI:     LLM_MODEL="openai/gpt-4" or "openai/gpt-4o" or "openai/gpt-3.5-turbo"
#   - Azure:      LLM_MODEL="azure/your-deployment-name"
#   - Anthropic:  LLM_MODEL="anthropic/claude-3-opus-20240229"
#   - GROQ:       LLM_MODEL="groq/llama3-70b-8192"
#   - NVIDIA NIM: LLM_MODEL="nvidia_nim/meta/llama3-70b-instruct"
#
LLM_MODEL="openai/gpt-4"

# Provider-specific API keys (add the one for your chosen provider)
OPENAI_API_KEY=your_openai_api_key_here
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# GROQ_API_KEY=your_groq_api_key_here
# AZURE_API_KEY=your_azure_api_key_here
# AZURE_API_BASE=your_azure_endpoint_here
# AZURE_API_VERSION=your_azure_api_version_here

# =============================================================================
# SERPAPI CONFIGURATION (Required for travel searches)
# =============================================================================
# Get your API key at: https://serpapi.com/
SERPAPI_API_KEY=your_serpapi_api_key_here

# =============================================================================
# TRAVEL AGENT SETTINGS (Optional)
# =============================================================================
# Minimum hours between flight arrival and hotel check-in
# This buffer accounts for: immigration, customs, baggage claim, airport-to-hotel travel
# Default: 2 hours
TRAVEL_HOTEL_CHECKIN_GAP_HOURS=2

# =============================================================================
# TRANSPORT CONFIGURATION (Optional - defaults work for most setups)
# =============================================================================
# Message transport protocol: NATS (default) or SLIM
DEFAULT_MESSAGE_TRANSPORT=NATS

# Transport server URL
# For Docker: nats://nats:4222
# For local:  nats://localhost:4222
TRANSPORT_SERVER_ENDPOINT=nats://localhost:4222

# =============================================================================
# LOGGING (Optional)
# =============================================================================
# Log level: DEBUG, INFO, WARNING, ERROR
LOGGING_LEVEL=INFO
```

**⚠️ Important Security Notes:**
- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them periodically
- The `.env` file is already in `.gitignore` by default

### Step 4: Install Dependencies

**Install Python dependencies using uv:**

```bash
uv sync
```

**Install frontend dependencies:**

```bash
cd frontend
npm install
cd ..
```

---

## Running the Application

### Option 1: Docker Compose (Recommended)

This is the easiest way to run the entire application stack with all services.

**Start all services:**

```bash
docker compose up
```

**Start in detached mode (background):**

```bash
docker compose up -d
```

**View logs:**

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f travel-supervisor
```

**Stop all services:**

```bash
docker compose down
```

**Access the application:**

| Service | URL | Description |
|---------|-----|-------------|
| **UI** | http://localhost:3000 | Web interface |
| **API** | http://localhost:8000 | Travel supervisor API |
| **Grafana** | http://localhost:3001 | Observability dashboard |
| **Flight Agent** | http://localhost:9001 | Flight search A2A agent |
| **Hotel Agent** | http://localhost:9002 | Hotel search A2A agent |
| **Activity Agent** | http://localhost:9003 | Activity search A2A agent |

### Option 2: Local Development

For development purposes, you may want to run services individually.

**Terminal 1 - Start infrastructure services:**

```bash
docker compose up nats clickhouse-server otel-collector grafana
```

**Terminal 2 - Set PYTHONPATH and start the travel supervisor:**

```bash
# On Linux/macOS
export PYTHONPATH=$(pwd)
uv run python agents/supervisors/travel/main.py

# On Windows (PowerShell)
$env:PYTHONPATH = (Get-Location).Path
uv run python agents/supervisors/travel/main.py
```

**Terminal 3 - Start the frontend:**

```bash
cd frontend
npm run dev
```

---

## Usage

### Web Interface

1. Open http://localhost:3000 in your browser
2. Type your travel query in the chat interface
3. The agent will search for flights, hotels, and provide the best options

### API Endpoints

**Search for travel deals:**

```bash
curl -X POST http://localhost:8000/agent/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Find me the cheapest flight and hotel from LAX to Tokyo, January 15-22, 2026"
  }'
```

**Streaming search (real-time updates):**

```bash
curl -X POST http://localhost:8000/agent/prompt/stream \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Find travel options from NYC to Paris, February 1-10, 2026"
  }'
```

### Example Prompts

| Query Type | Example |
|------------|---------|
| Basic search | "Find me flights from LAX to Tokyo, March 12-15th, 2026" |
| Best deal | "What's the cheapest trip from NYC to Paris in March?" |
| Specific dates | "I need a trip from San Francisco to London, March 5-12" |

### Response Example

```
🎉 Best Travel Plan Found!

💰 Total Cost: $1,234.56

✈️ Flight Details:
- Airline: Japan Airlines
- Price: $850.00
- Departure: 2026-01-15 10:30
- Arrival: 2026-01-15 15:45
- Stops: 0 (Non-stop)

🏨 Hotel Details:
- Name: Tokyo Bay Hotel
- Price: $384.56
- Rating: ⭐⭐⭐⭐
- Check-in: 15:00

📋 Trip Summary:
- Route: LAX → NRT
- Dates: 2026-01-15 to 2026-01-22
- Buffer to Hotel: 2 hours
```

---

## Configuration Reference

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LLM_MODEL` | Language model in litellm format (e.g., `openai/gpt-4`) | ✅ Yes | - |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI models) | Depends on LLM | - |
| `ANTHROPIC_API_KEY` | Anthropic API key (if using Claude models) | Depends on LLM | - |
| `GROQ_API_KEY` | GROQ API key (if using GROQ models) | Depends on LLM | - |
| `AZURE_API_KEY` | Azure OpenAI API key | Depends on LLM | - |
| `AZURE_API_BASE` | Azure OpenAI endpoint URL | Depends on LLM | - |
| `AZURE_API_VERSION` | Azure OpenAI API version | Depends on LLM | - |
| `SERPAPI_API_KEY` | SerpAPI key for flight/hotel searches | ✅ Yes | - |
| `TRAVEL_HOTEL_CHECKIN_GAP_HOURS` | Hours between flight arrival and hotel check-in | No | `2` |
| `DEFAULT_MESSAGE_TRANSPORT` | Transport protocol (`NATS` or `SLIM`) | No | `NATS` |
| `TRANSPORT_SERVER_ENDPOINT` | Transport server URL | No | `nats://localhost:4222` |
| `LOGGING_LEVEL` | Log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | No | `INFO` |
| `ENABLE_HTTP` | Enable HTTP server | No | `true` |

### Advanced Configuration (Optional)

**LiteLLM Proxy (for centralized LLM management):**

```env
LITELLM_PROXY_BASE_URL=http://your-litellm-proxy:4000
LITELLM_PROXY_API_KEY=your_proxy_api_key
```

**OAuth2 OpenAI Provider (for enterprise deployments):**

```env
OAUTH2_CLIENT_ID=your_client_id
OAUTH2_CLIENT_SECRET=your_client_secret
OAUTH2_TOKEN_URL=https://your-oauth-provider/token
OAUTH2_BASE_URL=https://your-openai-endpoint
OAUTH2_APPKEY=your_app_key
```

### Timing Constraint

The agent enforces a minimum gap between flight arrival and hotel check-in to account for:
- Immigration/customs processing
- Baggage claim
- Airport-to-hotel travel time

Default is 2 hours. Adjust via `TRAVEL_HOTEL_CHECKIN_GAP_HOURS`.

---

## Supported LLM Providers

The travel agent uses [LiteLLM](https://docs.litellm.ai/docs/providers) for LLM provider abstraction, supporting 100+ providers:

| Provider | Model Format | Required Env Var |
|----------|--------------|------------------|
| **OpenAI** | `openai/gpt-4`, `openai/gpt-4o`, `openai/gpt-3.5-turbo` | `OPENAI_API_KEY` |
| **Azure OpenAI** | `azure/your-deployment-name` | `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION` |
| **Anthropic** | `anthropic/claude-3-opus-20240229`, `anthropic/claude-3-sonnet-20240229` | `ANTHROPIC_API_KEY` |
| **GROQ** | `groq/llama3-70b-8192`, `groq/mixtral-8x7b-32768` | `GROQ_API_KEY` |
| **NVIDIA NIM** | `nvidia_nim/meta/llama3-70b-instruct` | `NVIDIA_NIM_API_KEY` |
| **Google** | `gemini/gemini-pro` | `GOOGLE_API_KEY` |
| **Mistral** | `mistral/mistral-large-latest` | `MISTRAL_API_KEY` |

For a complete list of supported providers and models, see the [LiteLLM documentation](https://docs.litellm.ai/docs/providers).

---

## Project Structure

```
sandhacks-2026-project/
├── agents/
│   ├── activity/              # Activity search A2A agent
│   │   ├── agent.py
│   │   ├── agent_executor.py
│   │   ├── card.py
│   │   └── server.py
│   ├── flight/                # Flight search A2A agent
│   │   ├── agent.py
│   │   ├── agent_executor.py
│   │   ├── card.py
│   │   └── server.py
│   ├── hotel/                 # Hotel search A2A agent
│   │   ├── agent.py
│   │   ├── agent_executor.py
│   │   ├── card.py
│   │   └── server.py
│   ├── supervisors/
│   │   └── travel/            # Travel supervisor (main coordinator)
│   │       ├── main.py        # FastAPI server
│   │       ├── suggested_prompts.json
│   │       └── graph/
│   │           ├── graph.py   # LangGraph workflow
│   │           ├── models.py  # Pydantic models
│   │           ├── tools.py   # LangGraph tools
│   │           └── shared.py  # Shared state
│   └── travel/
│       ├── serpapi_tools.py   # SerpAPI flight/hotel/activity search
│       └── travel_logic.py    # Timing constraints & best plan logic
├── common/
│   ├── llm.py                 # LLM configuration
│   └── version.py             # Version info
├── config/
│   └── config.py              # Environment configuration loader
├── frontend/                  # React UI
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── docker/
│   ├── Dockerfile.activity-agent
│   ├── Dockerfile.flight-agent
│   ├── Dockerfile.hotel-agent
│   ├── Dockerfile.travel-supervisor
│   └── Dockerfile.ui
├── docker-compose.yaml
├── .env.example               # Environment template (copy to .env)
├── pyproject.toml             # Python dependencies
└── Makefile                   # Development commands
```

---

## Observability

### Grafana Dashboard

Access Grafana at http://localhost:3001 to view:
- Request traces
- Agent execution flows
- Performance metrics

**Default credentials:**
- Username: `admin`
- Password: `admin`

### Tracing

The agent uses OpenTelemetry for distributed tracing. Traces are collected by the OTEL collector and stored in ClickHouse.

---

## Troubleshooting

### Common Issues

**1. "SerpAPI key is not configured" error**

Make sure your `.env` file contains a valid `SERPAPI_API_KEY`:

```bash
# Verify the variable is set
cat .env | grep SERPAPI
```

**2. "LLM_MODEL is not set" error**

Ensure you've set both `LLM_MODEL` and the corresponding API key:

```env
LLM_MODEL="openai/gpt-4"
OPENAI_API_KEY=sk-...
```

**3. Docker containers not starting**

```bash
# Check Docker is running
docker ps

# Rebuild containers
docker compose build --no-cache
docker compose up
```

**4. Port already in use**

```bash
# Check what's using the port (e.g., 8000)
# Linux/macOS
lsof -i :8000

# Windows
netstat -ano | findstr :8000
```

**5. Frontend can't connect to backend**

If running locally without Docker, make sure `VITE_EXCHANGE_APP_API_URL` in the frontend points to the correct backend URL.

---

## Development

### Running Tests

```bash
uv run pytest tests/
```

### Linting

```bash
# Python
uv run ruff check .

# Frontend
cd frontend
npm run lint
```

### Formatting

```bash
# Frontend
cd frontend
npm run format
```

---

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.
