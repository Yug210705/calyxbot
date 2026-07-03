import { DashboardActivityItem } from "@/lib/types/dashboard";
import { formatDistanceToNow } from "date-fns";
import { Activity, Database, CheckCircle2, AlertTriangle, FileText, Info } from "lucide-react";

interface Props {
  activities: DashboardActivityItem[];
}

export function ActivityFeed({ activities }: Props) {
  if (activities.length === 0) {
    return (
      <div className="rounded-xl border bg-card text-card-foreground shadow-sm flex flex-col p-6 items-center text-center">
        <Activity className="h-8 w-8 text-muted-foreground mb-4 opacity-50" />
        <h3 className="font-medium">No recent activity</h3>
        <p className="text-sm text-muted-foreground mt-1">Activities will appear here once you connect a source and sync documents.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
      <div className="p-6 pb-4">
        <h3 className="font-semibold leading-none tracking-tight">Recent Activity</h3>
      </div>
      <div className="p-6 pt-0">
        <div className="space-y-6">
          {activities.map((activity) => (
            <div key={activity.id} className="flex gap-4">
              <div className="mt-0.5">
                <ActivityIcon type={activity.type} />
              </div>
              <div className="flex-1 space-y-1">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium leading-none">{activity.title}</p>
                  <p className="text-xs text-muted-foreground">
                    {formatDistanceToNow(new Date(activity.created_at), { addSuffix: true })}
                  </p>
                </div>
                {activity.description && (
                  <p className="text-sm text-muted-foreground">{activity.description}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ActivityIcon({ type }: { type: DashboardActivityItem["type"] }) {
  switch (type) {
    case "sync_success": return <CheckCircle2 className="h-4 w-4 text-green-500" />;
    case "sync_failed": return <AlertTriangle className="h-4 w-4 text-red-500" />;
    case "document_added": return <FileText className="h-4 w-4 text-blue-500" />;
    case "document_updated": return <Database className="h-4 w-4 text-amber-500" />;
    default: return <Info className="h-4 w-4 text-muted-foreground" />;
  }
}
