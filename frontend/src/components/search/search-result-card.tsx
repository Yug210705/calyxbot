import { SearchResultItem } from "@/lib/types/search";
import { SearchScoreBadge } from "./search-score-badge";
import { SearchSourceBadge } from "./search-source-badge";
import { FileText, Hash, FileIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { HighlightedSnippet } from "./highlighted-snippet";

interface Props {
  result: SearchResultItem;
  isSelected: boolean;
  query: string;
  onClick: () => void;
}

const formatTimeAgo = (dateStr?: string) => {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  const days = Math.floor((new Date().getTime() - date.getTime()) / 86400000);
  if (days === 0) return "Today";
  if (days === 1) return "Yesterday";
  return `${days}d ago`;
};

export function SearchResultCard({ result, isSelected, query, onClick }: Props) {
  return (
    <div 
      onClick={onClick}
      className={cn(
        "flex flex-col gap-3 rounded-xl border bg-card p-5 cursor-pointer transition-all hover:shadow-md",
        isSelected ? "border-primary ring-1 ring-primary" : "hover:border-primary/50"
      )}
    >
      {/* Top Row */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-2 min-w-0">
          <FileText className="h-4 w-4 text-primary shrink-0" />
          <h4 className="font-semibold text-foreground truncate">{result.document_title}</h4>
        </div>
        <div className="shrink-0">
          <SearchScoreBadge score={result.score} />
        </div>
      </div>

      {/* Second Row */}
      <div className="flex flex-wrap items-center gap-2">
        <SearchSourceBadge provider={result.provider} sourceLabel={result.source} />
        
        {result.section_heading && (
          <div className="flex items-center gap-1 text-xs text-muted-foreground bg-muted/30 px-2 py-1 rounded">
            <Hash className="h-3 w-3" />
            <span className="truncate max-w-[150px]">{result.section_heading}</span>
          </div>
        )}
        
        {result.page_number && (
          <div className="flex items-center gap-1 text-xs text-muted-foreground bg-muted/30 px-2 py-1 rounded">
            <FileIcon className="h-3 w-3" />
            <span>Page {result.page_number}</span>
          </div>
        )}
      </div>

      {/* Main Body Preview */}
      <div className="mt-1 relative">
        <HighlightedSnippet 
          text={result.snippet}
          query={query}
          className="text-sm text-muted-foreground line-clamp-3 leading-relaxed" 
        />
      </div>

      {/* Footer */}
      <div className="mt-2 flex items-center gap-4 text-xs text-muted-foreground/70">
        <span className="capitalize">{result.document_status.toLowerCase()}</span>
      </div>
    </div>
  );
}
