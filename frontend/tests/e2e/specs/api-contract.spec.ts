/* eslint-disable @typescript-eslint/no-unused-vars */
import { test } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { SignupPage } from '../pages/SignupPage';
import { config } from '../config';
import { cleanupTestUser, createTestUser } from '../helpers/auth.helper';
import { assertSuccessEnvelope, assertRequestId } from '../helpers/api.helper';

test.describe('Unified API Contract', () => {
  test('Backend returns unified format on /auth/me', async ({ request }) => {
    test.skip(config.isMockEnv, 'Skipping test because Supabase is not configured.');
    
    const email = `api-${Date.now()}@example.com`;
    const password = config.testUserPassword;
    
    // Create the test user via Admin API to bypass email rate limits
    await createTestUser(email, password);

    const authRes = await request.post(`${config.supabaseUrl}/auth/v1/token?grant_type=password`, {
      headers: {
        'apikey': config.supabaseAnonKey,
        'Content-Type': 'application/json'
      },
      data: {
        email,
        password
      }
    });
    const authBody = await authRes.json();
    console.log("Auth Response:", authBody);
    const { access_token } = authBody;

    const apiResponse = await request.get(`${config.apiUrl}/api/v1/auth/me`, {
      headers: {
        Authorization: `Bearer ${access_token}`
      }
    });
    if (!apiResponse.ok()) {
      console.log("API Response:", await apiResponse.text());
    }
    await assertSuccessEnvelope(apiResponse);
    assertRequestId(apiResponse);
    
    await cleanupTestUser(email);
  });
});
