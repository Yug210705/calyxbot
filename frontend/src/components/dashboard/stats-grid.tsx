import { Database, FileText, Share2, Clock } from "lucide-react";
import { StatCard } from "./stat-card";
import { DashboardStats } from "@/lib/types/dashboard";

interface StatsGridProps {
  stats: DashboardStats;
}

export function StatsGrid({ stats }: StatsGridProps) {
  // Format the date nicely if it exists
  const lastSyncStr = stats.last_sync_at 
    ? new Date(stats.last_sync_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
    : "Never";

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard
        title="Connected Sources"
        value={stats.connected_sources}
        icon={Share2}
        subtext="Active integrations"
      />
      <StatCard
        title="Documents"
        value={stats.documents_total.toLocaleString()}
        icon={FileText}
        subtext="Synced and normalized"
      />
      <StatCard
        title="Knowledge Objects"
        value={stats.knowledge_objects_total.toLocaleString()}
        icon={Database}
        subtext="Chunks & entities extracted"
      />
      <StatCard
        title="Last Sync"
        value={lastSyncStr}
        icon={Clock}
        subtext="Across all sources"
      />
    </div>
  );
}
