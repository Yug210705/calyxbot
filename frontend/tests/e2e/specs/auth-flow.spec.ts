import { test, expect } from '@playwright/test';
import { config } from '../config';
import { SignupPage } from '../pages/SignupPage';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { Navbar } from '../pages/Navbar';
import { autoConfirmUser, cleanupTestUser } from '../helpers/auth.helper';

test.describe('Auth Flow Lifecycle', () => {
  let dynamicEmail: string;
  const password = config.testUserPassword;

  test.beforeEach(() => {
    dynamicEmail = `e2e-${Date.now()}-${Math.random().toString(36).substring(7)}@example.com`;
  });

  test.afterEach(async () => {
    await cleanupTestUser(dynamicEmail);
  });

  test('User can sign up, login, and logout', async ({ page }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');

    const signupPage = new SignupPage(page);
    const loginPage = new LoginPage(page);
    const dashboardPage = new DashboardPage(page);
    const navbar = new Navbar(page);

    // 1. Signup
    await signupPage.goto();
    await signupPage.signup('E2E Test User', dynamicEmail, password);
    await signupPage.expectSuccessMessage();
    
    // Depending on whether email confirm is disabled or active:
    // If active, it will show a message. We auto-confirm it in the backend.
    await autoConfirmUser(dynamicEmail);

    // 2. Login
    await loginPage.goto();
    await loginPage.login(dynamicEmail, password);

    // 3. Dashboard Access
    await dashboardPage.expectVisible();

    // 4. Logout
    await navbar.logout();
    await expect(page).toHaveURL(/.*\/login/);
  });
});
