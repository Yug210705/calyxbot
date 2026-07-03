/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { apiFetch, ApiError } from "./client";
import { SearchResponse, SearchFilters } from "../types/search";
import { getMockSearchResults } from "../mocks/search";

import { shouldFallbackToMock } from "./fallback";

const USE_UI_MOCKS = process.env.NEXT_PUBLIC_USE_UI_MOCKS === "true";

export async function searchMemory(query: string, filters?: SearchFilters, orgId?: string): Promise<SearchResponse> {
  if (!query.trim()) {
    return { query, total: 0, latency_ms: 0, results: [] };
  }

  if (USE_UI_MOCKS) {
    await new Promise((resolve) => setTimeout(resolve, 800));
    let mockResults = getMockSearchResults(query);
    if (filters?.provider && filters.provider !== "all") {
      mockResults = mockResults.filter(r => r.provider === filters.provider);
    }
    if (filters?.status && filters.status !== "all") {
      mockResults = mockResults.filter(r => r.document_status === filters.status);
    }
    return {
      query,
      total: mockResults.length,
      latency_ms: Math.floor(Math.random() * 80) + 40,
      results: mockResults,
    };
  }

  try {
    const payload = {
      query,
      top_k: 20,
      provider: filters?.provider && filters.provider !== "all" ? filters.provider : null,
      status: filters?.status && filters.status !== "all" ? filters.status : null,
    };

    const response = await apiFetch<SearchResponse>("/search", { 
      method: "POST",
      body: JSON.stringify(payload),
      organizationId: orgId || "mock-org-id" 
    });
    
    return response;
  } catch (error: any) {
    if (USE_UI_MOCKS || shouldFallbackToMock(error)) {
      console.warn("Real Search API unavailable (5xx/Network), falling back to mock data", error);
      
      let mockResults = getMockSearchResults(query);
      if (filters?.provider && filters.provider !== "all") {
        mockResults = mockResults.filter(r => r.provider === filters.provider);
      }
      if (filters?.status && filters.status !== "all") {
        mockResults = mockResults.filter(r => r.document_status === filters.status);
      }

      return {
        query,
        total: mockResults.length,
        latency_ms: Math.floor(Math.random() * 80) + 40,
        results: mockResults,
      };
    }
    
    // For 4xx errors, we should NOT fallback. Propagate the error so UI shows error state.
    throw error;
  }
}
