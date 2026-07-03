import { SearchFilters as SearchFiltersType } from "@/lib/types/search";
import { Filter } from "lucide-react";

interface Props {
  filters: SearchFiltersType;
  onChange: (filters: SearchFiltersType) => void;
}

export function SearchFilters({ filters, onChange }: Props) {
  return (
    <div className="flex flex-wrap items-center gap-4 mt-6">
      <div className="flex items-center gap-2 text-sm font-medium text-muted-foreground mr-2">
        <Filter className="h-4 w-4" />
        Filters:
      </div>
      
      <select 
        value={filters.provider || "all"}
        onChange={(e) => onChange({ ...filters, provider: e.target.value })}
        className="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
      >
        <option value="all">All Sources</option>
        <option value="google_drive">Google Drive</option>
        <option value="notion">Notion</option>
        <option value="slack">Slack</option>
      </select>

      <select 
        value={filters.status || "all"}
        onChange={(e) => onChange({ ...filters, status: e.target.value })}
        className="h-9 rounded-md border border-input bg-background px-3 py-1 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
      >
        <option value="all">Any Status</option>
        <option value="ready">Ready (Retrieval)</option>
        <option value="embedded">Embedded</option>
        <option value="graph_built">Graph Built</option>
      </select>
    </div>
  );
}
