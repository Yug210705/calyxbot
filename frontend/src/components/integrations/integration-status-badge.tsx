import { IntegrationStatus } from "@/lib/types/integrations";
import { cn } from "@/lib/utils";

interface BadgeProps {
  status: IntegrationStatus;
}

const statusStyles: Record<IntegrationStatus, string> = {
  ACTIVE: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
  WARNING: "bg-yellow-500/10 text-yellow-500 border-yellow-500/20",
  ERROR: "bg-red-500/10 text-red-500 border-red-500/20",
  DISCONNECTED: "bg-muted text-muted-foreground border-border",
  AUTH_REQUIRED: "bg-orange-500/10 text-orange-500 border-orange-500/20",
};

export function IntegrationStatusBadge({ status }: BadgeProps) {
  return (
    <span 
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold capitalize",
        statusStyles[status]
      )}
    >
      {status.toLowerCase().replace('_', ' ')}
    </span>
  );
}
