"use client";

import { AppSidebar } from "./app-sidebar";
import { AppHeader } from "./app-header";
import { useSystemStatus } from "@/lib/hooks/use-system-status";
import { SystemStatusBanner } from "../system/system-status-banner";

interface AppShellProps {
  children: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  const { status } = useSystemStatus();

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <AppSidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <AppHeader />
        {status && <SystemStatusBanner status={status} />}
        <main className="flex-1 overflow-y-auto bg-muted/10 p-6 md:p-8">
          <div className="mx-auto max-w-7xl">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
