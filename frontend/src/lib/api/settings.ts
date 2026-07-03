import { SettingsData } from "../types/settings";
import { apiFetch } from "./client";
import { mockSettingsData } from "../mocks/settings";

const USE_UI_MOCKS = true; // Hardcoded for UI Rescue Sprint

export async function getSettingsData(orgId: string): Promise<SettingsData> {
  if (USE_UI_MOCKS) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return mockSettingsData;
  }

  try {
    return await apiFetch<SettingsData>("/settings", { organizationId: orgId });
  } catch (error) {
    console.warn("Real API failed, falling back to mock data for settings", error);
    return mockSettingsData;
  }
}

export async function updateSettingsData(orgId: string, updates: Partial<SettingsData>): Promise<SettingsData> {
  if (USE_UI_MOCKS) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    return { ...mockSettingsData, ...updates }; // Just mock the return
  }

  return await apiFetch<SettingsData>("/settings", {
    method: "PATCH",
    organizationId: orgId,
    body: JSON.stringify(updates),
  });
}
