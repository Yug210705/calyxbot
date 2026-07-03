import { AlertCircle } from "lucide-react";

interface ErrorStateProps {
  message?: string;
  onRetry: () => void;
}

export function IntegrationErrorState({ message = "Failed to load integrations", onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-12 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-red-500/10 text-red-500 mb-4">
        <AlertCircle className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-medium">Something went wrong</h3>
      <p className="text-sm text-muted-foreground mt-1 max-w-sm">{message}</p>
      <button 
        onClick={onRetry}
        className="mt-6 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors"
      >
        Try Again
      </button>
    </div>
  );
}
