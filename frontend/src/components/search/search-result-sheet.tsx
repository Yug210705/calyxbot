import { useEffect } from "react";
import { SearchResultItem } from "@/lib/types/search";
import { SearchScoreBadge } from "./search-score-badge";
import { SearchSourceBadge } from "./search-source-badge";
import { SearchResultPreview } from "./search-result-preview";
import { SearchResultMetadata } from "./search-result-metadata";
import { SearchResultActions } from "./search-result-actions";
import { X, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

interface Props {
  result: SearchResultItem | null;
  isOpen: boolean;
  query: string;
  onClose: () => void;
}

export function SearchResultSheet({ result, isOpen, query, onClose }: Props) {
  useEffect(() => {
    if (isOpen) {
      window.document.body.style.overflow = "hidden";
    } else {
      window.document.body.style.overflow = "auto";
    }
    return () => {
      window.document.body.style.overflow = "auto";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <>
      <div 
        className={cn(
          "fixed inset-0 z-50 bg-background/80 backdrop-blur-sm transition-opacity duration-300 xl:hidden",
          isOpen ? "opacity-100" : "opacity-0"
        )}
        onClick={onClose}
      />
      
      <div 
        className={cn(
          "fixed inset-y-0 right-0 z-50 w-full max-w-2xl border-l bg-background shadow-2xl transition-transform duration-300 ease-in-out xl:static xl:translate-x-0 xl:shadow-none xl:border-l xl:z-0 xl:w-full",
          isOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex items-start justify-between border-b px-6 py-4 shrink-0">
            <div className="pr-6 min-w-0">
              {result ? (
                <>
                  <h2 className="text-xl font-bold truncate leading-tight mb-2">
                    {result.document_title}
                  </h2>
                  <div className="flex items-center gap-3">
                    <SearchScoreBadge score={result.score} />
                    <SearchSourceBadge provider={result.provider} sourceLabel={result.source} />
                  </div>
                </>
              ) : null}
            </div>
            <button 
              onClick={onClose}
              className="rounded-full p-2 hover:bg-muted transition-colors xl:hidden"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Scrollable Content */}
          <div className="flex-1 overflow-y-auto px-6 py-6">
            {result ? (
              <div className="space-y-6 pb-12">
                <div className="flex justify-end">
                  <SearchResultActions result={result} />
                </div>
                <SearchResultPreview result={result} query={query} />
                <SearchResultMetadata result={result} />
                
                <div className="pt-4 border-t">
                  {/* Note: This assumes /documents is built to handle deep linking via ID eventually, 
                      or just navigates to the list for now. */}
                  <Link 
                    href="/documents"
                    className="inline-flex items-center justify-center gap-2 rounded-md bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 transition-colors w-full"
                  >
                    View Full Document details
                    <ExternalLink className="h-4 w-4" />
                  </Link>
                </div>
              </div>
            ) : (
              <div className="flex h-full items-center justify-center text-muted-foreground text-sm">
                Select a result to preview its contents.
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
