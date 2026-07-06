import { Link } from 'react-router-dom';
import { buildPayload, formatJson, sampleRows } from '../lib/api';

const featureCards = [
  {
    title: 'Simple input flow',
    text: 'Add a few height and weight rows, then send them straight to the FastAPI endpoint.',
  },
  {
    title: 'Model-friendly payload',
    text: 'The frontend converts the rows into the exact Height and Weight arrays your model expects.',
  },
  {
    title: 'FastAPI ready',
    text: 'The app posts JSON directly to the local service and renders the returned cluster labels cleanly.',
  },
];

const workflowSteps = [
  'Enter or load a small set of measurements.',
  'Send the rows to the local FastAPI endpoint.',
  'Inspect the payload preview and returned cluster labels.',
];

export default function HomePage() {
  return (
    <div className="page-stack">
      <section className="hero-grid">
        <div className="hero-copy panel panel-hero">
          <p className="eyebrow">Hierarchical clustering dashboard</p>
          <h2>Turn a few body measurements into cluster labels.</h2>
          <p className="lead">
            This frontend is designed for your FastAPI service running locally on port 8000.
            It keeps the workflow minimal for testing and easier to use.
          </p>

          <div className="hero-actions">
            <Link className="button button-primary" to="/predict">
              Open prediction studio
            </Link>
            <Link className="button button-secondary" to="/about">
              View architecture
            </Link>
          </div>

          <div className="metric-row">
            <article className="metric-card">
              <span>Input format</span>
              <strong>Editable rows</strong>
            </article>
            <article className="metric-card">
              <span>Backend</span>
              <strong>localhost:8000</strong>
            </article>
          </div>
        </div>

        <div className="panel payload-panel">
          <div className="panel-header">
            <p className="eyebrow">Training sample</p>
            <h3>Example JSON payload</h3>
          </div>
          <pre className="code-block">{formatJson(buildPayload(sampleRows))}</pre>
          <div className="payload-note">
            <span>Expected response</span>
            <strong>JSON array of cluster labels</strong>
          </div>
        </div>
      </section>

      <section className="feature-grid">
        {featureCards.map((card) => (
          <article className="panel feature-card" key={card.title}>
            <p className="eyebrow">Core value</p>
            <h3>{card.title}</h3>
            <p>{card.text}</p>
          </article>
        ))}
      </section>

      <section className="panel process-panel">
        <div className="panel-header compact">
          <div>
            <p className="eyebrow">Workflow</p>
            <h3>Three-step prediction flow</h3>
          </div>
          <Link className="text-link" to="/predict">
            Go to studio
          </Link>
        </div>

        <div className="steps-list">
          {workflowSteps.map((step, index) => (
            <div className="step-item" key={step}>
              <span className="step-index">0{index + 1}</span>
              <p>{step}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}