/* eslint-disable react/no-unescaped-entities */
import { Plug } from "lucide-react";

export function IntegrationsEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed py-16 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary mb-4">
        <Plug className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-medium">No Integrations Yet</h3>
      <p className="text-sm text-muted-foreground mt-1 max-w-sm">
        Connect your first data source to start building your organization's semantic memory.
      </p>
    </div>
  );
}
