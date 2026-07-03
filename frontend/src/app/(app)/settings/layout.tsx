import React from "react";
import Link from "next/link";
import { Settings, Sliders, Server } from "lucide-react";

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col md:flex-row gap-8">
      {/* Sidebar for settings navigation */}
      <aside className="w-full md:w-64 shrink-0">
        <h2 className="text-xl font-bold mb-6 px-2">Settings</h2>
        <nav className="space-y-1">
          <Link 
            href="/settings" 
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-primary/10 text-primary font-medium transition-colors"
          >
            <Settings className="h-4 w-4" />
            General
          </Link>
          <Link 
            href="#" 
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-muted-foreground hover:bg-muted/50 hover:text-foreground transition-colors cursor-not-allowed opacity-50"
          >
            <Sliders className="h-4 w-4" />
            Appearance
            <span className="ml-auto text-[10px] uppercase tracking-wider font-semibold border rounded px-1.5 py-0.5">Soon</span>
          </Link>
          <Link 
            href="#" 
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-muted-foreground hover:bg-muted/50 hover:text-foreground transition-colors cursor-not-allowed opacity-50"
          >
            <Server className="h-4 w-4" />
            Advanced
            <span className="ml-auto text-[10px] uppercase tracking-wider font-semibold border rounded px-1.5 py-0.5">Soon</span>
          </Link>
        </nav>
      </aside>

      {/* Main settings content area */}
      <div className="flex-1 max-w-3xl">
        {children}
      </div>
    </div>
  );
}
