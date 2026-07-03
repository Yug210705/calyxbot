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
    ...

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
        - link "Dashboard" [ref=e7] [cursor=pointer]:
          - /url: /dashboard
          - img [ref=e8]
          - text: Dashboard
        - link "Integrations" [ref=e13] [cursor=pointer]:
          - /url: /integrations
          - img [ref=e14]
          - text: Integrations
        - link "Documents" [ref=e19] [cursor=pointer]:
          - /url: /documents
          - img [ref=e20]
          - text: Documents
        - link "Search Memory" [ref=e24] [cursor=pointer]:
          - /url: /search
          - img [ref=e25]
          - text: Search Memory
      - link "Settings" [ref=e29] [cursor=pointer]:
        - /url: /settings
        - img [ref=e30]
        - text: Settings
    - generic [ref=e33]:
      - banner [ref=e34]:
        - generic [ref=e36] [cursor=pointer]:
          - img [ref=e37]
          - generic [ref=e43]: Acme Corp
        - generic [ref=e45]:
          - img [ref=e47]
          - button "Logout" [ref=e50]:
            - img [ref=e51]
      - generic [ref=e55]:
        - img [ref=e56]
        - generic [ref=e60]: "Calyx is running in demo mode using mock data. Connect a live source to start building real company memory. • Last sync: 2 minutes ago"
      - main [ref=e61]:
        - generic [ref=e63]:
          - generic [ref=e64]:
            - generic [ref=e65]:
              - heading "Documents" [level=1] [ref=e66]
              - paragraph [ref=e67]: View and manage documents indexed across your connected data sources.
            - button "Refresh" [ref=e68]:
              - img [ref=e69]
              - text: Refresh
          - generic [ref=e74]:
            - generic [ref=e75]:
              - img [ref=e76]
              - textbox "Search documents..." [ref=e79]
            - combobox [ref=e80]:
              - option "All Sources" [selected]
              - option "Google Drive"
              - option "Notion"
              - option "Slack"
              - option "Uploads"
            - combobox [ref=e81]:
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
          - generic [ref=e82]:
            - generic [ref=e83]:
              - generic [ref=e84]: Document
              - generic [ref=e85]:
                - generic [ref=e86]: Status
                - generic [ref=e87]: Version
                - generic [ref=e88]: Chunks
                - generic [ref=e89]: Updated
            - generic [ref=e90]:
              - generic [ref=e91] [cursor=pointer]:
                - generic [ref=e92]:
                  - img [ref=e94]
                  - generic [ref=e100]:
                    - heading "Engineering Onboarding Handbook 2024" [level=4] [ref=e101]
                    - generic [ref=e102]:
                      - generic [ref=e103]:
                        - img [ref=e104]
                        - generic [ref=e106]: Engineering Hub
                      - generic [ref=e107]: •
                      - generic [ref=e108]: vnd.google-apps.document
                - generic [ref=e109]:
                  - generic [ref=e111]: Ready
                  - paragraph [ref=e113]: v3
                  - generic [ref=e114]:
                    - paragraph [ref=e115]: "42"
                    - paragraph [ref=e116]: Chunks
                  - paragraph [ref=e118]: 12m ago
                  - img [ref=e120]
              - generic [ref=e122] [cursor=pointer]:
                - generic [ref=e123]:
                  - img [ref=e125]
                  - generic [ref=e131]:
                    - heading "Q3 Sprint Planning Notes" [level=4] [ref=e132]
                    - generic [ref=e133]:
                      - generic [ref=e134]:
                        - img [ref=e135]
                        - generic [ref=e139]: Product Team
                      - generic [ref=e140]: •
                      - generic [ref=e141]: markdown
                - generic [ref=e142]:
                  - generic [ref=e144]: Graph Built
                  - paragraph [ref=e146]: v1
                  - generic [ref=e147]:
                    - paragraph [ref=e148]: "18"
                    - paragraph [ref=e149]: Chunks
                  - paragraph [ref=e151]: 45m ago
                  - img [ref=e153]
              - generic [ref=e155] [cursor=pointer]:
                - generic [ref=e156]:
                  - img [ref=e158]
                  - generic [ref=e164]:
                    - 'heading "Incident Postmortem: SEV-1 Database Outage" [level=4] [ref=e165]'
                    - generic [ref=e166]:
                      - generic [ref=e167]:
                        - img [ref=e168]
                        - generic [ref=e170]: SRE Shared Drive
                      - generic [ref=e171]: •
                      - generic [ref=e172]: vnd.google-apps.document
                - generic [ref=e173]:
                  - generic [ref=e175]: Embedded
                  - paragraph [ref=e177]: v1
                  - generic [ref=e178]:
                    - paragraph [ref=e179]: "24"
                    - paragraph [ref=e180]: Chunks
                  - paragraph [ref=e182]: 2h ago
                  - img [ref=e184]
              - generic [ref=e186] [cursor=pointer]:
                - generic [ref=e187]:
                  - img [ref=e189]
                  - generic [ref=e195]:
                    - heading "Frontend Architecture ADR-004" [level=4] [ref=e196]
                    - generic [ref=e197]:
                      - generic [ref=e198]:
                        - img [ref=e199]
                        - generic [ref=e201]: Architecture Board
                      - generic [ref=e202]: •
                      - generic [ref=e203]: pdf
                - generic [ref=e204]:
                  - generic [ref=e206]: Chunked
                  - paragraph [ref=e208]: v2
                  - generic [ref=e209]:
                    - paragraph [ref=e210]: "35"
                    - paragraph [ref=e211]: Chunks
                  - paragraph [ref=e213]: 5h ago
                  - img [ref=e215]
              - generic [ref=e217] [cursor=pointer]:
                - generic [ref=e218]:
                  - img [ref=e220]
                  - generic [ref=e226]:
                    - 'heading "Customer Escalation: ACME Corp Integration" [level=4] [ref=e227]'
                    - generic [ref=e228]:
                      - generic [ref=e229]:
                        - img [ref=e230]
                        - generic [ref=e232]: "#escalations-acme"
                      - generic [ref=e233]: •
                      - generic [ref=e234]: plain
                - generic [ref=e235]:
                  - generic [ref=e237]: Ready
                  - paragraph [ref=e239]: v1
                  - generic [ref=e240]:
                    - paragraph [ref=e241]: "8"
                    - paragraph [ref=e242]: Chunks
                  - paragraph [ref=e244]: 1d ago
                  - img [ref=e246]
              - generic [ref=e248] [cursor=pointer]:
                - generic [ref=e249]:
                  - img [ref=e251]
                  - generic [ref=e255]:
                    - heading "Senior Backend Engineer Scorecard" [level=4] [ref=e256]
                    - generic [ref=e257]:
                      - generic [ref=e258]:
                        - img [ref=e259]
                        - generic [ref=e261]: Hiring Hub
                      - generic [ref=e262]: •
                      - generic [ref=e263]: vnd.google-apps.spreadsheet
                - generic [ref=e264]:
                  - generic [ref=e266]: Failed
                  - paragraph [ref=e268]: v1
                  - generic [ref=e269]:
                    - paragraph [ref=e270]: "0"
                    - paragraph [ref=e271]: Chunks
                  - paragraph [ref=e273]: 2d ago
                  - img [ref=e275]
              - generic [ref=e277] [cursor=pointer]:
                - generic [ref=e278]:
                  - img [ref=e280]
                  - generic [ref=e286]:
                    - 'heading "Product Requirements: Search V2" [level=4] [ref=e287]'
                    - generic [ref=e288]:
                      - generic [ref=e289]:
                        - img [ref=e290]
                        - generic [ref=e294]: PRDs
                      - generic [ref=e295]: •
                      - generic [ref=e296]: markdown
                - generic [ref=e297]:
                  - generic [ref=e299]: Normalized
                  - paragraph [ref=e301]: v4
                  - generic [ref=e302]:
                    - paragraph [ref=e303]: "0"
                    - paragraph [ref=e304]: Chunks
                  - paragraph [ref=e306]: 5m ago
                  - img [ref=e308]
              - generic [ref=e310] [cursor=pointer]:
                - generic [ref=e311]:
                  - img [ref=e313]
                  - generic [ref=e319]:
                    - heading "Security Audit Findings 2023" [level=4] [ref=e320]
                    - generic [ref=e321]:
                      - generic [ref=e322]:
                        - img [ref=e323]
                        - generic [ref=e325]: Compliance
                      - generic [ref=e326]: •
                      - generic [ref=e327]: pdf
                - generic [ref=e328]:
                  - generic [ref=e330]: Fetched
                  - paragraph [ref=e332]: v1
                  - generic [ref=e333]:
                    - paragraph [ref=e334]: "0"
                    - paragraph [ref=e335]: Chunks
                  - paragraph [ref=e337]: 2m ago
                  - img [ref=e339]
              - generic [ref=e341] [cursor=pointer]:
                - generic [ref=e342]:
                  - img [ref=e344]
                  - generic [ref=e350]:
                    - heading "API Rate Limiting Proposal" [level=4] [ref=e351]
                    - generic [ref=e352]:
                      - generic [ref=e353]:
                        - img [ref=e354]
                        - generic [ref=e356]: Engineering Hub
                      - generic [ref=e357]: •
                      - generic [ref=e358]: vnd.google-apps.document
                - generic [ref=e359]:
                  - generic [ref=e361]: Ready
                  - paragraph [ref=e363]: v2
                  - generic [ref=e364]:
                    - paragraph [ref=e365]: "15"
                    - paragraph [ref=e366]: Chunks
                  - paragraph [ref=e368]: 4d ago
                  - img [ref=e370]
              - generic [ref=e372] [cursor=pointer]:
                - generic [ref=e373]:
                  - img [ref=e375]
                  - generic [ref=e379]:
                    - heading "Q4 Marketing Budget Draft" [level=4] [ref=e380]
                    - generic [ref=e381]:
                      - generic [ref=e382]:
                        - img [ref=e383]
                        - generic [ref=e385]: Finance
                      - generic [ref=e386]: •
                      - generic [ref=e387]: vnd.google-apps.spreadsheet
                - generic [ref=e388]:
                  - generic [ref=e390]: Pending
                  - paragraph [ref=e392]: v1
                  - generic [ref=e393]:
                    - paragraph [ref=e394]: "0"
                    - paragraph [ref=e395]: Chunks
                  - paragraph [ref=e397]: 1m ago
                  - img [ref=e399]
  - region "Notifications alt+T"
  - button "Open Next.js Dev Tools" [ref=e406] [cursor=pointer]:
    - img [ref=e407]
  - alert [ref=e411]
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