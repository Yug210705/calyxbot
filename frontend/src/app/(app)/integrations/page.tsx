"use client";

import { useIntegrations } from "@/lib/hooks/use-integrations";
import { useIntegrationActions } from "@/lib/hooks/use-integration-actions";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, Suspense } from "react";
import { IntegrationsHeader } from "@/components/integrations/integrations-header";
import { ConnectedIntegrationsGrid } from "@/components/integrations/connected-integrations-grid";
import { AvailableIntegrationsGrid } from "@/components/integrations/available-integrations-grid";
import { RecentSyncJobsCard } from "@/components/integrations/recent-sync-jobs-card";
import { IntegrationsSkeleton } from "@/components/integrations/integrations-skeleton";
import { useSyncJobs } from "@/lib/hooks/use-sync-jobs";
import { IntegrationErrorState } from "@/components/integrations/integration-error-state";
import { toastInfo, toastSuccess, toastError } from "@/components/ui/app-toast";

function IntegrationsPageContent() {
  const orgId = "mock-org-id"; // In a real app, this comes from auth/context
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const { 
    availableIntegrations, 
    connectedIntegrations, 
    isLoading, 
    error, 
    refresh,
    setConnectedIntegrations,
    setAvailableIntegrations
  } = useIntegrations(orgId);

  const { jobs: recentJobs, refresh: refreshJobs, hasActiveJobs } = useSyncJobs();

  const {
    pendingAction,
    handleConnectGoogleDrive,
    handleSyncNow,
    handleDisconnect
  } = useIntegrationActions(orgId, refresh);

  // Handle OAuth callback redirects
  useEffect(() => {
    const connected = searchParams.get("connected");
    const errorParam = searchParams.get("error");
    
    if (connected === "google_drive") {
      toastSuccess("Google Drive connected successfully!");
      refresh();
      // Clean up the URL
      router.replace("/integrations");
    } else if (errorParam) {
      toastError(`Failed to connect: ${errorParam.replace("_", " ")}`);
      // Clean up the URL
      router.replace("/integrations");
    }
  }, [searchParams, router, refresh]);

  // Fallback simulator for UI fluidity when API isn't ready
  const simulateConnect = (providerId: string) => {
    const provider = availableIntegrations.find(p => p.provider === providerId);
    if (!provider) return;
    
    setAvailableIntegrations(prev => prev.filter(p => p.provider !== providerId));
    setConnectedIntegrations(prev => [
      ...prev, 
      {
        id: `mock-conn-${Date.now()}`,
        provider: provider.provider,
        displayName: provider.name,
        status: "ACTIVE",
        health: "healthy",
        lastSyncAt: new Date().toISOString(),
        documentCount: 0,
      }
    ]);
  };

  const simulateDisconnect = (integrationId: string) => {
    const connection = connectedIntegrations.find(c => c.id === integrationId);
    if (!connection) return;
    
    setConnectedIntegrations(prev => prev.filter(c => c.id !== integrationId));
    // Ideally we'd add it back to available, but this is just a fallback simulation
    refresh(); 
  };

  if (isLoading) {
    return <IntegrationsSkeleton />;
  }

  if (error) {
    return <IntegrationErrorState onRetry={refresh} message={error.message} />;
  }

  return (
    <div className="space-y-12 pb-8">
      <IntegrationsHeader 
        onConnectGoogleDrive={() => handleConnectGoogleDrive(simulateConnect)}
        isConnecting={pendingAction === "connect_google_drive"}
      />
      
      {/* Section 1: Connected Integrations */}
      <section>
        <h2 className="text-xl font-semibold mb-6">Connected Data Sources</h2>
        <ConnectedIntegrationsGrid 
          connections={connectedIntegrations}
          onSync={(id) => handleSyncNow(id, refreshJobs)}
          onDisconnect={(id) => handleDisconnect(id, simulateDisconnect)}
          pendingAction={hasActiveJobs ? "sync_running" : pendingAction}
        />
      </section>

      {/* Section 2: Available Integrations */}
      {availableIntegrations.length > 0 && (
        <section>
          <div className="mb-6">
            <h2 className="text-xl font-semibold">Available Data Sources</h2>
            <p className="text-sm text-muted-foreground mt-1">Connect more tools to expand your organization's memory.</p>
          </div>
          <AvailableIntegrationsGrid 
            providers={availableIntegrations}
            onConnect={(providerId) => {
              if (providerId === "google_drive") {
                handleConnectGoogleDrive(simulateConnect);
              } else {
                toastInfo("Only Google Drive is implemented for this demo");
              }
            }}
            pendingAction={pendingAction}
          />
        </section>
      )}

      {/* Section 3: Recent Sync Jobs */}
      <section>
        <RecentSyncJobsCard jobs={recentJobs} />
      </section>
    </div>
  );
}

export default function IntegrationsPage() {
  return (
    <Suspense fallback={
      <div className="flex-1 space-y-6 p-8 max-w-7xl mx-auto w-full">
        <IntegrationsSkeleton />
      </div>
    }>
      <IntegrationsPageContent />
    </Suspense>
  );
}
