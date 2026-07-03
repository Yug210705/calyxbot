import { DashboardResponse } from "../types/dashboard";

export const mockDashboardData: DashboardResponse = {
  stats: {
    connected_sources: 1,
    documents_total: 147,
    knowledge_objects_total: 2890,
    last_sync_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(), // 15 mins ago
  },
  activity: [
    {
      id: "act-1",
      title: "Google Drive sync completed",
      description: "142 documents indexed from Product Specs",
      created_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
      type: "sync_success",
      status: "success",
    },
    {
      id: "act-2",
      title: "Search index updated",
      description: "Embeddings generated for onboarding docs",
      created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      type: "document_updated",
      status: "info",
    },
    {
      id: "act-3",
      title: "2 documents failed processing",
      description: "PDF parse errors in Q1_Report.pdf",
      created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
      type: "sync_failed",
      status: "error",
    }
  ],
  checklist: [
    {
      id: "chk-1",
      label: "Connect your first source",
      completed: true,
      href: "/integrations",
    },
    {
      id: "chk-2",
      label: "Run your first sync",
      completed: true,
      href: "/integrations",
    },
    {
      id: "chk-3",
      label: "Review ingested documents",
      completed: false,
      href: "/documents",
    },
    {
      id: "chk-4",
      label: "Ask Calyx a question in Search",
      completed: false,
      href: "/search",
    }
  ],
  system_health: {
    mode: "demo",
    activeSources: "1",
    documentsIndexedToday: "142",
    lastSyncLabel: "15 minutes ago",
  }
};
