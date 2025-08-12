# Docker deployment (Gunicorn + Nginx + HTTPS)

## 1) Set environment
- Fill `backend/.env` with your real values (SHOPIFY keys, DB, email provider, APP_BASE_URL).
- Make sure `APP_BASE_URL=https://YOUR_DOMAIN`

## 2) Set domain in Nginx (HTTP)
Edit `deploy/nginx/conf.d/app.conf` and replace `YOUR_DOMAIN` with your real domain.

## 3) Build & run (HTTP only)
```
docker compose -f deploy/docker-compose.yml up -d --build
```

## 4) Issue HTTPS certificate (Let's Encrypt, webroot)
Point your domain DNS to this server, then run:
```
./deploy/issue-cert.sh your-domain.com admin@your-domain.com
```
This obtains the cert and switches Nginx to the TLS config.

## 5) Renewals
`certbot` container auto-renews certs every 12h (via cron-like loop).

## 6) Static assets
Nginx serves `/static/` from `deploy/static/`. Your logo is available at:
`https://YOUR_DOMAIN/static/logo.svg`

## 7) Backend
Gunicorn runs the Flask app at `backend:5000` inside Docker.
```