import { useEffect, useState } from "react";
import { DocumentDetail } from "@/lib/types/documents";
import { DocumentStatusBadge } from "./document-status-badge";
import { DocumentProcessingTimeline } from "./document-processing-timeline";
import { DocumentStatsPanel } from "./document-stats-panel";
import { DocumentMetadataPanel } from "./document-metadata-panel";
import { X, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface Props {
  document: DocumentDetail | null;
  isOpen: boolean;
  onClose: () => void;
  isLoading: boolean;
}

export function DocumentDetailSheet({ document, isOpen, onClose, isLoading }: Props) {
  // Prevent scrolling on body when sheet is open
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
      {/* Backdrop */}
      <div 
        className={cn(
          "fixed inset-0 z-50 bg-background/80 backdrop-blur-sm transition-opacity duration-300",
          isOpen ? "opacity-100" : "opacity-0"
        )}
        onClick={onClose}
      />
      
      {/* Sheet */}
      <div 
        className={cn(
          "fixed inset-y-0 right-0 z-50 w-full max-w-2xl border-l bg-background shadow-2xl transition-transform duration-300 ease-in-out sm:w-[500px] md:w-[600px]",
          isOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        {/* Header */}
        <div className="flex items-start justify-between border-b px-6 py-4">
          <div className="pr-6">
            {isLoading ? (
              <div className="h-6 w-48 rounded bg-muted animate-pulse mb-2" />
            ) : document ? (
              <h2 className="text-xl font-bold">{document.title}</h2>
            ) : null}
            
            <div className="mt-2 flex items-center gap-3">
              {isLoading ? (
                <div className="h-5 w-20 rounded-full bg-muted animate-pulse" />
              ) : document ? (
                <DocumentStatusBadge status={document.status} />
              ) : null}
            </div>
          </div>
          <button 
            onClick={onClose}
            className="rounded-full p-2 hover:bg-muted transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="h-[calc(100vh-85px)] overflow-y-auto px-6 py-6">
          {isLoading ? (
            <div className="flex h-full items-center justify-center">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : document ? (
            <div className="space-y-8 pb-12">
              {/* Section 2: Key Stats */}
              <section>
                <DocumentStatsPanel document={document} />
              </section>



              {/* Section 5: Processing Timeline */}
              <section>
                <DocumentProcessingTimeline timeline={document.processing_timeline} />
              </section>

              {/* Section 3: Metadata */}
              <section>
                <DocumentMetadataPanel document={document} />
              </section>
            </div>
          ) : (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              Document not found.
            </div>
          )}
        </div>
      </div>
    </>
  );
}
