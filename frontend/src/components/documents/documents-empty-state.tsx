import { FileText } from "lucide-react";
import Link from "next/link";

export function DocumentsEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-24 text-center bg-card">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary mb-6">
        <FileText className="h-8 w-8" />
      </div>
      <h3 className="text-xl font-semibold mb-2">No Documents Found</h3>
      <p className="text-muted-foreground mb-8 max-w-md">
        Your organization's memory is empty. Connect a data source to start indexing your knowledge.
      </p>
      <Link 
        href="/integrations"
        className="rounded-md bg-primary px-6 py-2.5 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors shadow-sm"
      >
        Connect Data Source
      </Link>
    </div>
  );
}
