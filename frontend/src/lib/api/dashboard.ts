import { DashboardResponse } from "../types/dashboard";
import { apiFetch } from "./client";
import { mockDashboardData } from "../mocks/dashboard";
import { shouldFallbackToMock } from "./fallback";

const USE_UI_MOCKS = process.env.NEXT_PUBLIC_USE_UI_MOCKS === "true";

export async function getDashboardData(orgId: string): Promise<DashboardResponse> {
  try {
    return await apiFetch<DashboardResponse>("/dashboard", { organizationId: orgId });
  } catch (error) {
    if (USE_UI_MOCKS || shouldFallbackToMock(error)) {
      console.warn("API failed or mocks enabled, falling back to mock data for dashboard", error);
      return mockDashboardData;
    }
    throw error;
  }
}
