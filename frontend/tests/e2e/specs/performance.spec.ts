import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { config } from '../config';
import * as fs from 'fs';
import * as path from 'path';
import { createTestUser, cleanupTestUser } from '../helpers/auth.helper';
import { DashboardPage } from '../pages/DashboardPage';

test.describe('Performance Baselines', () => {
  const email = `perf-${Date.now()}@example.com`;
  
  test.afterAll(async () => {
    await cleanupTestUser(email);
  });

  test('Login and /auth/me latency', async ({ page }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');
    
    await createTestUser(email, config.testUserPassword);

    const loginPage = new LoginPage(page);
    await loginPage.goto();

    const startTime = performance.now();
    await loginPage.login(email, config.testUserPassword);
    
    const dashboardPage = new DashboardPage(page);
    await dashboardPage.expectVisible();
    
    const endTime = performance.now();
    const latency = endTime - startTime;

    console.log(`[Performance] Login round-trip latency: ${latency.toFixed(2)}ms`);

    // Output to performance-report.json
    const reportPath = path.resolve(process.cwd(), 'artifacts/performance-report.json');
    const mdPath = path.resolve(process.cwd(), 'artifacts/performance-summary.md');

    // Create artifacts dir if missing
    if (!fs.existsSync(path.dirname(reportPath))) {
      fs.mkdirSync(path.dirname(reportPath), { recursive: true });
    }

    const report = {
      timestamp: new Date().toISOString(),
      loginRoundtripMs: latency
    };
    
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

    const mdReport = `# Performance Summary\n\n- **Login Roundtrip**: ${latency.toFixed(2)}ms\n- **Timestamp**: ${report.timestamp}\n`;
    fs.writeFileSync(mdPath, mdReport);

    // Soft assertion: emit warning if close to threshold
    const WARNING_THRESHOLD = 5000;
    const ERROR_THRESHOLD = 25000;

    if (latency > WARNING_THRESHOLD && latency <= ERROR_THRESHOLD) {
      console.warn(`⚠️ Latency warning: ${latency.toFixed(2)}ms exceeds ${WARNING_THRESHOLD}ms`);
    }

    // Hard fail if significantly exceeded
    expect(latency, 'Latency should not exceed hard threshold').toBeLessThanOrEqual(ERROR_THRESHOLD);
  });
});
