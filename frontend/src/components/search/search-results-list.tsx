import { SearchResultItem } from "@/lib/types/search";
import { SearchResultCard } from "./search-result-card";

interface Props {
  results: SearchResultItem[];
  selectedId: string | null;
  query: string;
  onSelectResult: (result: SearchResultItem) => void;
}

export function SearchResultsList({ results, selectedId, query, onSelectResult }: Props) {
  return (
    <div className="flex flex-col gap-4">
      {results.map((result) => (
        <SearchResultCard 
          key={result.chunk_id}
          result={result}
          isSelected={selectedId === result.chunk_id}
          query={query}
          onClick={() => onSelectResult(result)}
        />
      ))}
    </div>
  );
}
