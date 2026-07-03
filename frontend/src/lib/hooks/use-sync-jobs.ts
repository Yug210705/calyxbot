/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useEffect, useCallback } from "react";
import { SyncJob } from "../types/integrations";
import { getSyncJobs } from "../api/sync-jobs";

export function useSyncJobs() {
  const [jobs, setJobs] = useState<SyncJob[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJobs = useCallback(async () => {
    try {
      const data = await getSyncJobs();
      setJobs(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to load sync jobs");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const hasActiveJobs = jobs.some((job) => job.status === "PENDING" || job.status === "RUNNING");

  useEffect(() => {
    let intervalId: NodeJS.Timeout;
    
    if (hasActiveJobs) {
      intervalId = setInterval(() => {
        fetchJobs();
      }, 3000);
    }
    
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [hasActiveJobs, fetchJobs]);

  return {
    jobs,
    isLoading,
    error,
    refresh: fetchJobs,
    hasActiveJobs,
  };
}
