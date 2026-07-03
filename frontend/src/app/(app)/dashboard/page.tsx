"use client";

import { useDashboard } from "@/lib/hooks/use-dashboard";
import { DashboardHero } from "@/components/dashboard/dashboard-hero";
import { StatsGrid } from "@/components/dashboard/stats-grid";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { ActivityFeed } from "@/components/dashboard/activity-feed";
import { OnboardingChecklist } from "@/components/dashboard/onboarding-checklist";
import { SystemHealthCard } from "@/components/dashboard/system-health-card";
export default function DashboardPage() {
  // In a real app with auth, we'd get the orgId from the session/context
  const orgId = "mock-org-id";
  const { data, isLoading, error } = useDashboard(orgId);

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-8">
        <div className="h-16 w-1/3 rounded-lg bg-muted"></div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 rounded-xl bg-muted"></div>
          ))}
        </div>
        <div className="grid gap-8 lg:grid-cols-3">
          <div className="h-64 rounded-xl bg-muted lg:col-span-2"></div>
          <div className="h-64 rounded-xl bg-muted"></div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex h-64 flex-col items-center justify-center rounded-xl border bg-card text-center">
        <p className="text-muted-foreground">Failed to load dashboard.</p>
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
    <div className="space-y-8 pb-8">
      <DashboardHero />
      
      <StatsGrid stats={data.stats} />
      
      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-8">
          <ActivityFeed activities={data.activity} />
          <OnboardingChecklist checklist={data.checklist} />
        </div>
        <div className="space-y-8">
          <SystemHealthCard health={data.system_health} />
          <QuickActions />
        </div>
      </div>
    </div>
  );
}
