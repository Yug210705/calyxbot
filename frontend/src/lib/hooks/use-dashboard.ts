/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useEffect, useCallback } from "react";
import { DashboardResponse } from "../types/dashboard";
import { getDashboardData } from "../api/dashboard";

export function useDashboard(orgId: string | undefined) {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchDashboard = useCallback(async () => {
    if (!orgId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const response = await getDashboardData(orgId);
      setData(response);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to load dashboard data"));
    } finally {
      setIsLoading(false);
    }
  }, [orgId]);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return {
    data,
    isLoading,
    error,
    refetch: fetchDashboard,
  };
}
