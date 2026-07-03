"use client";

import { useSettings } from "@/lib/hooks/use-settings";
import { OrganizationProfileForm } from "@/components/settings/organization-profile";

export default function SettingsPage() {
  const orgId = "mock-org-id";
  const { data, isLoading, isSaving, error, updateSettings } = useSettings(orgId);

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-64 rounded-xl bg-muted"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-64 flex-col items-center justify-center rounded-xl border bg-card text-center">
        <p className="text-muted-foreground">Failed to load settings.</p>
        <button 
          onClick={() => window.location.reload()} 
          className="mt-4 rounded-md bg-primary px-4 py-2 text-sm text-primary-foreground hover:bg-primary/90"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8 pb-12">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">General Settings</h1>
        <p className="text-muted-foreground mt-2">
          Manage your organization profile and workspace preferences.
        </p>
      </div>

      <div className="space-y-8">
        <OrganizationProfileForm 
          profile={data.organization} 
          onSave={updateSettings} 
          isSaving={isSaving} 
        />
      </div>
    </div>
  );
}
