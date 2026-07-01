'use client'

import Link from 'next/link'
import { useActionState } from 'react'
import { signup } from '@/app/auth/actions'
import { CalyxSubmitButton } from '@/components/CalyxSubmitButton'
import { CalyxInput } from '@/components/CalyxInput'
import { Label } from '@/components/ui/label'

const initialState: { success: boolean; error?: string; message?: string } = {
  success: false,
}

export default function SignupPage() {
  const [state, formAction] = useActionState(signup, initialState)

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-black p-4 relative overflow-hidden">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-500/30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-fuchsia-500/30 rounded-full blur-3xl animate-pulse delay-1000"></div>

      <div className="relative z-10 w-full max-w-md p-8 rounded-2xl border border-white/10 bg-white/10 dark:bg-black/20 backdrop-blur-xl shadow-2xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2">Join Calyx</h1>
          <p className="text-gray-300">Start building your cognitive enterprise.</p>
        </div>

        {state?.error && (
          <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-200 text-sm">
            {state.error}
          </div>
        )}

        {state?.message && !state?.error && (
          <div className="mb-6 p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/50 text-emerald-200 text-sm">
            {state.message}
          </div>
        )}

        <form action={formAction} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="fullName" className="text-gray-200">Full Name</Label>
            <CalyxInput 
              id="fullName" 
              name="fullName" 
              type="text" 
              placeholder="Ada Lovelace" 
              required 
              className="bg-white/5 border-white/10 text-white placeholder:text-gray-400 focus-visible:ring-fuchsia-500"
            />
          </div>

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
            <Label htmlFor="password" className="text-gray-200">Password</Label>
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
            Create Account
          </CalyxSubmitButton>
        </form>

        <div className="mt-8 text-center text-sm text-gray-300">
          Already have an account?{' '}
          <Link href="/login" className="text-fuchsia-400 hover:text-fuchsia-300 font-medium transition-colors">
            Sign in
          </Link>
        </div>
      </div>
    </div>
  )
}
