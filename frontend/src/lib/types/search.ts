export type SearchProvider = "google_drive" | "notion" | "slack" | "upload";

export type SearchResultItem = {
  chunk_id: string;
  document_id: string;
  document_title: string;
  provider: SearchProvider;
  source: string;
  snippet: string;
  score: number;
  section_heading?: string | null;
  page_number?: number | null;
  document_status: string;
};

export type SearchResponse = {
  query: string;
  total: number;
  latency_ms: number;
  results: SearchResultItem[];
};

export type SearchFilters = {
  provider?: string;
  status?: string;
};
