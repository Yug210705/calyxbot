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

export function SearchSourceBadge({ provider, sourceLabel, className }: BadgeProps) {
  const Icon = providerIcons[provider] || File;
  
  return (
    <div className={cn("inline-flex items-center gap-1.5 rounded bg-muted/50 px-2 py-1 text-xs text-muted-foreground", className)}>
      <Icon className="h-3 w-3" />
      <span className="truncate max-w-[150px] font-medium">{sourceLabel}</span>
    </div>
  );
}
