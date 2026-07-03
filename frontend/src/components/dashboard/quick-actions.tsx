import Link from "next/link";
import { Plus, Search, FileText } from "lucide-react";

export function QuickActions() {
  return (
    <div className="rounded-xl border bg-card p-6">
      <h3 className="font-medium mb-4">Quick Actions</h3>
      <div className="flex flex-col gap-3">
        <Link 
          href="/integrations" 
          className="flex items-center gap-3 rounded-lg border p-3 hover:bg-muted transition-colors"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
            <Plus className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">Connect Google Drive</p>
            <p className="text-xs text-muted-foreground">Add a new data source</p>
          </div>
        </Link>
        
        <Link 
          href="/documents" 
          className="flex items-center gap-3 rounded-lg border p-3 hover:bg-muted transition-colors"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
            <FileText className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">View Documents</p>
            <p className="text-xs text-muted-foreground">Browse synced content</p>
          </div>
        </Link>

        <Link 
          href="/search" 
          className="flex items-center gap-3 rounded-lg border p-3 hover:bg-muted transition-colors"
        >
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
            <Search className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">Search Memory</p>
            <p className="text-xs text-muted-foreground">Query your organization data</p>
          </div>
        </Link>
      </div>
    </div>
  );
}
