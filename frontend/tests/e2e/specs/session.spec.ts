import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { config } from '../config';
import { createTestUser, cleanupTestUser } from '../helpers/auth.helper';

test.describe('Session Edge Cases', () => {
  const email = `session-${Date.now()}@example.com`;
  const password = config.testUserPassword;

  test.beforeEach(async ({ page }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');
    
    // Create the user first via Admin API
    await createTestUser(email, password);

    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(email, password);
  });

  test.afterAll(async () => {
    await cleanupTestUser(email);
  });

  test('Session persists across browser refresh', async ({ page }) => {
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.expectVisible();
    await page.reload();
    await dashboardPage.expectVisible();
  });

  test('Invalid token correctly bounces to login', async ({ page, context }) => {
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.expectVisible();

    // Invalidate the session by clearing cookies
    await context.clearCookies();

    // Reload
    await page.reload();

    // Should redirect to login
    await expect(page).toHaveURL(/.*\/login/);
  });
});
