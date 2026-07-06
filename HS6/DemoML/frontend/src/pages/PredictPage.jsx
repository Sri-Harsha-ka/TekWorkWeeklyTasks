import { useMemo, useState } from 'react';
import {
  buildPayload,
  defaultApiPath,
  defaultApiUrl,
  formatJson,
  requestPredictions,
  sampleRows,
} from '../lib/api';

function createRow(height = '', weight = '') {
  return {
    id: crypto.randomUUID(),
    Height: height,
    Weight: weight,
  };
}

function cloneSampleRows() {
  return sampleRows.map((row) => ({
    id: crypto.randomUUID(),
    Height: row.Height,
    Weight: row.Weight,
  }));
}

function extractPredictions(data) {
  if (Array.isArray(data)) {
    return data;
  }

  if (data && Array.isArray(data.predictions)) {
    return data.predictions;
  }

  return [];
}

export default function PredictPage() {
  const [apiUrl, setApiUrl] = useState(defaultApiUrl);
  const [apiPath, setApiPath] = useState(defaultApiPath);
  const [rows, setRows] = useState(() => cloneSampleRows());
  const [predictionData, setPredictionData] = useState(null);
  const [error, setError] = useState('');
  const [status, setStatus] = useState('Ready to predict');
  const [isLoading, setIsLoading] = useState(false);

  const preview = useMemo(() => {
    try {
      return formatJson(buildPayload(rows));
    } catch (previewError) {
      return previewError.message;
    }
  }, [rows]);

  const predictions = predictionData ? extractPredictions(predictionData) : [];

  function updateRow(rowId, field, value) {
    setRows((currentRows) =>
      currentRows.map((row) => (row.id === rowId ? { ...row, [field]: value } : row)),
    );
  }

  function addRow() {
    setRows((currentRows) => [...currentRows, createRow()]);
  }

  function removeRow(rowId) {
    setRows((currentRows) => {
      if (currentRows.length <= 2) {
        return currentRows;
      }

      return currentRows.filter((row) => row.id !== rowId);
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setPredictionData(null);

    let payload;

    try {
      payload = buildPayload(rows);
    } catch (validationError) {
      setError(validationError.message);
      setStatus('Fix the measurements before sending');
      return;
    }

    const controller = new AbortController();
    setIsLoading(true);
    setStatus('Sending measurements to the API');

    try {
      const data = await requestPredictions({
        apiUrl,
        apiPath,
        payload,
        signal: controller.signal,
      });

      setPredictionData(data);
      setStatus('Prediction received');
    } catch (requestError) {
      setError(requestError.message || 'Request failed');
      setStatus('Unable to retrieve predictions');
    } finally {
      setIsLoading(false);
    }
  }

  function loadSampleData() {
    setRows(cloneSampleRows());
    setPredictionData(null);
    setError('');
    setStatus('Loaded sample measurements');
  }

  const predictionItems = predictions.map((prediction, index) => ({
    row: rows[index],
    value: String(prediction),
  }));

  return (
    <div className="studio-layout">
      <section className="panel panel-form">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Prediction studio</p>
            <h2>Enter a few measurements and cluster them.</h2>
            <p className="form-hint">
              Add at least two rows. The app sends the measurements to <strong>/predict</strong> and
              renders the returned cluster labels.
            </p>
          </div>
          <div className="form-actions">
            <button className="button button-secondary button-small" type="button" onClick={loadSampleData}>
              Load sample
            </button>
            <button className="button button-secondary button-small" type="button" onClick={addRow}>
              Add row
            </button>
          </div>
        </div>

        <form className="prediction-form" onSubmit={handleSubmit}>
          <div className="sample-list">
            {rows.map((row, index) => (
              <div className="sample-row" key={row.id}>
                <div className="sample-row-header">
                  <p className="row-label">Sample {index + 1}</p>
                  <button
                    className="text-link row-remove"
                    type="button"
                    onClick={() => removeRow(row.id)}
                    disabled={rows.length <= 2}
                  >
                    Remove
                  </button>
                </div>

                <div className="field-grid">
                  <label className="field">
                    <span>Height</span>
                    <input
                      type="number"
                      inputMode="numeric"
                      value={row.Height}
                      onChange={(event) => updateRow(row.id, 'Height', event.target.value)}
                      placeholder="170"
                    />
                  </label>

                  <label className="field">
                    <span>Weight</span>
                    <input
                      type="number"
                      inputMode="numeric"
                      value={row.Weight}
                      onChange={(event) => updateRow(row.id, 'Weight', event.target.value)}
                      placeholder="65"
                    />
                  </label>
                </div>
              </div>
            ))}
          </div>

          <div className="action-row">
            <button className="button button-primary" type="submit" disabled={isLoading}>
              {isLoading ? 'Predicting...' : 'Run prediction'}
            </button>
            <p className="status-text">{status}</p>
          </div>

          {error ? <div className="alert alert-error">{error}</div> : null}
        </form>
      </section>

      <aside className="studio-sidebar">
        <section className="panel side-panel">
          <div className="panel-header compact">
            <div>
              <p className="eyebrow">Payload preview</p>
              <h3>Live JSON</h3>
            </div>
          </div>
          <pre className="code-block preview-block">{preview}</pre>
        </section>

        <section className="panel side-panel">
          <div className="panel-header compact">
            <div>
              <p className="eyebrow">Model response</p>
              <h3>Cluster labels</h3>
            </div>
          </div>

          {predictionItems.length > 0 ? (
            <div className="prediction-list">
              {predictionItems.map((item, index) => (
                <div className="prediction-pill" key={`${index}-${item}`}>
                  <div className="prediction-pill-top">
                    <span className="prediction-index">Sample 0{index + 1}</span>
                    <span className="cluster-chip">Cluster {item.value}</span>
                  </div>
                  <pre>
                    Height {item.row?.Height} cm · Weight {item.row?.Weight} kg
                  </pre>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>Your cluster labels will appear here after the request completes.</p>
            </div>
          )}
        </section>
      </aside>
    </div>
  );
}