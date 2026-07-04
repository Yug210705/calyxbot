import { test, expect } from '@playwright/test';

test('search page renders and handles queries', async ({ page }) => {
  await page.goto('/search');
  
  // Wait for loading to finish
  await expect(page.locator('.animate-pulse')).toHaveCount(0, { timeout: 10000 });
  
  // Verify empty state
  await expect(page.getByPlaceholder('Ask a question or search for concepts...')).toBeVisible();
  await expect(page.getByText('Type a query to search across all your connected documents, chunks, and extracted knowledge objects.')).toBeVisible();

  // Trigger search
  await page.getByPlaceholder('Ask a question or search for concepts...').fill('test query');
  await page.getByRole('button', { name: 'Search' }).click();
  await page.keyboard.press('Enter');

  // Verify search loading or results
  await expect(page.getByText('results for')).toBeVisible({ timeout: 10000 });
});
