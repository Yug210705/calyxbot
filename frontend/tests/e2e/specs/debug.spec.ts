/* eslint-disable @typescript-eslint/no-unused-vars */
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { config } from '../config';
import { createTestUser, cleanupTestUser } from '../helpers/auth.helper';

test.describe('Debug Login', () => {
  test.beforeAll(async () => {
    await createTestUser(config.testUserEmail, config.testUserPassword);
  });

  test.afterAll(async () => {
    await cleanupTestUser(config.testUserEmail);
  });

  test('debug login', async ({ page }) => {
    page.on('response', response => console.log(`<< ` + response.status() + ` ` + response.url()));
    page.on('console', msg => console.log(`BROWSER CONSOLE: ` + msg.text()));

    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(config.testUserEmail, config.testUserPassword);
    
    await page.waitForTimeout(6000); // Wait explicitly to see what happens
  });
});
