import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });
dotenv.config({ path: '../backend/.env' });

const url = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;
const adminKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const supabase = createClient(url, key);

async function run() {
  const email = `test-${Date.now()}@example.com`;
  const password = 'TestPassword123!';
  
  console.log('Signing up...');
  const { error: signupError } = await supabase.auth.signUp({
    email,
    password,
    options: { data: { full_name: 'Test' } }
  });
  console.log('Signup Result:', signupError ? signupError.message : 'Success');
  
  console.log('Auto confirming...');
  const res = await fetch(`${url}/auth/v1/admin/users`, {
    headers: { 'Authorization': `Bearer ${adminKey}`, 'apikey': adminKey }
  });
  const users = await res.json();
  const user = users.users.find((u: { email: string; id: string }) => u.email === email);
  if (user) {
    const confirmRes = await fetch(`${url}/auth/v1/admin/users/${user.id}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${adminKey}`, 'apikey': adminKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email_confirm: true })
    });
    console.log('Confirm status:', confirmRes.status);
  } else {
    console.log('User not found in admin API!');
  }
  
  console.log('Signing in...');
  const { error: signinError } = await supabase.auth.signInWithPassword({
    email, password
  });
  console.log('Signin Result:', signinError ? signinError.message : 'Success');
}

run();
