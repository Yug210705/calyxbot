import { test, expect } from '@playwright/test';

test('integrations page renders without crashing', async ({ page }) => {
  await page.goto('/integrations');
  
  // Wait for loading to finish
  await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  
  // Check that the shell renders
  await expect(page.getByText('Connected Integrations')).toBeVisible();
  await expect(page.getByText('Available Integrations')).toBeVisible();
});
