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

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16.14+ (for frontend)
- Docker (optional, for containerized setup)
- [SerpAPI API Key](https://serpapi.com/) - Required for flight/hotel searches

### Setup

1. **Clone and install dependencies**

```bash
# Install Python dependencies
uv sync

# Set PYTHONPATH
export PYTHONPATH=$(pwd)
```

2. **Configure environment**

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Required: LLM Provider (choose one)
LLM_MODEL="openai/gpt-4"
OPENAI_API_KEY=your_openai_api_key

# Required: SerpAPI for flight/hotel search
SERPAPI_API_KEY=your_serpapi_api_key

# Optional: Adjust timing gap between flight arrival and hotel check-in
TRAVEL_HOTEL_CHECKIN_GAP_HOURS=2
```

### Running the Agent

#### Option 1: Docker Compose (Recommended)

```bash
docker compose up
```

Access:
- **UI**: http://localhost:3000
- **API**: http://localhost:8000
- **Grafana**: http://localhost:3001

#### Option 2: Local Development

**Terminal 1 - Start infrastructure:**
```bash
docker compose up nats clickhouse-server otel-collector grafana
```

**Terminal 2 - Start travel supervisor:**
```bash
uv run python agents/supervisors/travel/main.py
```

**Terminal 3 - Start frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Usage

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
| Basic search | "Find me flights from LAX to Tokyo, Jan 15-22, 2026" |
| Best deal | "What's the cheapest trip from NYC to Paris next month?" |
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

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_MODEL` | Language model (e.g., `openai/gpt-4`) | Required |
| `SERPAPI_API_KEY` | SerpAPI key for searches | Required |
| `TRAVEL_HOTEL_CHECKIN_GAP_HOURS` | Hours between flight arrival and hotel check-in | `2` |
| `DEFAULT_MESSAGE_TRANSPORT` | Transport protocol (NATS/SLIM) | `NATS` |
| `TRANSPORT_SERVER_ENDPOINT` | Transport server URL | `nats://localhost:4222` |

### Timing Constraint

The agent enforces a minimum gap between flight arrival and hotel check-in to account for:
- Immigration/customs processing
- Baggage claim
- Airport-to-hotel travel time

Default is 2 hours. Adjust via `TRAVEL_HOTEL_CHECKIN_GAP_HOURS`.

## Project Structure

```
lungo/
├── agents/
│   ├── travel/                    # Travel module
│   │   ├── serpapi_tools.py       # SerpAPI flight/hotel search
│   │   └── travel_logic.py        # Timing constraints & best plan logic
│   └── supervisors/
│       └── travel/                # Travel supervisor
│           ├── main.py            # FastAPI server
│           ├── suggested_prompts.json
│           └── graph/
│               ├── graph.py       # LangGraph workflow
│               ├── models.py      # Pydantic models
│               ├── tools.py       # LangGraph tools
│               └── shared.py      # Shared state
├── config/
│   └── config.py                  # Configuration loader
├── frontend/                      # React UI
├── docker/
│   └── Dockerfile.travel-supervisor
├── docker-compose.yaml
└── .env.example
```

## Observability

### Grafana Dashboard

Access Grafana at http://localhost:3001 to view:
- Request traces
- Agent execution flows
- Performance metrics

### Tracing

The agent uses OpenTelemetry for distributed tracing. Traces are collected by the OTEL collector and stored in ClickHouse.

## Supported LLM Providers

The travel agent uses [litellm](https://docs.litellm.ai/docs/providers) for LLM integration:

- **OpenAI**: `LLM_MODEL="openai/gpt-4"`
- **Azure OpenAI**: `LLM_MODEL="azure/your-deployment"`
- **GROQ**: `LLM_MODEL="groq/llama3-70b-8192"`
- **NVIDIA NIM**: `LLM_MODEL="nvidia_nim/meta/llama3-70b-instruct"`

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.
