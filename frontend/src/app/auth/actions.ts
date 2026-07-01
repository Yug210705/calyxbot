'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { createClient } from '@/lib/supabase/server'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
})

const signupSchema = z.object({
  fullName: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

export async function login(prevState: unknown, formData: FormData) {
  const supabase = await createClient()
  
  const email = formData.get('email') as string
  const password = formData.get('password') as string

  const parsed = loginSchema.safeParse({ email, password })
  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message }
  }

  const { error, data } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  if (error) {
    return { success: false, error: error.message }
  }

  const token = data.session.access_token
  
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/complete-signup`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    })
    if (!res.ok) {
      console.error("Failed to sync login with backend:", await res.text())
    }
  } catch (err) {
    console.error("Failed to reach backend:", err)
  }

  revalidatePath('/', 'layout')
  redirect('/dashboard')
}

export async function signup(prevState: unknown, formData: FormData) {
  const supabase = await createClient()
  
  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const fullName = formData.get('fullName') as string

  const parsed = signupSchema.safeParse({ email, password, fullName })
  if (!parsed.success) {
    return { success: false, error: parsed.error.issues[0].message }
  }

  const { error, data } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        name: fullName
      }
    }
  })

  if (error) {
    return { success: false, error: error.message }
  }
  
  if (data?.session?.access_token) {
    const token = data.session.access_token
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/complete-signup`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          full_name: fullName
        })
      })
      if (!res.ok) {
        console.error("Failed to sync signup with backend:", await res.text())
      }
    } catch (err) {
      console.error("Failed to reach backend:", err)
    }
    revalidatePath('/', 'layout')
    redirect('/dashboard')
  }

  return { success: true, message: "Check your email to confirm your account." }
}

export async function logout() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  redirect('/login')
}
