const highlights = [
  {
    title: 'Two-feature input',
    text: 'The UI maps directly to the Height and Weight features used by the saved clustering model.',
  },
  {
    title: 'Simpler interaction',
    text: 'Instead of editing JSON by hand, the user can add rows and submit them with one click.',
  },
  {
    title: 'Clean response handling',
    text: 'The app renders the cluster labels returned from the API in a readable format.',
  },
];

export default function AboutPage() {
  return (
    <div className="page-stack about-page">
      <section className="panel about-hero">
        <p className="eyebrow">About the app</p>
        <h2>Designed for a local ML demo that still feels production-grade.</h2>
        <p className="lead">
          This frontend keeps the interface focused on your clustering model while staying quick to
          use, responsive, and easy to read.
        </p>
      </section>

      <section className="feature-grid">
        {highlights.map((highlight) => (
          <article className="panel feature-card" key={highlight.title}>
            <p className="eyebrow">Architecture note</p>
            <h3>{highlight.title}</h3>
            <p>{highlight.text}</p>
          </article>
        ))}
      </section>

      <section className="panel about-footer">
        <h3>Backend contract</h3>
        <p>
          Send a POST request containing a JSON object with Height and Weight arrays. The
          response is a JSON object with a predictions array and sample count.
        </p>
      </section>
    </div>
  );
}