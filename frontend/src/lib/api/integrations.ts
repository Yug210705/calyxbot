/* eslint-disable @typescript-eslint/no-unused-vars */
import { apiFetch } from "./client";
import { 
  IntegrationProvider, 
  IntegrationConnection, 
  SyncJob 
} from "../types/integrations";
import { 
  mockAvailableProviders, 
  mockConnectedIntegrations, 
  mockRecentSyncJobs 
} from "../mocks/integrations";

import { shouldFallbackToMock } from "./fallback";

const USE_UI_MOCKS = process.env.NEXT_PUBLIC_USE_UI_MOCKS === "true";

export async function getIntegrationsOverview(orgId: string): Promise<{
  available: IntegrationProvider[];
  connected: IntegrationConnection[];
  recentJobs: SyncJob[];
}> {
  try {
    const [integrations, syncJobs] = await Promise.all([
      apiFetch<IntegrationConnection[]>("/integrations", { organizationId: orgId }),
      apiFetch<SyncJob[]>("/integrations/jobs", { organizationId: orgId }).catch(() => [])
    ]);
    
    // We mock available providers for now since there isn't a backend registry endpoint yet
    // In the future we could fetch this from /integrations/providers
    return {
      available: mockAvailableProviders.filter(
        p => !integrations.some(c => c.provider === p.provider)
      ),
      connected: integrations,
      recentJobs: syncJobs,
    };
  } catch (error) {
    if (USE_UI_MOCKS || shouldFallbackToMock(error)) {
      console.warn("Real API failed, falling back to mock data for integrations", error);
      return {
        available: mockAvailableProviders,
        connected: mockConnectedIntegrations,
        recentJobs: [] as SyncJob[],
      };
    }
    throw error;
  }
}

export async function connectGoogleDrive(orgId: string): Promise<{ authorization_url: string } | null> {
  try {
    return await apiFetch<{ authorization_url: string }>("/integrations/google/connect", {
      method: "POST",
      organizationId: orgId
    });
  } catch (error) {
    if (USE_UI_MOCKS || shouldFallbackToMock(error)) {
      console.warn("Real API failed, returning mock authorization URL for Google Drive");
      return { authorization_url: "/integrations?connected=google_drive" };
    }
    throw error;
  }
}



export async function disconnectIntegration(id: string, orgId: string): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, 600));
  return; // Force mock simulation
}
