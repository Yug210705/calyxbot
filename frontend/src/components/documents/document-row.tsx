/* eslint-disable react-hooks/static-components */
import { DocumentListItem } from "@/lib/types/documents";
import { DocumentStatusBadge } from "./document-status-badge";
import { DocumentSourceBadge } from "./document-source-badge";
import { FileText, Image, FileJson, Layout, FileType2, ChevronRight } from "lucide-react";

interface Props {
  document: DocumentListItem;
  onClick: (id: string) => void;
}

const getMimeIcon = (mimeType: string) => {
  if (mimeType.includes("image")) return Image;
  if (mimeType.includes("json")) return FileJson;
  if (mimeType.includes("spreadsheet") || mimeType.includes("excel")) return Layout;
  if (mimeType.includes("presentation")) return FileType2;
  return FileText; // Default
};

const formatTimeAgo = (dateStr: string) => {
  const date = new Date(dateStr);
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000);
  
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
};

export function DocumentRow({ document, onClick }: Props) {
  const MimeIcon = getMimeIcon(document.mime_type);

  return (
    <div 
      onClick={() => onClick(document.id)}
      className="flex items-center justify-between p-4 hover:bg-muted/50 transition-colors cursor-pointer group"
    >
      <div className="flex items-start gap-4 min-w-0 flex-1">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted/50 mt-0.5">
          <MimeIcon className="h-5 w-5 text-muted-foreground" />
        </div>
        <div className="min-w-0 pr-4">
          <h4 className="text-sm font-medium truncate group-hover:text-primary transition-colors">
            {document.title}
          </h4>
          <div className="mt-1 flex items-center gap-3">
            <DocumentSourceBadge 
              provider={document.provider} 
              sourceLabel={document.source || document.provider} 
            />
            <span className="hidden sm:inline text-xs text-muted-foreground/50">•</span>
            <span className="hidden sm:inline text-xs text-muted-foreground truncate">
              {document.mime_type.split('/').pop()}
            </span>
          </div>
        </div>
      </div>
      
      <div className="flex items-center gap-6 text-right shrink-0">
        <div className="hidden lg:block w-24">
          <DocumentStatusBadge status={document.status} />
        </div>
        
        <div className="hidden md:block w-16 text-center">
          <p className="text-sm font-medium">v{document.version}</p>
        </div>
        
        <div className="hidden sm:block w-16 text-center">
          <p className="text-sm font-medium">{document.chunk_count}</p>
          <p className="text-[10px] text-muted-foreground uppercase">Chunks</p>
        </div>
        
        <div className="w-20 text-right">
          <p className="text-sm text-muted-foreground">{formatTimeAgo(document.updated_at)}</p>
        </div>
        
        <div className="w-6 flex justify-end">
          <ChevronRight className="h-5 w-5 text-muted-foreground opacity-50 group-hover:opacity-100 transition-opacity" />
        </div>
      </div>
    </div>
  );
}
