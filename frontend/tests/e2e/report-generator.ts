import * as fs from 'fs';
import * as path from 'path';

export function generateAlphaValidationReport() {
  const resultsPath = path.resolve(process.cwd(), 'artifacts/test-results.json');
  const perfPath = path.resolve(process.cwd(), 'artifacts/performance-summary.md');
  const outPath = path.resolve(process.cwd(), '../architecture/product/alpha-validation-report.md');

  let results: Record<string, unknown> = {};
  if (fs.existsSync(resultsPath)) {
    results = JSON.parse(fs.readFileSync(resultsPath, 'utf8'));
  }

  let perfText = 'N/A';
  if (fs.existsSync(perfPath)) {
    perfText = fs.readFileSync(perfPath, 'utf8');
  }

  const passed = Array.isArray(results?.suites) ? results.suites.reduce((acc: number, suite: Record<string, unknown>) => acc + (Array.isArray(suite.specs) ? suite.specs.filter((s: Record<string, unknown>) => s.ok).length : 0), 0) : 0;
  const failed = Array.isArray(results?.suites) ? results.suites.reduce((acc: number, suite: Record<string, unknown>) => acc + (Array.isArray(suite.specs) ? suite.specs.filter((s: Record<string, unknown>) => !s.ok).length : 0), 0) : 0;

  const md = `# Alpha Validation Report - Sprint 1 (Identity Slice)

**Execution Timestamp**: ${new Date().toISOString()}
**Environment**: E2E Suite via Playwright
**Status**: ${(failed > 0 || passed === 0) ? '🔴 BLOCKED' : '✅ READY FOR ORGANIZATIONS'}

## Test Execution Summary
- **Passed**: ${passed}
- **Failed**: ${failed}

## Performance Baseline
${perfText}

## CI/CD Artifacts
- **Screenshots/Videos/Traces**: Retained in \`playwright-report/\` and \`artifacts/\`.

## Recommendation
${(failed > 0 || passed === 0) ? 'Tests failed or skipped. Fix environment credentials before proceeding.' : 'Ready for Organizations.'}
`;

  fs.writeFileSync(outPath, md);
  console.log(`Generated Alpha Validation Report at ${outPath}`);
}

if (require.main === module) {
  generateAlphaValidationReport();
}
