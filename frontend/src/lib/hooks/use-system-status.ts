import { useState, useEffect } from "react";
import { SystemStatus } from "../types/system";
import { getSystemStatus } from "../api/system";

export function useSystemStatus() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function fetchStatus() {
      try {
        const data = await getSystemStatus();
        if (mounted) {
          setStatus(data);
          setError(null);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : "Failed to fetch system status");
          // Fallback handled in API, but just in case:
          setStatus({
            mode: "degraded",
            message: "Some backend services are unavailable.",
          });
        }
      } finally {
        if (mounted) {
          setIsLoading(false);
        }
      }
    }

    fetchStatus();

    return () => {
      mounted = false;
    };
  }, []);

  return { status, isLoading, error };
}
