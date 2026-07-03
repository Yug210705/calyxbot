import { SearchResultItem } from "@/lib/types/search";
import { Hash, FileIcon } from "lucide-react";
import { HighlightedSnippet } from "./highlighted-snippet";

interface Props {
  result: SearchResultItem;
  query?: string;
}

export function SearchResultPreview({ result, query = "" }: Props) {
  return (
    <div className="rounded-xl border bg-card overflow-hidden">
      <div className="border-b px-6 py-4 bg-muted/20 flex items-center justify-between">
        <h3 className="text-sm font-semibold">Matched Content</h3>
        <div className="flex gap-3">
          {result.section_heading && (
            <div className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
              <Hash className="h-3.5 w-3.5" />
              <span>{result.section_heading}</span>
            </div>
          )}
          {result.page_number && (
            <div className="flex items-center gap-1 text-xs font-medium text-muted-foreground">
              <FileIcon className="h-3.5 w-3.5" />
              <span>Page {result.page_number}</span>
            </div>
          )}
        </div>
      </div>
      <div className="p-6">
        <div className="relative text-sm font-mono text-muted-foreground whitespace-pre-wrap leading-relaxed">
          <HighlightedSnippet text={result.snippet} query={query} />
        </div>
      </div>
    </div>
  );
}
