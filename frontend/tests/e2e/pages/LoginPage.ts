import { Page } from '@playwright/test';

export class LoginPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('input[type="email"]', email);
    await this.page.fill('input[type="password"]', password);
    await this.page.click('button[type="submit"]');
  }

  async expectError(message: string) {
    const errorBanner = this.page.locator('.bg-red-500\\/10');
    await errorBanner.waitFor({ state: 'visible' });
    const text = await errorBanner.innerText();
    if (!text.includes(message)) {
      throw new Error(`Expected error containing "${message}", got "${text}"`);
    }
  }
}
