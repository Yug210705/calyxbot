/* eslint-disable react/no-unescaped-entities */
import { SearchX } from "lucide-react";

interface NoResultsProps {
  query: string;
  onClearFilters: () => void;
}

export function SearchNoResultsState({ query, onClearFilters }: NoResultsProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-24 text-center bg-card mt-8">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-muted text-muted-foreground mb-6">
        <SearchX className="h-8 w-8" />
      </div>
      <h3 className="text-xl font-semibold mb-2">No results for &quot;{query}&quot;</h3>
      <p className="text-muted-foreground mb-8 max-w-md">
        We couldn't find any documents, chunks, or extracted knowledge matching your search. Try adjusting your query or filters.
      </p>
      <button 
        onClick={onClearFilters}
        className="rounded-md border bg-background px-6 py-2.5 text-sm font-medium hover:bg-muted transition-colors shadow-sm"
      >
        Clear Filters
      </button>
    </div>
  );
}
