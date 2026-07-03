import { DocumentDetail } from "@/lib/types/documents";
import { Copy, Layers, Link2, GitBranch } from "lucide-react";

interface Props {
  document: DocumentDetail;
}

export function DocumentStatsPanel({ document }: Props) {
  const stats = [
    { label: "Version", value: `v${document.version}`, icon: GitBranch },
    { label: "Chunks", value: document.chunk_count.toLocaleString(), icon: Layers },
    { label: "Knowledge Objects", value: document.knowledge_object_count?.toLocaleString() || "-", icon: Copy },
    { label: "Graph Relations", value: document.graph_relation_count?.toLocaleString() || "-", icon: Link2 },
  ];

  return (
    <div className="grid grid-cols-2 gap-4">
      {stats.map((stat, i) => (
        <div key={i} className="rounded-xl border bg-card p-4 flex flex-col justify-between h-24">
          <div className="flex items-center gap-2 text-muted-foreground">
            <stat.icon className="h-4 w-4" />
            <span className="text-xs font-medium uppercase tracking-wider">{stat.label}</span>
          </div>
          <p className="text-2xl font-semibold">{stat.value}</p>
        </div>
      ))}
    </div>
  );
}
