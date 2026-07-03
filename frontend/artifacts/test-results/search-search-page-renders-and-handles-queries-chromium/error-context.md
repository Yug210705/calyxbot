# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: search.spec.ts >> search page renders and handles queries
- Location: tests\e2e\specs\search.spec.ts:3:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByPlaceholder('Ask anything or search your memory...')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByPlaceholder('Ask anything or search your memory...')

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
  - heading "Semantic Memory Search" [level=1]
  - paragraph: Retrieve exact answers and context across your indexed documents, chunks, and knowledge graph.
  - textbox "Ask a question or search for concepts..."
  - button "Search" [disabled]
  - heading "Search Organizational Memory" [level=3]
  - paragraph: Type a query to search across all your connected documents, chunks, and extracted knowledge objects.
  - heading "Example Queries" [level=3]
  - button "Sprint planning notes"
  - button "Incident response process"
  - button "Onboarding handbook"
  - button "Customer escalation"
  - button "Hiring scorecard"
  - button "API rate limiting"
- region "Notifications alt+T"
- alert
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('search page renders and handles queries', async ({ page }) => {
  4  |   await page.goto('/search');
  5  |   
  6  |   // Wait for loading to finish
  7  |   await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  8  |   
  9  |   // Verify empty state
> 10 |   await expect(page.getByPlaceholder('Ask anything or search your memory...')).toBeVisible();
     |                                                                                ^ Error: expect(locator).toBeVisible() failed
  11 |   await expect(page.getByText('Start typing to search across your documents')).toBeVisible();
  12 | 
  13 |   // Trigger search
  14 |   await page.getByPlaceholder('Ask anything or search your memory...').fill('test query');
  15 |   // the page might auto-search or have a button, assuming auto-search or enter
  16 |   await page.keyboard.press('Enter');
  17 | 
  18 |   // Verify search loading or results
  19 |   await expect(page.getByText('Search Results')).toBeVisible({ timeout: 10000 });
  20 | });
  21 | 
```