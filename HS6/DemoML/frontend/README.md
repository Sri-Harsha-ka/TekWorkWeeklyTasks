# Clustering Studio Frontend

Modern Vite + React + React Router DOM frontend for the FastAPI clustering service running locally at `http://localhost:8000`.

## Setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the dev server:

   ```bash
   npm run dev
   ```

## Backend Integration

The prediction page posts JSON payloads in this format:

```json
{
  "Height": [170, 162, 168, 190, 192, 188],
  "Weight": [65, 67, 63, 95, 98, 92]
}
```

By default, the app targets `http://localhost:8000/predict`. You can change this in the UI or with environment variables:

- `VITE_API_URL` - defaults to `http://localhost:8000`
- `VITE_API_PATH` - defaults to `/predict`

## Build

```bash
npm run build
```