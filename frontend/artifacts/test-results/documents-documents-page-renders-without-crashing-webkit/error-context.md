# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: documents.spec.ts >> documents page renders without crashing
- Location: tests\e2e\specs\documents.spec.ts:3:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText('Documents')
Expected: visible
Error: strict mode violation: getByText('Documents') resolved to 4 elements:
    1) <a href="/documents" class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors bg-primary/10 text-primary">…</a> aka getByRole('link', { name: 'Documents' })
    2) <h1 class="text-3xl font-bold tracking-tight">Documents</h1> aka getByRole('heading', { name: 'Documents' })
    3) <p class="mt-2 text-muted-foreground">View and manage documents indexed across your con…</p> aka getByText('View and manage documents')
    4) <div class="hidden sm:flex items-center justify-between px-4 py-3 border-b bg-muted/20 text-xs font-medium text-muted-foreground uppercase tracking-wider">…</div> aka getByText('DocumentStatusVersionChunksUpdated')

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByText('Documents')

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e2]:
    - complementary [ref=e3]:
      - heading "Calyx" [level=1] [ref=e5]
      - generic [ref=e6]:
        - link "Dashboard" [ref=e7]:
          - /url: /dashboard
          - img [ref=e8]
          - text: Dashboard
        - link "Integrations" [ref=e13]:
          - /url: /integrations
          - img [ref=e14]
          - text: Integrations
        - link "Documents" [ref=e16]:
          - /url: /documents
          - img [ref=e17]
          - text: Documents
        - link "Search Memory" [ref=e21]:
          - /url: /search
          - img [ref=e22]
          - text: Search Memory
      - link "Settings" [ref=e26]:
        - /url: /settings
        - img [ref=e27]
        - text: Settings
    - generic [ref=e30]:
      - banner [ref=e31]:
        - generic [ref=e33] [cursor=pointer]:
          - img [ref=e34]
          - generic [ref=e38]: Acme Corp
        - generic [ref=e40]:
          - img [ref=e42]
          - button "Logout" [ref=e45]:
            - img [ref=e46]
      - generic [ref=e49]:
        - img [ref=e50]
        - generic [ref=e52]: "Calyx is running in demo mode using mock data. Connect a live source to start building real company memory. • Last sync: 2 minutes ago"
      - main [ref=e53]:
        - generic [ref=e55]:
          - generic [ref=e56]:
            - generic [ref=e57]:
              - heading "Documents" [level=1] [ref=e58]
              - paragraph [ref=e59]: View and manage documents indexed across your connected data sources.
            - button "Refresh" [ref=e60]:
              - img [ref=e61]
              - text: Refresh
          - generic [ref=e66]:
            - generic [ref=e67]:
              - img [ref=e68]
              - textbox "Search documents..." [ref=e71]
            - combobox [ref=e72]:
              - option "All Sources" [selected]
              - option "Google Drive"
              - option "Notion"
              - option "Slack"
              - option "Uploads"
            - combobox [ref=e73]:
              - option "All Statuses" [selected]
              - option "Ready"
              - option "Pending"
              - option "Fetched"
              - option "Normalized"
              - option "Chunked"
              - option "Embedded"
              - option "Indexed"
              - option "Graph Built"
              - option "Failed"
          - generic [ref=e74]:
            - generic [ref=e75]:
              - generic [ref=e76]: Document
              - generic [ref=e77]:
                - generic [ref=e78]: Status
                - generic [ref=e79]: Version
                - generic [ref=e80]: Chunks
                - generic [ref=e81]: Updated
            - generic [ref=e82]:
              - generic [ref=e83] [cursor=pointer]:
                - generic [ref=e84]:
                  - img [ref=e86]
                  - generic [ref=e89]:
                    - heading "Engineering Onboarding Handbook 2024" [level=4] [ref=e90]
                    - generic [ref=e91]:
                      - generic [ref=e92]:
                        - img [ref=e93]
                        - generic [ref=e95]: Engineering Hub
                      - generic [ref=e96]: •
                      - generic [ref=e97]: vnd.google-apps.document
                - generic [ref=e98]:
                  - generic [ref=e100]: Ready
                  - paragraph [ref=e102]: v3
                  - generic [ref=e103]:
                    - paragraph [ref=e104]: "42"
                    - paragraph [ref=e105]: Chunks
                  - paragraph [ref=e107]: 12m ago
                  - img [ref=e109]
              - generic [ref=e111] [cursor=pointer]:
                - generic [ref=e112]:
                  - img [ref=e114]
                  - generic [ref=e117]:
                    - heading "Q3 Sprint Planning Notes" [level=4] [ref=e118]
                    - generic [ref=e119]:
                      - generic [ref=e120]:
                        - img [ref=e121]
                        - generic [ref=e125]: Product Team
                      - generic [ref=e126]: •
                      - generic [ref=e127]: markdown
                - generic [ref=e128]:
                  - generic [ref=e130]: Graph Built
                  - paragraph [ref=e132]: v1
                  - generic [ref=e133]:
                    - paragraph [ref=e134]: "18"
                    - paragraph [ref=e135]: Chunks
                  - paragraph [ref=e137]: 45m ago
                  - img [ref=e139]
              - generic [ref=e141] [cursor=pointer]:
                - generic [ref=e142]:
                  - img [ref=e144]
                  - generic [ref=e147]:
                    - 'heading "Incident Postmortem: SEV-1 Database Outage" [level=4] [ref=e148]'
                    - generic [ref=e149]:
                      - generic [ref=e150]:
                        - img [ref=e151]
                        - generic [ref=e153]: SRE Shared Drive
                      - generic [ref=e154]: •
                      - generic [ref=e155]: vnd.google-apps.document
                - generic [ref=e156]:
                  - generic [ref=e158]: Embedded
                  - paragraph [ref=e160]: v1
                  - generic [ref=e161]:
                    - paragraph [ref=e162]: "24"
                    - paragraph [ref=e163]: Chunks
                  - paragraph [ref=e165]: 2h ago
                  - img [ref=e167]
              - generic [ref=e169] [cursor=pointer]:
                - generic [ref=e170]:
                  - img [ref=e172]
                  - generic [ref=e175]:
                    - heading "Frontend Architecture ADR-004" [level=4] [ref=e176]
                    - generic [ref=e177]:
                      - generic [ref=e178]:
                        - img [ref=e179]
                        - generic [ref=e181]: Architecture Board
                      - generic [ref=e182]: •
                      - generic [ref=e183]: pdf
                - generic [ref=e184]:
                  - generic [ref=e186]: Chunked
                  - paragraph [ref=e188]: v2
                  - generic [ref=e189]:
                    - paragraph [ref=e190]: "35"
                    - paragraph [ref=e191]: Chunks
                  - paragraph [ref=e193]: 5h ago
                  - img [ref=e195]
              - generic [ref=e197] [cursor=pointer]:
                - generic [ref=e198]:
                  - img [ref=e200]
                  - generic [ref=e203]:
                    - 'heading "Customer Escalation: ACME Corp Integration" [level=4] [ref=e204]'
                    - generic [ref=e205]:
                      - generic [ref=e206]:
                        - img [ref=e207]
                        - generic [ref=e209]: "#escalations-acme"
                      - generic [ref=e210]: •
                      - generic [ref=e211]: plain
                - generic [ref=e212]:
                  - generic [ref=e214]: Ready
                  - paragraph [ref=e216]: v1
                  - generic [ref=e217]:
                    - paragraph [ref=e218]: "8"
                    - paragraph [ref=e219]: Chunks
                  - paragraph [ref=e221]: 1d ago
                  - img [ref=e223]
              - generic [ref=e225] [cursor=pointer]:
                - generic [ref=e226]:
                  - img [ref=e228]
                  - generic [ref=e230]:
                    - heading "Senior Backend Engineer Scorecard" [level=4] [ref=e231]
                    - generic [ref=e232]:
                      - generic [ref=e233]:
                        - img [ref=e234]
                        - generic [ref=e236]: Hiring Hub
                      - generic [ref=e237]: •
                      - generic [ref=e238]: vnd.google-apps.spreadsheet
                - generic [ref=e239]:
                  - generic [ref=e241]: Failed
                  - paragraph [ref=e243]: v1
                  - generic [ref=e244]:
                    - paragraph [ref=e245]: "0"
                    - paragraph [ref=e246]: Chunks
                  - paragraph [ref=e248]: 2d ago
                  - img [ref=e250]
              - generic [ref=e252] [cursor=pointer]:
                - generic [ref=e253]:
                  - img [ref=e255]
                  - generic [ref=e258]:
                    - 'heading "Product Requirements: Search V2" [level=4] [ref=e259]'
                    - generic [ref=e260]:
                      - generic [ref=e261]:
                        - img [ref=e262]
                        - generic [ref=e266]: PRDs
                      - generic [ref=e267]: •
                      - generic [ref=e268]: markdown
                - generic [ref=e269]:
                  - generic [ref=e271]: Normalized
                  - paragraph [ref=e273]: v4
                  - generic [ref=e274]:
                    - paragraph [ref=e275]: "0"
                    - paragraph [ref=e276]: Chunks
                  - paragraph [ref=e278]: 5m ago
                  - img [ref=e280]
              - generic [ref=e282] [cursor=pointer]:
                - generic [ref=e283]:
                  - img [ref=e285]
                  - generic [ref=e288]:
                    - heading "Security Audit Findings 2023" [level=4] [ref=e289]
                    - generic [ref=e290]:
                      - generic [ref=e291]:
                        - img [ref=e292]
                        - generic [ref=e294]: Compliance
                      - generic [ref=e295]: •
                      - generic [ref=e296]: pdf
                - generic [ref=e297]:
                  - generic [ref=e299]: Fetched
                  - paragraph [ref=e301]: v1
                  - generic [ref=e302]:
                    - paragraph [ref=e303]: "0"
                    - paragraph [ref=e304]: Chunks
                  - paragraph [ref=e306]: 2m ago
                  - img [ref=e308]
              - generic [ref=e310] [cursor=pointer]:
                - generic [ref=e311]:
                  - img [ref=e313]
                  - generic [ref=e316]:
                    - heading "API Rate Limiting Proposal" [level=4] [ref=e317]
                    - generic [ref=e318]:
                      - generic [ref=e319]:
                        - img [ref=e320]
                        - generic [ref=e322]: Engineering Hub
                      - generic [ref=e323]: •
                      - generic [ref=e324]: vnd.google-apps.document
                - generic [ref=e325]:
                  - generic [ref=e327]: Ready
                  - paragraph [ref=e329]: v2
                  - generic [ref=e330]:
                    - paragraph [ref=e331]: "15"
                    - paragraph [ref=e332]: Chunks
                  - paragraph [ref=e334]: 4d ago
                  - img [ref=e336]
              - generic [ref=e338] [cursor=pointer]:
                - generic [ref=e339]:
                  - img [ref=e341]
                  - generic [ref=e343]:
                    - heading "Q4 Marketing Budget Draft" [level=4] [ref=e344]
                    - generic [ref=e345]:
                      - generic [ref=e346]:
                        - img [ref=e347]
                        - generic [ref=e349]: Finance
                      - generic [ref=e350]: •
                      - generic [ref=e351]: vnd.google-apps.spreadsheet
                - generic [ref=e352]:
                  - generic [ref=e354]: Pending
                  - paragraph [ref=e356]: v1
                  - generic [ref=e357]:
                    - paragraph [ref=e358]: "0"
                    - paragraph [ref=e359]: Chunks
                  - paragraph [ref=e361]: 1m ago
                  - img [ref=e363]
  - region "Notifications alt+T"
  - button "Open Next.js Dev Tools" [ref=e370] [cursor=pointer]:
    - img [ref=e371]
  - alert [ref=e376]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('documents page renders without crashing', async ({ page }) => {
  4  |   await page.goto('/documents');
  5  |   
  6  |   // Wait for loading to finish
  7  |   await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  8  |   
  9  |   // Check that the table renders
> 10 |   await expect(page.getByText('Documents')).toBeVisible();
     |                                             ^ Error: expect(locator).toBeVisible() failed
  11 |   await expect(page.getByRole('table')).toBeVisible();
  12 | });
  13 | 
```