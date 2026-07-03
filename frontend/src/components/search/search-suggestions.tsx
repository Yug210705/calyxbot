import { ArrowRight } from "lucide-react";

interface Props {
  onSelect: (query: string) => void;
}

export function SearchSuggestions({ onSelect }: Props) {
  const suggestions = [
    "Sprint planning notes",
    "Incident response process",
    "Onboarding handbook",
    "Customer escalation",
    "Hiring scorecard",
    "API rate limiting",
  ];

  return (
    <div className="mt-12 w-full max-w-4xl">
      <h3 className="text-sm font-semibold text-muted-foreground mb-4 uppercase tracking-wider">
        Example Queries
      </h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => onSelect(suggestion)}
            className="flex items-center justify-between rounded-lg border bg-card p-4 text-left hover:bg-muted/50 transition-colors group"
          >
            <span className="text-sm font-medium">{suggestion}</span>
            <ArrowRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity -translate-x-2 group-hover:translate-x-0 duration-300" />
          </button>
        ))}
      </div>
    </div>
  );
}
