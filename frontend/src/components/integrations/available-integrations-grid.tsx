import { IntegrationProvider } from "@/lib/types/integrations";
import { IntegrationCard } from "./integration-card";

interface Props {
  providers: IntegrationProvider[];
  onConnect: (providerId: string) => void;
  pendingAction: string | null;
}

export function AvailableIntegrationsGrid({ providers, onConnect, pendingAction }: Props) {
  if (providers.length === 0) {
    return null; // Don't show anything if all are connected
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
      {providers.map((provider) => (
        <IntegrationCard 
          key={provider.provider} 
          provider={provider} 
          onConnect={() => onConnect(provider.provider)}
          isActionPending={pendingAction === `connect_${provider.provider}`}
        />
      ))}
    </div>
  );
}
