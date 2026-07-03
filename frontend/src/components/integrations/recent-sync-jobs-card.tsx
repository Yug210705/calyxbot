import { SyncJob } from "@/lib/types/integrations";
import { SyncJobRow } from "./sync-job-row";

interface RecentSyncJobsCardProps {
  jobs: SyncJob[];
}

export function RecentSyncJobsCard({ jobs }: RecentSyncJobsCardProps) {
  if (jobs.length === 0) {
    return (
      <div className="flex flex-col rounded-xl border bg-card p-6">
        <h3 className="font-semibold text-lg mb-4">Recent Sync Jobs</h3>
        <div className="flex h-32 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground">
          No recent sync jobs across your integrations.
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col rounded-xl border bg-card overflow-hidden">
      <div className="border-b px-6 py-4 bg-muted/20">
        <h3 className="font-semibold text-lg">Recent Sync Jobs</h3>
      </div>
      <div className="divide-y">
        {jobs.map((job) => (
          <SyncJobRow key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}
