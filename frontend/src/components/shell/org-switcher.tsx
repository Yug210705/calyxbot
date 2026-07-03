"use client";

import { Building2 } from "lucide-react";

export function OrgSwitcher() {
  // For MVP, just hardcode a placeholder or read from a mock.
  // In a real app, this would be a dropdown showing current org and allowing switch.
  
  return (
    <div className="flex items-center gap-2 rounded-md border px-3 py-1.5 text-sm font-medium hover:bg-muted cursor-pointer transition-colors">
      <Building2 className="h-4 w-4 text-muted-foreground" />
      <span>Acme Corp</span>
    </div>
  );
}
