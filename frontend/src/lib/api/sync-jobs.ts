import { apiFetch } from "./client";
import { SyncJob } from "../types/integrations";

export async function triggerIntegrationSync(integrationId: string): Promise<SyncJob> {
  return apiFetch<SyncJob>(`/integrations/${integrationId}/sync`, {
    method: "POST",
  });
}

export async function getSyncJobs(): Promise<SyncJob[]> {
  return apiFetch<SyncJob[]>("/integrations/jobs");
}

export async function getSyncJob(jobId: string): Promise<SyncJob> {
  return apiFetch<SyncJob>(`/integrations/jobs/${jobId}`);
}
