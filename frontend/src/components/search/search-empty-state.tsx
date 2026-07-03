import { Search } from "lucide-react";

export function SearchEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-32 text-center bg-card mt-8">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary mb-6">
        <Search className="h-8 w-8" />
      </div>
      <h3 className="text-xl font-semibold mb-2">Search Organizational Memory</h3>
      <p className="text-muted-foreground mb-8 max-w-md">
        Type a query to search across all your connected documents, chunks, and extracted knowledge objects.
      </p>
    </div>
  );
}
