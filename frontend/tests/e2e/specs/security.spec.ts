import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { config } from '../config';
import { assertSecurityHeaders } from '../helpers/api.helper';
import { createTestUser, cleanupTestUser } from '../helpers/auth.helper';

test.describe('Security & Hardening', () => {
  test.beforeAll(async () => {
    await createTestUser(config.testUserEmail, config.testUserPassword);
  });

  test.afterAll(async () => {
    await cleanupTestUser(config.testUserEmail);
  });

  test('Unauthenticated user is bounced from /dashboard', async ({ page }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/.*\/login/);
  });

  test('Authenticated user is bounced from /login', async ({ page }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(config.testUserEmail, config.testUserPassword);
    
    // Wait for login to complete and redirect to dashboard
    await expect(page).toHaveURL(/.*\/dashboard/, { timeout: 15000 });
    
    // Attempt to go back to login
    await page.goto('/login');
    await expect(page).toHaveURL(/.*\/dashboard/, { timeout: 15000 });
  });

  test('Backend responses contain baseline security headers', async ({ request }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');
    // We can directly hit a backend API endpoint to assert security headers
    const apiResponse = await request.get(`${config.apiUrl}/api/v1/auth/me`);
    assertSecurityHeaders(apiResponse);
  });
});
