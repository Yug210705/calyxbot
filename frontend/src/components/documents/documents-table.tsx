import { DocumentListItem } from "@/lib/types/documents";
import { DocumentRow } from "./document-row";

interface Props {
  documents: DocumentListItem[];
  onDocumentClick: (id: string) => void;
}

export function DocumentsTable({ documents, onDocumentClick }: Props) {
  return (
    <div className="rounded-xl border bg-card overflow-hidden">
      <div className="hidden sm:flex items-center justify-between px-4 py-3 border-b bg-muted/20 text-xs font-medium text-muted-foreground uppercase tracking-wider">
        <div className="flex-1 pl-14">Document</div>
        <div className="flex items-center gap-6 text-right pr-6">
          <div className="hidden lg:block w-24 text-center">Status</div>
          <div className="hidden md:block w-16 text-center">Version</div>
          <div className="hidden sm:block w-16 text-center">Chunks</div>
          <div className="w-20 text-right">Updated</div>
        </div>
      </div>
      <div className="divide-y">
        {documents.map((doc) => (
          <DocumentRow 
            key={doc.id} 
            document={doc} 
            onClick={onDocumentClick}
          />
        ))}
      </div>
    </div>
  );
}
