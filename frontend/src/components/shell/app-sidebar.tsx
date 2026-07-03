"use client";

import {
  LayoutDashboard,
  Plug,
  Files,
  Search,
  Settings
} from "lucide-react";
import { NavItem } from "./nav-item";

export function AppSidebar() {
  return (
    <aside className="w-64 border-r bg-muted/30 flex flex-col h-full">
      <div className="p-6">
        <h1 className="text-xl font-bold text-primary tracking-tight">Calyx</h1>
      </div>
      
      <div className="flex-1 px-4 space-y-1">
        <NavItem href="/dashboard" icon={LayoutDashboard} label="Dashboard" />
        <NavItem href="/integrations" icon={Plug} label="Integrations" />
        <NavItem href="/documents" icon={Files} label="Documents" />
        <NavItem href="/search" icon={Search} label="Search Memory" />
      </div>
      
      <div className="p-4 border-t">
        <NavItem href="/settings" icon={Settings} label="Settings" />
      </div>
    </aside>
  );
}
