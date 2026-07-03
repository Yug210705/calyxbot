import { AlertCircle } from "lucide-react";

interface ErrorStateProps {
  message?: string;
  onRetry: () => void;
}

export function SearchErrorState({ message = "Failed to run search", onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-24 text-center bg-card mt-8">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-500/10 text-red-500 mb-6">
        <AlertCircle className="h-8 w-8" />
      </div>
      <h3 className="text-xl font-semibold mb-2">Something went wrong</h3>
      <p className="text-muted-foreground mb-8 max-w-md">{message}</p>
      <button 
        onClick={onRetry}
        className="rounded-md bg-primary px-6 py-2.5 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors shadow-sm"
      >
        Try Again
      </button>
    </div>
  );
}
