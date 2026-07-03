import { SystemStatus } from "../types/system";
import { mockSystemStatus } from "../mocks/system";
import { apiFetch } from "./client";

const USE_UI_MOCKS = true; // Hardcoded to true for UI Rescue Sprint

export async function getSystemStatus(): Promise<SystemStatus> {
  if (USE_UI_MOCKS) {
    await new Promise((resolve) => setTimeout(resolve, 300));
    return mockSystemStatus;
  }

  try {
    const status = await apiFetch<SystemStatus>("/system/health");
    return status;
  } catch (error) {
    console.warn("Real API failed, falling back to mock system status", error);
    return {
      mode: "degraded",
      message: "Some backend services are unavailable. Search and sync actions may be simulated temporarily.",
    };
  }
}
