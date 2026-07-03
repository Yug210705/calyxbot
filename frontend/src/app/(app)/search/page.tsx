"use client";

import { useState } from "react";
import { useSearch } from "@/lib/hooks/use-search";
import { SearchResultItem } from "@/lib/types/search";

import { SearchHeader } from "@/components/search/search-header";
import { SearchBar } from "@/components/search/search-bar";
import { SearchFilters } from "@/components/search/search-filters";
import { SearchSuggestions } from "@/components/search/search-suggestions";

import { SearchResultsList } from "@/components/search/search-results-list";
import { SearchResultSheet } from "@/components/search/search-result-sheet";
import { SearchResultsToolbar } from "@/components/search/search-results-toolbar";

import { SearchEmptyState } from "@/components/search/search-empty-state";
import { SearchLoadingState } from "@/components/search/search-loading-state";
import { SearchNoResultsState } from "@/components/search/search-no-results-state";
import { SearchErrorState } from "@/components/search/search-error-state";

export default function SearchPage() {
  const orgId = "mock-org-id";

  const {
    query,
    setQuery,
    filters,
    setFilters,
    results,
    total,
    latencyMs,
    isLoading,
    error,
    hasSearched,
    runSearch,
    clearSearch,
  } = useSearch(orgId);

  const [selectedResult, setSelectedResult] = useState<SearchResultItem | null>(null);
  const [isSheetOpen, setIsSheetOpen] = useState(false);

  const handleSearchSubmit = () => {
    setSelectedResult(null); // Reset selection on new search
    runSearch();
  };

  const handleSuggestionSelect = (suggestion: string) => {
    setQuery(suggestion);
    setSelectedResult(null);
    runSearch(suggestion);
  };

  const handleResultSelect = (result: SearchResultItem) => {
    setSelectedResult(result);
    // On mobile, clicking a result should also open the sheet
    setIsSheetOpen(true);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-theme(spacing.16))] pb-8 overflow-hidden">
      
      {/* Top Section: Header, Search Bar, Filters */}
      <div className="flex-none pt-2 pb-6 shrink-0">
        <SearchHeader />
        
        <SearchBar 
          query={query}
          onChange={setQuery}
          onSubmit={handleSearchSubmit}
          onClear={clearSearch}
          isLoading={isLoading}
        />
        
        {hasSearched && !isLoading && (
          <SearchFilters 
            filters={filters}
            onChange={(newFilters) => {
              setFilters(newFilters);
              // Automatically re-run search with new filters
              runSearch(query, newFilters);
            }}
          />
        )}
      </div>

      {/* Main Body Section */}
      <div className="flex-1 overflow-hidden relative">
        {/* State 1: Before any search */}
        {!hasSearched && !isLoading && (
          <div className="h-full overflow-y-auto pb-12">
            <SearchEmptyState />
            <SearchSuggestions onSelect={handleSuggestionSelect} />
          </div>
        )}

        {/* State 2: Loading */}
        {isLoading && (
          <div className="h-full overflow-y-auto pb-12">
            <SearchLoadingState />
          </div>
        )}

        {/* State 3: Error */}
        {error && !isLoading && (
          <div className="h-full overflow-y-auto pb-12">
            <SearchErrorState 
              message={error.message} 
              onRetry={handleSearchSubmit} 
            />
          </div>
        )}

        {/* State 4: Search Success but 0 results */}
        {hasSearched && !isLoading && !error && results.length === 0 && (
          <div className="h-full overflow-y-auto pb-12">
            <SearchNoResultsState 
              query={query} 
              onClearFilters={() => {
                const cleared = { provider: "all", status: "all" };
                setFilters(cleared);
                runSearch(query, cleared);
              }}
            />
          </div>
        )}

        {/* State 5: Results */}
        {hasSearched && !isLoading && !error && results.length > 0 && (
          <div className="flex h-full xl:gap-8">
            
            {/* Left Column: Results List */}
            <div className="flex-1 overflow-y-auto pb-12 pr-2">
              <div className="max-w-4xl">
                <SearchResultsToolbar 
                  total={total}
                  latencyMs={latencyMs}
                  query={query}
                  hasFilters={filters.provider !== "all" || filters.status !== "all"}
                  onClearFilters={() => {
                    const cleared = { provider: "all", status: "all" };
                    setFilters(cleared);
                    runSearch(query, cleared);
                  }}
                />
                <SearchResultsList 
                  results={results}
                  selectedId={selectedResult?.chunk_id || null}
                  query={query}
                  onSelectResult={handleResultSelect}
                />
              </div>
            </div>

            {/* Right Column (Desktop) / Sheet (Mobile): Result Detail */}
            <SearchResultSheet 
              result={selectedResult}
              query={query}
              isOpen={isSheetOpen || (selectedResult !== null)} // Always "open" on desktop if something is selected
              onClose={() => {
                setIsSheetOpen(false);
                // On desktop, we might also want to clear selection to close it visually
                // if we are simulating the slide-away behavior. 
                // For now, let's keep it selected on desktop unless explicitly cleared.
              }}
            />

          </div>
        )}
      </div>

    </div>
  );
}
