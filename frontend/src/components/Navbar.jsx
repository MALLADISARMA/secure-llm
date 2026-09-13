import { NavLink } from "react-router-dom";
import {
  ShieldCheck,
  LayoutDashboard,
  ScanSearch,
  History,
} from "lucide-react";

const navigation = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Analyzer",
    path: "/analyzer",
    icon: ScanSearch,
  },
  {
    name: "History",
    path: "/history",
    icon: History,
  },
];

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">

        {/* Logo */}
        <NavLink to="/" className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-900">
            <ShieldCheck className="h-5 w-5 text-white" />
          </div>

          <div>
            <h1 className="text-sm font-bold text-slate-900">
              SecureLLM
            </h1>

            <p className="text-[10px] font-medium uppercase tracking-wider text-slate-400">
              AI Security Gateway
            </p>
          </div>
        </NavLink>

        {/* Navigation */}
        <nav className="flex items-center gap-1">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === "/"}
                className={({ isActive }) =>
                  `flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition ${
                    isActive
                      ? "bg-slate-100 text-slate-900"
                      : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                  }`
                }
              >
                <Icon className="h-4 w-4" />
                {item.name}
              </NavLink>
            );
          })}
        </nav>

      </div>
    </header>
  );
}