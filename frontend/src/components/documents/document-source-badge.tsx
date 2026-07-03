import { Folder, Database, MessageSquare, Upload, File } from "lucide-react";
import { cn } from "@/lib/utils";

interface BadgeProps {
  provider: string;
  sourceLabel: string;
  className?: string;
}

const providerIcons: Record<string, React.ElementType> = {
  google_drive: Folder,
  notion: Database,
  slack: MessageSquare,
  upload: Upload,
};

export function DocumentSourceBadge({ provider, sourceLabel, className }: BadgeProps) {
  const Icon = providerIcons[provider] || File;
  
  return (
    <div className={cn("flex items-center gap-1.5 text-xs text-muted-foreground", className)}>
      <Icon className="h-3 w-3" />
      <span className="truncate max-w-[120px] sm:max-w-[180px]">{sourceLabel}</span>
    </div>
  );
}
