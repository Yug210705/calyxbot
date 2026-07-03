import { useState, useEffect, useCallback } from "react";
import { SettingsData } from "../types/settings";
import { getSettingsData, updateSettingsData } from "../api/settings";
import { toastSuccess, toastError } from "@/components/ui/app-toast";

export function useSettings(orgId: string | undefined) {
  const [data, setData] = useState<SettingsData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchSettings = useCallback(async () => {
    if (!orgId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const response = await getSettingsData(orgId);
      setData(response);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to load settings"));
    } finally {
      setIsLoading(false);
    }
  }, [orgId]);

  useEffect(() => {
    fetchSettings();
  }, [fetchSettings]);

  const updateSettings = async (updates: Partial<SettingsData>) => {
    if (!orgId || !data) return;
    
    setIsSaving(true);
    try {
      const response = await updateSettingsData(orgId, updates);
      setData(response);
      toastSuccess("Settings saved successfully");
    } catch (err) {
      toastError("Failed to save settings");
      throw err;
    } finally {
      setIsSaving(false);
    }
  };

  return {
    data,
    isLoading,
    isSaving,
    error,
    refetch: fetchSettings,
    updateSettings,
  };
}
