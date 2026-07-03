import { useState, useEffect, useCallback } from "react";
import { IntegrationProvider, IntegrationConnection, SyncJob } from "../types/integrations";
import { getIntegrationsOverview } from "../api/integrations";

export function useIntegrations(orgId: string | undefined) {
  const [availableIntegrations, setAvailableIntegrations] = useState<IntegrationProvider[]>([]);
  const [connectedIntegrations, setConnectedIntegrations] = useState<IntegrationConnection[]>([]);
  const [recentJobs, setRecentJobs] = useState<SyncJob[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchIntegrations = useCallback(async () => {
    if (!orgId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const data = await getIntegrationsOverview(orgId);
      setAvailableIntegrations(data.available);
      setConnectedIntegrations(data.connected);
      setRecentJobs(data.recentJobs);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to load integrations"));
    } finally {
      setIsLoading(false);
    }
  }, [orgId]);

  useEffect(() => {
    fetchIntegrations();
  }, [fetchIntegrations]);

  return {
    availableIntegrations,
    connectedIntegrations,
    recentJobs,
    isLoading,
    error,
    refresh: fetchIntegrations,
    // Provide a way to manually update state for optimistic UI updates in action hooks
    setConnectedIntegrations,
    setAvailableIntegrations,
  };
}
