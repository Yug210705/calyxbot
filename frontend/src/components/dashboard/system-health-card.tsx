import { AlertTriangle, CheckCircle2, Server, Globe, Database } from "lucide-react";
import { cn } from "@/lib/utils";

interface Props {
  health: Record<string, string>;
}

export function SystemHealthCard({ health }: Props) {
  const syncHealthy = health.sync === "healthy";
  const searchReady = health.search === "ready";
  const ingestionConnected = health.ingestion === "connected";

  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
      <div className="p-6 pb-4">
        <h3 className="font-semibold leading-none tracking-tight">System Health</h3>
      </div>
      <div className="p-6 pt-0">
        <div className="space-y-4">
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Server className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Search Readiness</span>
            </div>
            <div className={cn("flex items-center gap-1.5 text-sm", searchReady ? "text-green-600" : "text-amber-600")}>
              {searchReady ? <CheckCircle2 className="h-4 w-4" /> : <AlertTriangle className="h-4 w-4" />}
              <span className="capitalize">{health.search}</span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Globe className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Ingestion Pipeline</span>
            </div>
            <div className={cn("flex items-center gap-1.5 text-sm", ingestionConnected ? "text-green-600" : "text-amber-600")}>
              {ingestionConnected ? <CheckCircle2 className="h-4 w-4" /> : <AlertTriangle className="h-4 w-4" />}
              <span className="capitalize">{health.ingestion.replace("_", " ")}</span>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Database className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Sync Status</span>
            </div>
            <div className={cn("flex items-center gap-1.5 text-sm", syncHealthy ? "text-green-600" : "text-amber-600")}>
              {syncHealthy ? <CheckCircle2 className="h-4 w-4" /> : <AlertTriangle className="h-4 w-4" />}
              <span className="capitalize">{health.sync}</span>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
