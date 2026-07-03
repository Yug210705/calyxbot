import { IntegrationProvider, IntegrationConnection, SyncJob } from "../types/integrations";

export const mockAvailableProviders: IntegrationProvider[] = [
  {
    provider: "google_drive",
    name: "Google Drive",
    description: "Sync documents, spreadsheets, and presentations.",
    category: "storage",
    available: true,
  },
  {
    provider: "notion",
    name: "Notion",
    description: "Connect your workspaces and knowledge bases.",
    category: "docs",
    available: true,
  },
  {
    provider: "slack",
    name: "Slack",
    description: "Index channel history and team discussions.",
    category: "chat",
    available: true,
  },
];

export const mockConnectedIntegrations: IntegrationConnection[] = [
  {
    id: "conn-1",
    provider: "google_drive",
    displayName: "Engineering Drive",
    status: "ACTIVE",
    health: "healthy",
    lastSyncAt: new Date(Date.now() - 1000 * 60 * 15).toISOString(), // 15 mins ago
    documentCount: 147,
  }
];

export const mockRecentSyncJobs: SyncJob[] = [
  {
    id: "job-1",
    integration_id: "conn-1",
    provider: "google_drive",
    status: "RUNNING",
    documents_found: 150,
    documents_changed: 42,
    documents_skipped: 0,
    documents_failed: 0,
    bytes_processed: 1234567,
    created_at: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    duration_ms: 0,
  },
  {
    id: "job-2",
    integration_id: "conn-1",
    provider: "google_drive",
    status: "SUCCESS",
    documents_found: 145,
    documents_changed: 105,
    documents_skipped: 40,
    documents_failed: 0,
    bytes_processed: 2234567,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
    finished_at: new Date(Date.now() - 1000 * 60 * 60 * 24 + 45000).toISOString(),
    duration_ms: 45000, // 45 seconds
  },
  {
    id: "job-3",
    integration_id: "conn-slack-1",
    provider: "slack",
    status: "FAILED",
    documents_found: 0,
    documents_changed: 0,
    documents_skipped: 0,
    documents_failed: 0,
    bytes_processed: 0,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
    finished_at: new Date(Date.now() - 1000 * 60 * 60 * 48 + 5000).toISOString(),
    duration_ms: 5000,
    error_message: "Connection refused",
  },
  {
    id: "job-4",
    integration_id: "conn-1",
    provider: "google_drive",
    status: "SUCCESS",
    documents_found: 40,
    documents_changed: 40,
    documents_skipped: 0,
    documents_failed: 0,
    bytes_processed: 334567,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString(),
    started_at: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString(),
    finished_at: new Date(Date.now() - 1000 * 60 * 60 * 72 + 12000).toISOString(),
    duration_ms: 12000,
  }
];
