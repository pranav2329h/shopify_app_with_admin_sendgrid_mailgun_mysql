# Shopify Auto Email App

This project is a full-stack Flask + React app that integrates with Shopify webhooks and sends Gmail-based notification emails. It includes:

## Features
- 📬 Sends emails (via Gmail SMTP using app password)
- 🧠 Logs every email in MySQL
- 🧾 Displays logs in real-time in a React admin panel
- 🪝 Accepts Shopify webhooks for registration (expandable)

## Setup Instructions

### Backend

1. Install Python dependencies:
```bash
cd backend
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Create `.env` from `.env.example` and fill values (esp. Gmail + DB).

3. Start Flask app:
```bash
python run.py
```

### Frontend

1. Install Node.js and dependencies:
```bash
cd frontend
npm install
```

2. Start React dev server:
```bash
npm run dev
```

## Notes

- Make sure MySQL is running and DB is created before backend starts.
- You must use a Gmail **App Password** (not your regular password).