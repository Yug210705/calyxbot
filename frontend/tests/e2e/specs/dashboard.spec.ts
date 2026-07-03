import { test, expect } from '@playwright/test';

test('dashboard page renders without crashing', async ({ page }) => {
  await page.goto('/dashboard');
  
  // Wait for loading to finish
  await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  
  // Check that key sections are rendered
  await expect(page.getByText('Connected Sources')).toBeVisible();
  await expect(page.getByText('System Health')).toBeVisible();
  await expect(page.getByText('Recent Activity')).toBeVisible();
  await expect(page.getByText('Getting Started')).toBeVisible();
});
