import { test, expect } from '@playwright/test';

test('search page renders and handles queries', async ({ page }) => {
  await page.goto('/search');
  
  // Wait for loading to finish
  await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  
  // Verify empty state
  await expect(page.getByPlaceholder('Ask anything or search your memory...')).toBeVisible();
  await expect(page.getByText('Start typing to search across your documents')).toBeVisible();

  // Trigger search
  await page.getByPlaceholder('Ask anything or search your memory...').fill('test query');
  // the page might auto-search or have a button, assuming auto-search or enter
  await page.keyboard.press('Enter');

  // Verify search loading or results
  await expect(page.getByText('Search Results')).toBeVisible({ timeout: 10000 });
});
