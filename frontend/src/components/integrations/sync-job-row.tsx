import { SyncJob } from "@/lib/types/integrations";
import { CheckCircle2, CircleDashed, Clock, XCircle, Folder, MessageSquare, Database, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface SyncJobRowProps {
  job: SyncJob;
}

const statusConfig = {
  PENDING: { icon: Clock, className: "text-muted-foreground", label: "Pending" },
  RUNNING: { icon: CircleDashed, className: "text-blue-500 animate-spin-slow", label: "Running" },
  SUCCESS: { icon: CheckCircle2, className: "text-emerald-500", label: "Completed" },
  FAILED: { icon: XCircle, className: "text-red-500", label: "Failed" },
};

const providerIcons = {
  google_drive: Folder,
  notion: Database,
  slack: MessageSquare,
};

export function SyncJobRow({ job }: SyncJobRowProps) {
  const config = statusConfig[job.status] || { icon: AlertCircle, className: "text-muted-foreground", label: "Unknown" };
  const StatusIcon = config.icon;
  const ProviderIcon = providerIcons[job.provider as keyof typeof providerIcons] || Database;
  
  const dateStr = new Date(job.created_at).toLocaleDateString([], { 
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' 
  });
  
  const durationStr = job.duration_ms 
    ? `${(job.duration_ms / 1000).toFixed(1)}s` 
    : (job.status === "RUNNING" ? "Running..." : "-");

  return (
    <div className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors">
      <div className="flex items-center gap-4">
        <div className={cn("flex h-9 w-9 items-center justify-center rounded-full bg-muted/50", config.className)}>
          <StatusIcon className="h-5 w-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <ProviderIcon className="h-3.5 w-3.5 text-muted-foreground" />
            <p className="text-sm font-medium capitalize">{job.provider.replace("_", " ")}</p>
          </div>
          <p className="text-xs text-muted-foreground mt-0.5">{dateStr}</p>
        </div>
      </div>
      
      <div className="flex items-center gap-8 text-right">
        <div className="hidden sm:block">
          <p className="text-sm font-medium">{job.documents_changed} docs changed</p>
          <p className="text-xs text-muted-foreground">Found {job.documents_found}</p>
        </div>
        <div className="w-24">
          <p className={cn("text-sm font-medium", config.className)}>{config.label}</p>
          <p className="text-xs text-muted-foreground">{durationStr}</p>
        </div>
      </div>
    </div>
  );
}
