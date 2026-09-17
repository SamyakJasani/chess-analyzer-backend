# Chess Analyzer Backend

Flask backend for integrating external APIs. It currently has no database dependency.

## Setup

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

The local server runs at `http://127.0.0.1:5000`.

## Endpoints

- `GET /api/health` returns the service health status.
- `GET /api/users/<username>` returns the player's Chess.com profile.
- `GET /api/users/<username>/games` loads the player's latest monthly archive and returns its games in descending order.
- `GET /api/openapi.json` returns the Pydantic-generated OpenAPI 3.0.3 contract.

The application is organized into `models`, `repositories`, `services`, and `routes`. The repository currently reads from Chess.com's API; database models and repositories can be added later without moving route logic. Runtime configuration belongs in `.env`; it is ignored by Git.

## Production-style startup

```powershell
waitress-serve --listen=127.0.0.1:5000 run:app
```
