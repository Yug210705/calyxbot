# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth-flow.spec.ts >> Auth Flow Lifecycle >> User can sign up, login, and logout
- Location: tests\e2e\specs\auth-flow.spec.ts:21:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: locator('.bg-emerald-500\\/10')
Expected: visible
Timeout: 10000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 10000ms
  - waiting for locator('.bg-emerald-500\\/10')

```

```yaml
- heading "Join Calyx" [level=1]
- paragraph: Start building your cognitive enterprise.
- text: email rate limit exceeded Full Name
- textbox "Full Name":
  - /placeholder: Ada Lovelace
- text: Email Address
- textbox "Email Address":
  - /placeholder: ada@example.com
- text: Password
- textbox "Password":
  - /placeholder: ••••••••
- button "Create Account"
- text: Already have an account?
- link "Sign in":
  - /url: /login
- alert
```

# Test source

```ts
  1  | import { Page, expect } from '@playwright/test';
  2  | 
  3  | export class SignupPage {
  4  |   readonly page: Page;
  5  | 
  6  |   constructor(page: Page) {
  7  |     this.page = page;
  8  |   }
  9  | 
  10 |   async goto() {
  11 |     await this.page.goto('/signup');
  12 |   }
  13 | 
  14 |   async signup(fullName: string, email: string, password: string) {
  15 |     await this.page.fill('input[name="fullName"]', fullName);
  16 |     await this.page.fill('input[name="email"]', email);
  17 |     await this.page.fill('input[name="password"]', password);
  18 |     await this.page.click('button[type="submit"]');
  19 |   }
  20 | 
  21 |   async expectSuccessMessage() {
  22 |     const successBanner = this.page.locator('.bg-emerald-500\\/10');
> 23 |     await expect(successBanner).toBeVisible({ timeout: 10000 });
     |                                 ^ Error: expect(locator).toBeVisible() failed
  24 |   }
  25 | 
  26 |   async expectError(message: string) {
  27 |     const errorBanner = this.page.locator('.bg-red-500\\/10');
  28 |     await expect(errorBanner).toBeVisible();
  29 |     await expect(errorBanner).toContainText(message);
  30 |   }
  31 | }
  32 | 
```