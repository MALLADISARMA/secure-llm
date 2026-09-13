import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Navbar from "./components/Navbar";

import Dashboard from "./pages/DashBoard";
import Analyzer from "./pages/Analyzer";
import History from "./pages/History";

export default function App() {
  return (
    <BrowserRouter>

      <div className="min-h-screen bg-slate-50">

        <Navbar />

        <Routes>

          <Route
            path="/"
            element={<Dashboard />}
          />

          <Route
            path="/analyzer"
            element={<Analyzer />}
          />

          <Route
            path="/history"
            element={<History />}
          />

        </Routes>

      </div>

    </BrowserRouter>
  );
}