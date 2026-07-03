import { SystemStatus } from "@/lib/types/system";
import { AlertCircle, AlertTriangle, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface Props {
  status: SystemStatus;
}

export function SystemStatusBanner({ status }: Props) {
  let bgColor = "bg-primary/10";
  let textColor = "text-primary";
  let Icon = CheckCircle2;
  
  if (status.mode === "demo") {
    bgColor = "bg-amber-500/15";
    textColor = "text-amber-600 dark:text-amber-500";
    Icon = AlertTriangle;
  } else if (status.mode === "degraded") {
    bgColor = "bg-red-500/15";
    textColor = "text-red-600 dark:text-red-500";
    Icon = AlertCircle;
  }

  return (
    <div className={cn("w-full px-6 py-2 flex items-center gap-2 text-sm font-medium border-b", bgColor, textColor)}>
      <Icon className="h-4 w-4 shrink-0" />
      <span className="flex-1 truncate">
        {status.message}
        {status.lastSyncLabel && ` • Last sync: ${status.lastSyncLabel}`}
      </span>
    </div>
  );
}
