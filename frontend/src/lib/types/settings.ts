export type OrganizationProfile = {
  id: string;
  name: string;
  slug: string;
  plan: "Free" | "Pro" | "Enterprise";
  memberCount: number;
};

export type AppearanceSettings = {
  theme: "light" | "dark" | "system";
};

export type AdvancedSettings = {
  retentionDays: number;
  customIndexingRules: boolean;
};

export type SettingsData = {
  organization: OrganizationProfile;
  appearance: AppearanceSettings;
  advanced: AdvancedSettings;
};
