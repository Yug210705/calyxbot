/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import { connectGoogleDrive, disconnectIntegration } from "../api/integrations";
import { triggerIntegrationSync } from "../api/sync-jobs";
import { toastSuccess, toastError, toastInfo } from "@/components/ui/app-toast";

export function useIntegrationActions(orgId: string | undefined, refreshIntegrations: () => void) {
  const [pendingAction, setPendingAction] = useState<string | null>(null);

  const handleConnectGoogleDrive = async (simulateUpdate: (providerId: string) => void) => {
    if (!orgId) return;
    setPendingAction("connect_google_drive");
    try {
      const response = await connectGoogleDrive(orgId);
      if (response && response.authorization_url) {
        window.location.href = response.authorization_url;
      } else {
        toastError("Failed to get authorization URL from server");
      }
    } catch (error) {
      console.error(error);
      toastError("Failed to connect Google Drive");
    } finally {
      setPendingAction(null);
    }
  };

  const handleSyncNow = async (integrationId: string, refreshJobs?: () => void) => {
    if (!orgId) return;
    setPendingAction(`sync_${integrationId}`);
    try {
      await triggerIntegrationSync(integrationId);
      toastSuccess("Sync started");
      if (refreshJobs) refreshJobs();
    } catch (error: any) {
      console.error(error);
      toastError(error.message || "Failed to trigger sync");
    } finally {
      setPendingAction(null);
    }
  };

  const handleDisconnect = async (integrationId: string, simulateDisconnect: (id: string) => void) => {
    if (!orgId) return;
    
    // Minimal confirm before disconnect
    if (!confirm("Are you sure you want to disconnect this integration?")) return;

    setPendingAction(`disconnect_${integrationId}`);
    try {
      await disconnectIntegration(integrationId, orgId);
      refreshIntegrations();
      toastSuccess("Integration disconnected");
    } catch (error) {
      console.error(error);
      simulateDisconnect(integrationId);
      toastInfo("Integration disconnected (mock)");
    } finally {
      setPendingAction(null);
    }
  };

  return {
    pendingAction,
    handleConnectGoogleDrive,
    handleSyncNow,
    handleDisconnect,
  };
}
