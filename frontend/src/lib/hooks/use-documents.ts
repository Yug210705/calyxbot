import { useState, useEffect, useCallback, useRef } from "react";
import { DocumentListItem } from "../types/documents";
import { getDocuments } from "../api/documents";

export function useDocuments(orgId: string | undefined) {
  const [documents, setDocuments] = useState<DocumentListItem[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  // Filters
  const [search, setSearch] = useState("");
  const [providerFilter, setProviderFilter] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  
  // Debounce search state to avoid too many API calls while typing
  const [debouncedSearch, setDebouncedSearch] = useState("");
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(search);
    }, 300);
    return () => clearTimeout(handler);
  }, [search]);

  const fetchDocuments = useCallback(async () => {
    if (!orgId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const data = await getDocuments(orgId, {
        q: debouncedSearch || undefined,
        provider: providerFilter,
        status: statusFilter,
        limit: 50
      });
      setDocuments(data.items);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to load documents"));
    } finally {
      setIsLoading(false);
    }
  }, [orgId, debouncedSearch, providerFilter, statusFilter]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  return {
    documents,
    filteredDocuments: documents, // keeping this property to satisfy page.tsx without huge refactor
    total,
    search,
    providerFilter,
    statusFilter,
    setSearch,
    setProviderFilter,
    setStatusFilter,
    isLoading,
    error,
    refresh: fetchDocuments,
  };
}
