"use client";

import { OrganizationProfile } from "@/lib/types/settings";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Save, Building2, Users } from "lucide-react";

interface Props {
  profile: OrganizationProfile;
  onSave: (updates: Partial<{ organization: OrganizationProfile }>) => Promise<void>;
  isSaving: boolean;
}

export function OrganizationProfileForm({ profile, onSave, isSaving }: Props) {
  const [name, setName] = useState(profile.name);
  const [slug, setSlug] = useState(profile.slug);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (name === profile.name && slug === profile.slug) return;
    
    await onSave({
      organization: { ...profile, name, slug }
    });
  };

  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden">
      <div className="p-6 border-b bg-muted/10">
        <h3 className="font-semibold text-lg">Organization Profile</h3>
        <p className="text-sm text-muted-foreground mt-1">Manage your company details and workspace settings.</p>
      </div>
      
      <form onSubmit={handleSubmit} className="p-6 space-y-6">
        <div className="grid gap-6 sm:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium">Organization Name</label>
            <div className="relative">
              <Building2 className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                className="pl-9" 
                placeholder="Acme Corp"
              />
            </div>
          </div>
          
          <div className="space-y-2">
            <label className="text-sm font-medium">Workspace Slug</label>
            <Input 
              value={slug} 
              onChange={(e) => setSlug(e.target.value)} 
              className="font-mono text-sm" 
              placeholder="acme-corp"
            />
            <p className="text-xs text-muted-foreground">Used for your unique Calyx URL.</p>
          </div>
        </div>

        <div className="flex items-center gap-6 p-4 rounded-lg bg-muted/30 border">
          <div className="flex-1">
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-primary" />
              <span className="text-sm font-medium">Current Plan</span>
            </div>
            <p className="text-sm text-muted-foreground mt-1">
              You are currently on the <strong className="text-foreground">{profile.plan}</strong> plan with {profile.memberCount} active members.
            </p>
          </div>
          <Button variant="outline" size="sm" type="button">Upgrade Plan</Button>
        </div>

        <div className="pt-2 flex justify-end">
          <Button 
            type="submit" 
            disabled={isSaving || (name === profile.name && slug === profile.slug)}
            className="gap-2"
          >
            <Save className="h-4 w-4" />
            {isSaving ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </form>
    </div>
  );
}
