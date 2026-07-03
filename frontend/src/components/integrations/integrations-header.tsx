/* eslint-disable react/no-unescaped-entities */
import { Plus } from "lucide-react";

interface IntegrationsHeaderProps {
  onConnectGoogleDrive: () => void;
  isConnecting: boolean;
}

export function IntegrationsHeader({ onConnectGoogleDrive, isConnecting }: IntegrationsHeaderProps) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Integrations</h1>
        <p className="mt-2 text-muted-foreground">
          Connect data sources to build your organization's semantic memory.
        </p>
      </div>
      
      <button 
        onClick={onConnectGoogleDrive}
        disabled={isConnecting}
        className="inline-flex items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 disabled:pointer-events-none transition-colors"
      >
        <Plus className="h-4 w-4" />
        {isConnecting ? "Connecting..." : "Connect Google Drive"}
      </button>
    </div>
  );
}
