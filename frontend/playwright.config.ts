import { defineConfig, devices } from '@playwright/test';
import { config as appConfig } from './tests/e2e/config';

export default defineConfig({
  testDir: './tests/e2e/specs',
  fullyParallel: true,
  forbidOnly: appConfig.isCI,
  retries: appConfig.isCI ? 2 : 0,
  workers: appConfig.isCI ? 1 : undefined,
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'artifacts/test-results.json' }]
  ],
  use: {
    baseURL: appConfig.baseUrl,
    trace: 'on-first-retry',
    video: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: appConfig.baseUrl,
    reuseExistingServer: !appConfig.isCI,
  },
  outputDir: 'artifacts/test-results',
});
