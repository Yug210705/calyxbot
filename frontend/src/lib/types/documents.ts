export type DocumentStatus =
  | "PENDING"
  | "FETCHED"
  | "NORMALIZED"
  | "CHUNKED"
  | "EMBEDDED"
  | "GRAPH_BUILT"
  | "READY"
  | "FAILED";

export type ProcessingTimelineItem = {
  key: string;
  label: string;
  status: "completed" | "current" | "pending" | "failed";
  timestamp: string | null;
};

export type DocumentListItem = {
  id: string;
  title: string;
  provider: string;
  source: string | null;
  mime_type: string;
  status: DocumentStatus;
  version: number;
  chunk_count: number;
  updated_at: string;
  last_synced_at: string | null;
  knowledge_object_count?: number;
};

export type DocumentDetail = DocumentListItem & {
  checksum: string;
  created_at: string;
  processing_timeline: ProcessingTimelineItem[];
  graph_relation_count?: number;
  page_count?: number | null;
  section_count?: number | null;
};

export type DocumentListResponse = {
  items: DocumentListItem[];
  total: number;
  page: number;
  size: number;
};
