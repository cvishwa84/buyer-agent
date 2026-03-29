# buyer-agent
AI-powered procurement buyer agent using LangChain and OpenAI

## Quickstart

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment

```bash
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env` if you plan to connect a real model later.  
Current MVP behavior is deterministic and does not require an API key.

### 3) Run the API

```bash
uvicorn app.main:app --reload
```

### 4) Request recommendations

```bash
curl -X POST http://127.0.0.1:8000/buyer-agent/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "item_name": "Nitrile Gloves",
    "quantity": 5000,
    "budget_per_unit": 0.11,
    "delivery_days_max": 20,
    "destination_country": "US",
    "quality_min_score": 80,
    "required_certifications": ["ISO9001", "CE"]
  }'
```

### 5) Run tests

```bash
pytest
```
