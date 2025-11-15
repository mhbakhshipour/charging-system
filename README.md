# Charging System

A Django + DRF application for CHARGING SYSTEM with production‑grade concurrency: atomic balance updates, idempotent unsafe requests, rate limiting, Redis caching, and Celery background processing.

## Quick Start
- Python 3.14 and Redis and PostgreSQL required
- Create virtualenv and install dependencies
  - `poety install`
- Set environment variables like `.env.sample` or a `.env` file
- Run web (ASGI) and worker processes

## Run
- Web API (ASGI, high concurrency)
  - `uvicorn charging_system_b2b.asgi:application --host 0.0.0.0 --port 8000 --workers 4`
- Celery worker
  - `celery -A charging_system_b2b worker -l info -c 4`
- Optional Celery beat
  - `celery -A charging_system_b2b beat -l info`

## Authentication
- Obtain token: `POST /api/auth/token/` with `username` and `password`
- Send `Authorization: Token <token>` on protected endpoints

## Endpoints
- `POST /api/vendor/submit-request/`
  - Body: `{ "requester": <vendor_id>, "amount": <int> }`
  - Response: `{ "data": { ... } }`
- `GET /api/vendor/approve-request/?request_credit_id=<id>`
  - Response: `{ "status": "accepted" }`
  - Work is processed asynchronously by Celery
- `POST /api/customer/increase-credit/`
  - Body: `{ "vendor": <vendor_id>, "customer": <customer_id>, "amount": <int> }`
  - Response: `{ "status": "accepted", "data": { ... } }`
  - Work is processed asynchronously by Celery

## Concurrency & Safety
- Atomic balance updates with `transaction.atomic`, `select_for_update`, and `F()` expressions
- Global idempotency for unsafe methods
  - Send `Idempotency-Key: <unique-id>` header to safely retry
- Rate limiting for unsafe methods
  - Defaults: `10` requests per `60s` per IP+path (see `charging_system_b2b/settings.py`)
- Redis is used for cache, idempotency store, and rate‑limit counters
- Celery background tasks with distributed locks

## Testing
- Run tests: `ENV=TEST python manage.py test -v 2`
- Tests verify
  - Endpoint workflows, balances, and transaction sums
  - Concurrency behavior for approvals and credit increases

## Examples
- Submit vendor credit request
  - `curl -X POST http://localhost:8000/api/vendor/submit-request/ -H "Authorization: Token <token>" -H "Content-Type: application/json" -d '{"requester": 1, "amount": 100}'`
- Approve request
  - `curl "http://localhost:8000/api/vendor/approve-request/?request_credit_id=1" -H "Authorization: Token <token>"`
- Increase customer credit
  - `curl -X POST http://localhost:8000/api/customer/increase-credit/ -H "Authorization: Token <token>" -H "Idempotency-Key: 123e4567" -H "Content-Type: application/json" -d '{"vendor": 1, "customer": 10, "amount": 50}'`

## Notes
- Use ASGI server (`uvicorn`) for higher throughput
- Keep Redis and Postgres tuned and reachable
- Prefer sending `Idempotency-Key` on POST/PUT/PATCH for safe retries
