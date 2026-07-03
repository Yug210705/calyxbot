import { Search } from "lucide-react";

interface Props {
  search: string;
  onSearchChange: (value: string) => void;
  providerFilter: string;
  onProviderChange: (value: string) => void;
  statusFilter: string;
  onStatusChange: (value: string) => void;
}

export function DocumentsFilters({
  search, onSearchChange,
  providerFilter, onProviderChange,
  statusFilter, onStatusChange
}: Props) {
  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center mb-6">
      {/* Search Input */}
      <div className="relative flex-1 max-w-sm">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <input 
          type="text" 
          placeholder="Search documents..." 
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="h-10 w-full rounded-md border border-input bg-background pl-10 pr-4 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
        />
      </div>

      {/* Provider Filter */}
      <select 
        value={providerFilter}
        onChange={(e) => onProviderChange(e.target.value)}
        className="h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <option value="all">All Sources</option>
        <option value="google_drive">Google Drive</option>
        <option value="notion">Notion</option>
        <option value="slack">Slack</option>
        <option value="upload">Uploads</option>
      </select>

      {/* Status Filter */}
      <select 
        value={statusFilter}
        onChange={(e) => onStatusChange(e.target.value)}
        className="h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <option value="all">All Statuses</option>
        <option value="ready">Ready</option>
        <option value="pending">Pending</option>
        <option value="fetched">Fetched</option>
        <option value="normalized">Normalized</option>
        <option value="chunked">Chunked</option>
        <option value="embedded">Embedded</option>
        <option value="indexed">Indexed</option>
        <option value="graph_built">Graph Built</option>
        <option value="failed">Failed</option>
      </select>
    </div>
  );
}
