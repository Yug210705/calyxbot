export type IntegrationStatus = "ACTIVE" | "WARNING" | "ERROR" | "DISCONNECTED" | "AUTH_REQUIRED";
export type IntegrationHealth = "healthy" | "degraded" | "error";

export type IntegrationProvider = {
  provider: "google_drive" | "notion" | "slack";
  name: string;
  description: string;
  category: "storage" | "docs" | "chat";
  available: boolean;
};

export type IntegrationConnection = {
  id: string;
  provider: "google_drive" | string;
  displayName: string;
  status: IntegrationStatus;
  health: IntegrationHealth;
  connectedAt?: string | null;
  lastSyncAt: string | null;
  documentCount: number;
  syncState?: string | null;
};

export type SyncJobStatus = "PENDING" | "RUNNING" | "SUCCESS" | "FAILED";

export type SyncJob = {
  id: string;
  integration_id: string;
  provider: "google_drive" | string;
  status: SyncJobStatus;
  documents_found: number;
  documents_changed: number;
  documents_skipped: number;
  documents_failed: number;
  bytes_processed: number;
  duration_ms: number;
  error_message?: string | null;
  created_at: string;
  started_at?: string | null;
  finished_at?: string | null;
};
