import { IntegrationHealth } from "@/lib/types/integrations";
import { cn } from "@/lib/utils";
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle } from "lucide-react";

interface BadgeProps {
  health: IntegrationHealth;
}

const healthConfig = {
  healthy: { icon: CheckCircle2, className: "text-emerald-500", label: "Healthy" },
  degraded: { icon: AlertTriangle, className: "text-yellow-500", label: "Degraded" },
  error: { icon: XCircle, className: "text-red-500", label: "Failing" },
  unknown: { icon: HelpCircle, className: "text-muted-foreground", label: "Unknown" },
};

export function IntegrationHealthBadge({ health }: BadgeProps) {
  const config = healthConfig[health as keyof typeof healthConfig] || healthConfig.unknown;
  const Icon = config.icon;

  return (
    <div className="flex items-center gap-1.5 text-xs font-medium text-muted-foreground">
      <Icon className={cn("h-3.5 w-3.5", config.className)} />
      <span>{config.label}</span>
    </div>
  );
}
