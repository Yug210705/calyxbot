import { test, expect } from '@playwright/test';

test('documents page renders without crashing', async ({ page }) => {
  await page.goto('/documents');
  
  // Wait for loading to finish
  await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  
  // Check that the table renders
  await expect(page.getByText('Documents')).toBeVisible();
  await expect(page.getByRole('table')).toBeVisible();
});
