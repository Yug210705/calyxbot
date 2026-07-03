import { useState, useCallback } from "react";
import { SearchResultItem, SearchFilters } from "../types/search";
import { searchMemory } from "../api/search";

export function useSearch(orgId: string | undefined) {
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<SearchFilters>({ provider: "all", status: "all" });
  
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [total, setTotal] = useState(0);
  const [latencyMs, setLatencyMs] = useState<number | undefined>(undefined);
  
  const [selectedResultId, setSelectedResultId] = useState<string | null>(null);
  
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const runSearch = useCallback(async (searchQuery?: string, searchFilters?: SearchFilters) => {
    const q = searchQuery !== undefined ? searchQuery : query;
    const f = searchFilters !== undefined ? searchFilters : filters;

    if (!q.trim()) {
      setResults([]);
      setTotal(0);
      setLatencyMs(undefined);
      setHasSearched(false);
      setSelectedResultId(null);
      return;
    }

    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    
    try {
      const response = await searchMemory(q, f, orgId);
      setResults(response.results);
      setTotal(response.total);
      setLatencyMs(response.latency_ms);
      
      // Auto-select first result if available and we don't have one selected
      if (response.results.length > 0 && !selectedResultId) {
        setSelectedResultId(response.results[0].chunk_id);
      } else if (response.results.length === 0) {
        setSelectedResultId(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Search failed"));
      setResults([]);
      setTotal(0);
      setLatencyMs(undefined);
      setSelectedResultId(null);
    } finally {
      setIsLoading(false);
    }
  }, [query, filters, orgId, selectedResultId]);

  const clearSearch = useCallback(() => {
    setQuery("");
    setFilters({ provider: "all", status: "all" });
    setResults([]);
    setTotal(0);
    setLatencyMs(undefined);
    setHasSearched(false);
    setError(null);
    setSelectedResultId(null);
  }, []);

  return {
    query,
    setQuery,
    filters,
    setFilters,
    results,
    total,
    latencyMs,
    selectedResultId,
    setSelectedResultId,
    isLoading,
    error,
    hasSearched,
    runSearch,
    clearSearch,
  };
}
