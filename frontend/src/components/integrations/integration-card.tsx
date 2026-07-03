import { IntegrationConnection, IntegrationProvider } from "@/lib/types/integrations";
import { IntegrationStatusBadge } from "./integration-status-badge";
import { IntegrationHealthBadge } from "./integration-health-badge";
import { Database, Folder, MessageSquare, Play, Pause, Trash2, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";

interface IntegrationCardProps {
  connection?: IntegrationConnection; // Present if connected
  provider?: IntegrationProvider;     // Present if available (not connected)
  onSync?: () => void;
  onDisconnect?: () => void;
  onConnect?: () => void;
  isActionPending?: boolean;
}

const providerIcons = {
  google_drive: Folder,
  notion: Database,
  slack: MessageSquare,
};

export function IntegrationCard({ 
  connection, 
  provider, 
  onSync, 
  onDisconnect, 
  onConnect,
  isActionPending 
}: IntegrationCardProps) {
  
  const isConnected = !!connection;
  const name = connection?.displayName || provider?.name || "Unknown";
  const type = connection?.provider || provider?.provider || "google_drive";
  const description = provider?.description || (isConnected ? "Connected data source" : "");
  
  const Icon = providerIcons[type as keyof typeof providerIcons] || Database;

  return (
    <div className="flex flex-col rounded-xl border bg-card p-6 shadow-sm">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted">
            <Icon className="h-5 w-5" />
          </div>
          <div>
            <h3 className="font-semibold">{name}</h3>
            {isConnected ? (
              <div className="mt-1 flex items-center gap-2">
                <IntegrationStatusBadge status={connection.status} />
                <IntegrationHealthBadge health={connection.health} />
              </div>
            ) : (
              <p className="mt-1 text-sm text-muted-foreground">{description}</p>
            )}
          </div>
        </div>
      </div>

      {isConnected && connection && (
        <div className="mt-6 grid grid-cols-2 gap-4 rounded-lg bg-muted/50 p-4 text-sm">
          <div>
            <p className="text-muted-foreground">Documents</p>
            <p className="font-medium">{connection.documentCount.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-muted-foreground">Last Sync</p>
            <p className="font-medium">
              {connection.lastSyncAt 
                ? new Date(connection.lastSyncAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
                : "Never"}
            </p>
          </div>
        </div>
      )}

      <div className="mt-6 flex flex-wrap items-center gap-3 pt-auto">
        {isConnected ? (
          <>
            <button 
              onClick={onSync}
              disabled={isActionPending || connection.syncState === "SYNCING"}
              className="inline-flex items-center gap-2 rounded-md bg-secondary px-3 py-1.5 text-sm font-medium text-secondary-foreground hover:bg-secondary/80 disabled:opacity-50 transition-colors"
            >
              <RefreshCw className={cn("h-4 w-4", (connection.syncState === "SYNCING" || isActionPending) && "animate-spin")} />
              {connection.syncState === "SYNCING" || isActionPending ? "Syncing..." : "Sync Now"}
            </button>
            <button 
              disabled={isActionPending}
              className="inline-flex items-center gap-2 rounded-md border px-3 py-1.5 text-sm font-medium hover:bg-muted disabled:opacity-50 transition-colors"
            >
              {connection.syncState === "PAUSED" ? (
                <><Play className="h-4 w-4" /> Resume</>
              ) : (
                <><Pause className="h-4 w-4" /> Pause</>
              )}
            </button>
            <button 
              onClick={onDisconnect}
              disabled={isActionPending}
              className="ml-auto inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium text-red-500 hover:bg-red-500/10 disabled:opacity-50 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
              Disconnect
            </button>
          </>
        ) : (
          <button 
            onClick={onConnect}
            disabled={isActionPending || !provider?.available}
            className="inline-flex w-full items-center justify-center gap-2 rounded-md border px-4 py-2 text-sm font-medium hover:bg-muted disabled:opacity-50 transition-colors"
          >
            {provider?.available ? "Connect" : "Coming Soon"}
          </button>
        )}
      </div>
    </div>
  );
}
