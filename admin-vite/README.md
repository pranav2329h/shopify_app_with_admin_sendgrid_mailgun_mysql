# Admin UI (Vite + React)

## Dev
```bash
npm install
npm run dev
```

## Build
```bash
npm run build
```
Copy the `dist/` folder to `deploy/static/app/`:
```bash
rm -rf ../../deploy/static/app && mkdir -p ../../deploy/static/app
cp -r dist/* ../../deploy/static/app/
```

The UI will be available at `https://YOUR_DOMAIN/app/` and talks to the backend at `/admin/*` and `/tasks/*`.