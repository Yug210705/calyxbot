# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: dashboard.spec.ts >> dashboard page renders without crashing
- Location: tests\e2e\specs\dashboard.spec.ts:3:5

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  locator('.animate-pulse')
Expected: 0
Received: 2
Timeout:  10000ms

Call log:
  - Expect "toHaveCount" with timeout 10000ms
  - waiting for locator('.animate-pulse')
    19 × locator resolved to 2 elements
       - unexpected value "2"

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e5]:
    - generic [ref=e6]:
      - img [ref=e8]
      - heading "Welcome Back" [level=1] [ref=e10]
      - paragraph [ref=e11]: Sign in to your Calyx account.
    - generic [ref=e12]:
      - generic [ref=e13]:
        - generic [ref=e14]: Email Address
        - textbox "Email Address" [ref=e15]:
          - /placeholder: ada@example.com
      - generic [ref=e16]:
        - generic [ref=e17]:
          - generic [ref=e18]: Password
          - link "Forgot password?" [ref=e19] [cursor=pointer]:
            - /url: "#"
        - textbox "Password" [ref=e20]:
          - /placeholder: ••••••••
      - button "Sign In" [ref=e21]
    - generic [ref=e22]:
      - text: Don't have an account?
      - link "Create one" [ref=e23] [cursor=pointer]:
        - /url: /signup
  - region "Notifications alt+T"
  - button "Open Next.js Dev Tools" [ref=e29] [cursor=pointer]:
    - img [ref=e30]
  - alert [ref=e33]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test('dashboard page renders without crashing', async ({ page }) => {
  4  |   await page.goto('/dashboard');
  5  |   
  6  |   // Wait for loading to finish
> 7  |   await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
     |                                                ^ Error: expect(locator).toHaveCount(expected) failed
  8  |   
  9  |   // Check that key sections are rendered
  10 |   await expect(page.getByText('Connected Sources')).toBeVisible();
  11 |   await expect(page.getByText('System Health')).toBeVisible();
  12 |   await expect(page.getByText('Recent Activity')).toBeVisible();
  13 |   await expect(page.getByText('Getting Started')).toBeVisible();
  14 | });
  15 | 
```