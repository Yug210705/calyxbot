import { Page } from '@playwright/test';

export class Navbar {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async logout() {
    // Assuming there's a logout button/link. Adjust selector as needed.
    const logoutBtn = this.page.locator('button', { hasText: 'Sign out' });
    if (await logoutBtn.isVisible()) {
      await logoutBtn.click();
    } else {
      // maybe it's in a form
      await this.page.locator('form[action="/auth/logout"] button').click();
    }
  }
}
