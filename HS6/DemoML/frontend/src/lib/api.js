export const defaultApiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
export const defaultApiPath = import.meta.env.VITE_API_PATH ?? '/predict';

export const sampleRows = [
  { id: 'sample-1', Height: 170, Weight: 65 },
  { id: 'sample-2', Height: 162, Weight: 67 },
  { id: 'sample-3', Height: 168, Weight: 63 },
  { id: 'sample-4', Height: 190, Weight: 95 },
  { id: 'sample-5', Height: 192, Weight: 98 },
  { id: 'sample-6', Height: 188, Weight: 92 },
];

function parseMeasurement(value, label, rowNumber) {
  const parsedValue = Number(value);

  if (value === '' || Number.isNaN(parsedValue)) {
    throw new Error(`Row ${rowNumber}: enter a valid number for ${label}.`);
  }

  return parsedValue;
}

export function buildPayload(rows) {
  if (!Array.isArray(rows) || rows.length < 2) {
    throw new Error('Add at least two rows before predicting.');
  }

  return {
    Height: rows.map((row, index) => parseMeasurement(row.Height, 'Height', index + 1)),
    Weight: rows.map((row, index) => parseMeasurement(row.Weight, 'Weight', index + 1)),
  };
}

export function formatJson(value) {
  return JSON.stringify(value, null, 2);
}

export async function requestPredictions({ apiUrl, apiPath, payload, signal }) {
  const url = new URL(apiPath, apiUrl).toString();
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
    signal,
  });

  const contentType = response.headers.get('content-type') ?? '';
  const data = contentType.includes('application/json')
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message = typeof data === 'string' ? data : data?.detail ?? data?.message;
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return data;
}