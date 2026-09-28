import { Link, Route, Routes } from "react-router-dom";
import PlayerList from "./pages/PlayerList.jsx";
import PlayerProfile from "./pages/PlayerProfile.jsx";

export default function App() {
  return (
    <div className="app">
      <header className="topbar">
        <Link to="/" className="brand">
          ASI <span>Scouting</span>
        </Link>
      </header>
      <main className="container">
        <Routes>
          <Route path="/" element={<PlayerList />} />
          <Route path="/players/:id" element={<PlayerProfile />} />
          <Route
            path="*"
            element={
              <div className="status status--error">
                Pagina non trovata. <Link to="/">Torna alla lista</Link>
              </div>
            }
          />
        </Routes>
      </main>
    </div>
  );
}
