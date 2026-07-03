import { IntegrationConnection } from "@/lib/types/integrations";
import { IntegrationCard } from "./integration-card";
import { IntegrationsEmptyState } from "./integrations-empty-state";

interface Props {
  connections: IntegrationConnection[];
  onSync: (id: string) => void;
  onDisconnect: (id: string) => void;
  pendingAction: string | null;
}

export function ConnectedIntegrationsGrid({ connections, onSync, onDisconnect, pendingAction }: Props) {
  if (connections.length === 0) {
    return <IntegrationsEmptyState />;
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      {connections.map((conn) => (
        <IntegrationCard 
          key={conn.id} 
          connection={conn} 
          onSync={() => onSync(conn.id)}
          onDisconnect={() => onDisconnect(conn.id)}
          isActionPending={pendingAction?.includes(conn.id) || false}
        />
      ))}
    </div>
  );
}
