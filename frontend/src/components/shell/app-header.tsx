import { OrgSwitcher } from "./org-switcher";
import { UserMenu } from "./user-menu";

export function AppHeader() {
  return (
    <header className="h-16 border-b bg-background flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        <OrgSwitcher />
      </div>
      <div className="flex items-center gap-4">
        {/* Placeholder for future mini search or notifications */}
        <UserMenu />
      </div>
    </header>
  );
}
