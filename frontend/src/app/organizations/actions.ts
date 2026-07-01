'use server'

import { revalidatePath } from 'next/cache'
import { createClient } from '@/lib/supabase/server'

export async function createOrganization(formData: FormData) {
  const name = formData.get('name') as string
  const slug = formData.get('slug') as string

  if (!name || !slug) {
    return { error: 'Name and slug are required' }
  }

  // Get current user session from Supabase to send to backend
  const supabase = await createClient()
  const { data: { session }, error: sessionError } = await supabase.auth.getSession()

  if (sessionError || !session) {
    return { error: 'Unauthorized' }
  }

  // The backend runs on 8000. 
  // In a real app we'd use process.env.NEXT_PUBLIC_API_URL or similar.
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'
  
  // Use a simple idempotency key based on time or random for now
  const idempotencyKey = crypto.randomUUID()

  try {
    const res = await fetch(`${apiUrl}/api/v1/organizations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.access_token}`,
        'Idempotency-Key': idempotencyKey
      },
      body: JSON.stringify({ name, slug })
    })

    const data = await res.json()

    if (!res.ok) {
      return { error: data?.detail?.error?.message || data?.detail || 'Failed to create organization' }
    }

    revalidatePath('/dashboard')
    // Next.js requires redirect to be called outside try/catch or it will be caught,
    // but in Server Actions, redirect throws an error which Next.js catches internally to perform redirect.
    // So we need to handle it properly or return a success flag and redirect on client.
    return { success: true, orgId: data.data.id }
  } catch (err: unknown) {
    console.error('Error creating organization:', err)
    return { error: err instanceof Error ? err.message : 'An unexpected error occurred' }
  }
}
