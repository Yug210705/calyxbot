import { SettingsData } from "../types/settings";

export const mockSettingsData: SettingsData = {
  organization: {
    id: "org-1",
    name: "Acme Corp",
    slug: "acme-corp",
    plan: "Pro",
    memberCount: 12,
  },
  appearance: {
    theme: "system",
  },
  advanced: {
    retentionDays: 90,
    customIndexingRules: false,
  }
};
