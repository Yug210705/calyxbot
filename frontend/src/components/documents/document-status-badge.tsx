import { DocumentStatus } from "@/lib/types/documents";
import { cn } from "@/lib/utils";

interface BadgeProps {
  status: DocumentStatus;
  className?: string;
}

const statusConfig: Record<DocumentStatus, { label: string; className: string }> = {
  PENDING: { label: "Pending", className: "bg-muted text-muted-foreground border-border" },
  FETCHED: { label: "Fetched", className: "bg-blue-500/10 text-blue-500 border-blue-500/20" },
  NORMALIZED: { label: "Normalized", className: "bg-blue-500/10 text-blue-500 border-blue-500/20" },
  CHUNKED: { label: "Chunked", className: "bg-indigo-500/10 text-indigo-500 border-indigo-500/20" },
  EMBEDDED: { label: "Embedded", className: "bg-purple-500/10 text-purple-500 border-purple-500/20" },
  GRAPH_BUILT: { label: "Graph Built", className: "bg-pink-500/10 text-pink-500 border-pink-500/20" },
  READY: { label: "Ready", className: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" },
  FAILED: { label: "Failed", className: "bg-red-500/10 text-red-500 border-red-500/20" },
};

export function DocumentStatusBadge({ status, className }: BadgeProps) {
  const config = statusConfig[status];
  
  return (
    <span 
      className={cn(
        "inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-semibold whitespace-nowrap",
        config.className,
        className
      )}
    >
      {config.label}
    </span>
  );
}
