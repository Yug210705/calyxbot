'use client'

import Link from 'next/link'
import { useActionState } from 'react'
import { login } from '@/app/auth/actions'
import { CalyxSubmitButton } from '@/components/CalyxSubmitButton'
import { CalyxInput } from '@/components/CalyxInput'
import { Label } from '@/components/ui/label'

const initialState: { success: boolean; error?: string } = {
  success: false,
}

export default function LoginPage() {
  const [state, formAction] = useActionState(login, initialState)

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-black p-4 relative overflow-hidden">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-500/30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/30 rounded-full blur-3xl animate-pulse delay-1000"></div>

      <div className="relative z-10 w-full max-w-md p-8 rounded-2xl border border-white/10 bg-white/10 dark:bg-black/20 backdrop-blur-xl shadow-2xl">
        <div className="mb-8 text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-white/10 mb-4 shadow-inner">
            <svg className="w-8 h-8 text-fuchsia-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
            </svg>
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2">Welcome Back</h1>
          <p className="text-gray-300">Sign in to your Calyx account.</p>
        </div>

        {state?.error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-200 text-sm">
            {state.error}
          </div>
        )}

        <form action={formAction} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-gray-200">Email Address</Label>
            <CalyxInput 
              id="email" 
              name="email" 
              type="email" 
              placeholder="ada@example.com" 
              required 
              className="bg-white/5 border-white/10 text-white placeholder:text-gray-400 focus-visible:ring-fuchsia-500"
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="password" className="text-gray-200">Password</Label>
              <Link href="#" className="text-xs text-fuchsia-400 hover:text-fuchsia-300 transition-colors">
                Forgot password?
              </Link>
            </div>
            <CalyxInput 
              id="password" 
              name="password" 
              type="password" 
              placeholder="••••••••" 
              required 
              className="bg-white/5 border-white/10 text-white placeholder:text-gray-400 focus-visible:ring-fuchsia-500"
            />
          </div>

          <CalyxSubmitButton className="w-full bg-gradient-to-r from-fuchsia-600 to-indigo-600 hover:from-fuchsia-500 hover:to-indigo-500 text-white font-semibold py-6 rounded-xl transition-all duration-300 shadow-[0_0_20px_rgba(192,38,211,0.3)] hover:shadow-[0_0_30px_rgba(192,38,211,0.5)]">
            Sign In
          </CalyxSubmitButton>
        </form>

        <div className="mt-8 text-center text-sm text-gray-300">
          Don&apos;t have an account?{' '}
          <Link href="/signup" className="text-fuchsia-400 hover:text-fuchsia-300 font-medium transition-colors">
            Create one
          </Link>
        </div>
      </div>
    </div>
  )
}
