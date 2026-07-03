import { Button } from "@/components/ui/button";
import { FilterX } from "lucide-react";

interface Props {
  total: number;
  latencyMs?: number;
  query: string;
  hasFilters?: boolean;
  onClearFilters?: () => void;
}

export function SearchResultsToolbar({ total, latencyMs, query, hasFilters, onClearFilters }: Props) {
  return (
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between py-2 border-b mb-6 text-sm">
      <div className="text-muted-foreground">
        Found <span className="font-semibold text-foreground">{total}</span> results for{" "}
        <span className="italic font-medium text-foreground">"{query}"</span>
        {latencyMs !== undefined && (
          <span className="text-xs ml-2 opacity-60">in {latencyMs}ms</span>
        )}
      </div>

      {hasFilters && (
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={onClearFilters}
          className="h-8 text-muted-foreground hover:text-foreground mt-2 sm:mt-0"
        >
          <FilterX className="h-4 w-4 mr-2" />
          Clear Filters
        </Button>
      )}
    </div>
  );
}
