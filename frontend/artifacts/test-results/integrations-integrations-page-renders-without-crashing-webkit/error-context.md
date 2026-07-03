# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: integrations.spec.ts >> integrations page renders without crashing
- Location: tests\e2e\specs\integrations.spec.ts:3:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText('Connected Integrations')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByText('Connected Integrations')

```

```yaml
- complementary:
  - heading "Calyx" [level=1]
  - link "Dashboard":
    - /url: /dashboard
  - link "Integrations":
    - /url: /integrations
  - link "Documents":
    - /url: /documents
  - link "Search Memory":
    - /url: /search
  - link "Settings":
    - /url: /settings
- banner:
  - text: Acme Corp
  - button "Logout"
- text: "Calyx is running in demo mode using mock data. Connect a live source to start building real company memory. • Last sync: 2 minutes ago"
- main:
  - heading "Integrations" [level=1]
  - paragraph: Connect data sources to build your organization's semantic memory.
  - button "Connect Google Drive"
  - heading "Connected Data Sources" [level=2]
  - heading "Engineering Drive" [level=3]
  - text: active Healthy
  - paragraph: Documents
  - paragraph: "147"
  - paragraph: Last Sync
  - paragraph: 12:28 AM
  - button "Sync Now"
  - button "Pause"
  - button "Disconnect"
  - heading "Available Data Sources" [level=2]
  - paragraph: Connect more tools to expand your organization's memory.
  - heading "Google Drive" [level=3]
  - paragraph: Sync documents, spreadsheets, and presentations.
  - button "Connect"
  - heading "Notion" [level=3]
  - paragraph: Connect your workspaces and knowledge bases.
  - button "Connect"
  - heading "Slack" [level=3]
  - paragraph: Index channel history and team discussions.
  - button "Connect"
  - heading "Recent Sync Jobs" [level=3]
  - text: No recent sync jobs across your integrations.
- region "Notifications alt+T"
- alert
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('integrations page renders without crashing', async ({ page }) => {
  4  |   await page.goto('/integrations');
  5  |   
  6  |   // Wait for loading to finish
  7  |   await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  8  |   
  9  |   // Check that the shell renders
> 10 |   await expect(page.getByText('Connected Integrations')).toBeVisible();
     |                                                          ^ Error: expect(locator).toBeVisible() failed
  11 |   await expect(page.getByText('Available Integrations')).toBeVisible();
  12 | });
  13 | 
```