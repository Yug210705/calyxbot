import { Page, expect } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async expectVisible() {
    await expect(this.page).toHaveURL(/.*\/dashboard/, { timeout: 15000 });
    await expect(this.page.locator('h1', { hasText: 'Dashboard' })).toBeVisible({ timeout: 15000 });
  }
}
