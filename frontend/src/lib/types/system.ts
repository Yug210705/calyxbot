export type AppRuntimeMode = "live" | "demo" | "degraded";

export type SystemStatus = {
  mode: AppRuntimeMode;
  message: string;
  lastSyncLabel?: string;
};
