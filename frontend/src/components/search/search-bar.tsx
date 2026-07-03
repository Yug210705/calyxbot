import { Search, X, Loader2 } from "lucide-react";

interface Props {
  query: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  onClear: () => void;
  isLoading: boolean;
}

export function SearchBar({ query, onChange, onSubmit, onClear, isLoading }: Props) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      onSubmit();
    }
  };

  return (
    <div className="relative flex items-center w-full max-w-4xl shadow-sm rounded-full bg-card border overflow-hidden focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-2 transition-all">
      <div className="pl-6 pr-2 text-primary">
        <Search className="h-6 w-6" />
      </div>
      <input 
        type="text" 
        value={query}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question or search for concepts..." 
        className="h-14 w-full bg-transparent px-4 py-2 text-lg outline-none placeholder:text-muted-foreground"
      />
      
      <div className="flex items-center gap-2 pr-4">
        {query && (
          <button 
            onClick={onClear}
            className="p-2 text-muted-foreground hover:text-foreground hover:bg-muted rounded-full transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        )}
        
        <button 
          onClick={onSubmit}
          disabled={isLoading || !query.trim()}
          className="rounded-full bg-primary px-6 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
        >
          {isLoading ? (
            <span className="flex items-center gap-2"><Loader2 className="h-4 w-4 animate-spin" /> Searching</span>
          ) : (
            "Search"
          )}
        </button>
      </div>
    </div>
  );
}
