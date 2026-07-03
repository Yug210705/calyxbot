import { RefreshCw } from "lucide-react";

interface Props {
  onRefresh: () => void;
  isRefreshing: boolean;
}

export function DocumentsHeader({ onRefresh, isRefreshing }: Props) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between mb-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Documents</h1>
        <p className="mt-2 text-muted-foreground">
          View and manage documents indexed across your connected data sources.
        </p>
      </div>
      
      <button 
        onClick={onRefresh}
        disabled={isRefreshing}
        className="inline-flex items-center justify-center gap-2 rounded-md border bg-background px-4 py-2 text-sm font-medium hover:bg-muted disabled:opacity-50 disabled:pointer-events-none transition-colors"
      >
        <RefreshCw className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`} />
        Refresh
      </button>
    </div>
  );
}
