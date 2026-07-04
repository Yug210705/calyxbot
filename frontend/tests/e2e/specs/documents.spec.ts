import { test, expect } from '@playwright/test';

test('documents page renders without crashing', async ({ page }) => {
  await page.goto('/documents');
  
  // Wait for loading to finish
  await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  
  // Check that the table renders (using a mock document title instead of table role since it uses divs)
  await expect(page.getByRole('heading', { name: 'Documents', exact: true })).toBeVisible();
  await expect(page.getByText('Engineering Onboarding Handbook 2024')).toBeVisible();
});
