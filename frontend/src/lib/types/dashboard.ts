export type DashboardStats = {
  connected_sources: number
  documents_total: number
  knowledge_objects_total: number
  last_sync_at: string | null
}

export type DashboardActivityItem = {
  id: string
  type: "sync_success" | "sync_failed" | "document_added" | "document_updated"
  title: string
  description: string
  created_at: string
  status?: string | null
}

export type DashboardChecklistItem = {
  id: string
  label: string
  description?: string
  completed: boolean
  href?: string | null
}

export type DashboardResponse = {
  stats: DashboardStats
  activity: DashboardActivityItem[]
  checklist: DashboardChecklistItem[]
  system_health: Record<string, string>
}
