import { NavLink, Outlet } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Home' },
  { to: '/predict', label: 'Predict' },
  { to: '/about', label: 'About' },
];

export default function Layout() {
  return (
    <div className="app-shell">
      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark">CS</div>
          <div>
            <p className="eyebrow">FastAPI Model Interface</p>
            <h1 className="brand-title">Clustering Studio</h1>
          </div>
        </div>

        <nav className="nav-links" aria-label="Primary navigation">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
              end={item.to === '/'}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="status-pill">FastAPI connected</div>
      </header>

      <main className="page-shell">
        <Outlet />
      </main>

      <footer className="footer-bar">
        <p>Built for hierarchical clustering predictions with a premium React UI.</p>
        <p>Backend target: localhost:8000/predict</p>
      </footer>
    </div>
  );
}