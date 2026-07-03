import { SearchX } from "lucide-react";

interface NoResultsProps {
  onClearFilters: () => void;
}

export function DocumentsNoResultsState({ onClearFilters }: NoResultsProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-16 text-center bg-card">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted text-muted-foreground mb-4">
        <SearchX className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-medium">No documents match your filters</h3>
      <p className="text-sm text-muted-foreground mt-1 mb-6 max-w-sm">
        Try adjusting your search query or removing filters to see more results.
      </p>
      <button 
        onClick={onClearFilters}
        className="rounded-md border bg-background px-4 py-2 text-sm font-medium hover:bg-muted transition-colors shadow-sm"
      >
        Clear Filters
      </button>
    </div>
  );
}
