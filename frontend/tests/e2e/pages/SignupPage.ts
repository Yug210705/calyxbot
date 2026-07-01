import { Page, expect } from '@playwright/test';

export class SignupPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/signup');
  }

  async signup(fullName: string, email: string, password: string) {
    await this.page.fill('input[name="fullName"]', fullName);
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }

  async expectSuccessMessage() {
    const successBanner = this.page.locator('.bg-emerald-500\\/10');
    await expect(successBanner).toBeVisible({ timeout: 10000 });
  }

  async expectError(message: string) {
    const errorBanner = this.page.locator('.bg-red-500\\/10');
    await expect(errorBanner).toBeVisible();
    await expect(errorBanner).toContainText(message);
  }
}
