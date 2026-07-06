import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <section className="panel notfound-panel">
      <p className="eyebrow">404</p>
      <h2>Page not found</h2>
      <p>The route you requested does not exist. Return to the dashboard or open the prediction studio.</p>
      <div className="hero-actions">
        <Link className="button button-primary" to="/">
          Back home
        </Link>
        <Link className="button button-secondary" to="/predict">
          Open prediction studio
        </Link>
      </div>
    </section>
  );
}