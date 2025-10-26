# moumatanaiiiii

# miwax — LINE Queue Notifier + Web UI

Queue management tool that:

- Assigns reservation numbers to LINE subscribers and replies with estimated wait time.
- Lets staff advance the queue and tune average service time via a simple web UI.
- Push-notifies the next user on LINE when their turn comes.
- Optionally replies to free-form messages using Azure OpenAI.


## System Design

graph TD
  U[User (LINE App)] -->|Follow| L[LINE Messaging API]
  L -->|Webhook /callback| W[Flask Webhook Server (main.py)]
  W -->|Append record| UD[(user_data.json)]
  W -->|Reply: Number + Wait| U

  S[Staff (Web UI)] -->|Adjust yobidasi/syoyojikan| Q[Queue Manager (app/app.py)]
  Q -->|Write| NUM[(app/numbers.json)]
  FW[Watchdog Thread] -->|Monitor change| NUM
  FW -->|Lookup user_id for yobidasi| UD
  FW -->|Push: Your turn!| L
  L --> U

  U -->|Text 'キャンセル'| L
  L --> W
  W -->|Mark canceled (user_id=0)| UD
  W -->|Ack cancel| U


## Repository Layout

- `main.py` — LINE webhook server, file watcher, optional Azure OpenAI replies.
- `app/app.py` — Web UI for queue operations (call next, adjust service time).
- `app/templates/index.html` — Web UI page.
- `app/numbers.json` — Current called number and per-user service time.
- `user_data.json` — Line-delimited JSON reservation log (one JSON object per line).
- `Dockerfile`, `compose.yaml` — Containerization and dev runtime (with ngrok).
- `requirements.txt` — Flask, ngrok, line-bot-sdk, watchdog, openai.


## How It Works

- New subscriber (Follow event)
  - User adds the LINE bot; `main.py` logs a new entry in `user_data.json` with an incremented reservation number `yoyaku` and the LINE `user_id`.
  - The bot replies with the assigned number and an estimated wait based on `app/numbers.json` values `yobidasi` (current called number) and `syoyojikan` (avg service time seconds).

- Advancing the queue
  - Staff opens the Web UI and increases `yobidasi` (call next) or adjusts `syoyojikan` (tune average).
  - A watchdog thread in `main.py` monitors `app/numbers.json`; when `yobidasi` changes, it finds the matching `user_id` from `user_data.json` and sends a LINE push message “順番になりました!” (It’s your turn!).
  - The processed reservation is then marked by setting its `user_id` to `0`.

- Cancellation
  - If a user sends “キャンセル”, the bot updates that reservation’s `user_id` to `0` and replies with an acknowledgment.


## Data Model

- `app/numbers.json` (single JSON object)
  - Example: `{ "yobidasi": 1, "syoyojikan": 120 }`
  - `yobidasi`: current called number (int)
  - `syoyojikan`: average service time in seconds (int)

- `user_data.json` (line-delimited JSON; one object per line)
  - Example: `{ "yoyaku": 12, "user_id": "<LINE_USER_ID>", "timestamp": 1710000000 }`
  - When notified or canceled, the reservation is marked by setting `user_id` to `0`.


## Prerequisites

- LINE Developers account and Messaging API channel.
- ngrok account and authtoken (for development tunneling).
- Python 3.10+ locally or Docker.
- Azure OpenAI (optional) if using AI replies.


## Configuration

Create a `.env` in the project root:

```
NGROK_AUTHTOKEN="<your_ngrok_token>"
LINE_CHANNEL_SECRET="<your_line_channel_secret>"
LINE_CHANNEL_ACCESS_TOKEN="<your_line_channel_access_token>"
```

Initialize `app/numbers.json` with sensible values (edit the file if empty):

```
{ "yobidasi": 1, "syoyojikan": 120 }
```

Security note: Never commit real secrets. Rotate any credentials already present in code or logs; replace them with environment variables in production.


## Run with Docker Compose

1) Build and start the webhook server with ngrok tunnel:

```
docker compose up --build
```

2) In LINE Developers Console, set the webhook URL to:

```
https://<your-ngrok-url>/callback
```

3) Start the Queue Manager UI inside the running container (second terminal):

```
docker compose exec python python app/app.py
```

Ports
- Webhook server: `:8888` (exposed by compose and forwarded via ngrok)
- Queue Manager UI: `:5000` (inside container; reachable at http://localhost:5000)


## Run Locally (without Docker)

```
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt

export ENV=dev
export NGROK_AUTHTOKEN=...
export LINE_CHANNEL_SECRET=...
export LINE_CHANNEL_ACCESS_TOKEN=...

# Start webhook server (spawns ngrok in dev)
python main.py  # listens on :8888

# In a second terminal, start the queue UI
python app/app.py  # serves UI on :5000
```

Set your LINE webhook to `https://<ngrok-url>/callback` and add the bot as a friend to test.


## Queue Manager UI

Open `http://localhost:5000/` and use the buttons:

- `呼び出す` — increments `yobidasi` by 1 (call next).
- `所要時間10秒減らす` / `所要時間10秒増やす` — adjust `syoyojikan`.

Displayed fields:
- 最新番号 (latest reserved in `user_data.json`)
- 呼び出し番号 (current called `yobidasi`)
- 待ち時間 (calculated minutes)
- 所要時間 (per-customer seconds)

Tip: Replace `app/static/048ofjnh.png` with your own Add-Friend QR.


## Notes and Caveats

- Paths: The webhook server uses `./app/numbers.json`, while the UI reads/writes `numbers.json` relative to its working directory. Running `python app/app.py` ensures the UI uses `app/numbers.json` as intended.
- Persistence: `cancelList` is in-memory; canceled reservations remain marked by `user_id=0`, but the list itself resets on restart.
- Files: `user_data.json` is line-delimited JSON; avoid manual edits during runtime to prevent corruption.
- Secrets: Do not commit `.env`, tokens, or keys. Consider adding `debug.log` and `user_data.json` to `.gitignore` for development.
- Azure OpenAI: The sample includes hard-coded credentials in `main.py` for demo. Replace with environment variables or remove AI replies for production.


## Troubleshooting

- No LINE replies: Check that ngrok printed a public URL and your webhook is set and enabled. Inspect `debug.log`.
- No push notification on call: Ensure `app/numbers.json` updates when pressing UI buttons; verify the watchdog is running (started with `main.py`).
- JSON errors: Verify `app/numbers.json` contains valid JSON and `user_data.json` has one JSON object per line.
- Port conflicts: Change the compose ports or local run ports as needed.


---

This project is for demonstration and should be hardened before production use (authN/Z for staff UI, robust storage, retry logic, rate limiting, structured logging, etc.).

>>>>>>> Describe your changes here.
