import * as path from 'path';
import * as dotenv from 'dotenv';

// Load .env.test if it exists, fallback to .env
const testEnvPath = path.resolve(process.cwd(), '.env.test');
const localEnvPath = path.resolve(process.cwd(), '.env.local');
const defaultEnvPath = path.resolve(process.cwd(), '.env');
const backendEnvPath = path.resolve(process.cwd(), '../backend/.env');

dotenv.config({ path: testEnvPath });
dotenv.config({ path: testEnvPath });
dotenv.config({ path: localEnvPath });
dotenv.config({ path: defaultEnvPath });
dotenv.config({ path: backendEnvPath });

export const config = {
  baseUrl: process.env.BASE_URL || 'http://localhost:3000',
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',
  serviceRoleKey: process.env.SUPABASE_SERVICE_ROLE_KEY || '',
  testUserEmail: process.env.TEST_USER_EMAIL || `test-${Date.now()}@example.com`,
  testUserPassword: process.env.TEST_USER_PASSWORD || 'TestPassword123!',
  testOrgName: process.env.TEST_ORG_NAME || 'Acme Corp Test',
  isCI: process.env.CI === 'true',
  headless: process.env.HEADLESS !== 'false', // default to true
  isMockEnv: !process.env.NEXT_PUBLIC_SUPABASE_URL || process.env.NEXT_PUBLIC_SUPABASE_URL.includes('mock.supabase.co') || process.env.NEXT_PUBLIC_SUPABASE_URL.includes('localhost'),
};
