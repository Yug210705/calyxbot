'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createOrganization } from '@/app/organizations/actions'
import { CalyxButton } from '@/components/CalyxButton'

export function OrganizationForm() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  
  const [name, setName] = useState('')
  const [slug, setSlug] = useState('')
  
  // Auto-generate slug from name
  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newName = e.target.value
    setName(newName)
    // Basic slugification: lowercase, replace spaces and non-alphanumeric with hyphen
    setSlug(newName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, ''))
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    
    const formData = new FormData()
    formData.append('name', name)
    formData.append('slug', slug)
    
    const res = await createOrganization(formData)
    
    if (res?.error) {
      setError(res.error)
      setLoading(false)
    } else if (res?.success) {
      router.push('/dashboard')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {error}
        </div>
      )}
      
      <div className="space-y-2">
        <label htmlFor="name" className="block text-sm font-medium text-gray-300">
          Organization Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          value={name}
          onChange={handleNameChange}
          placeholder="e.g. Acme Corp"
          required
          disabled={loading}
          className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="slug" className="block text-sm font-medium text-gray-300">
          Organization URL Slug
        </label>
        <div className="flex items-center">
          <span className="px-4 py-3 bg-white/5 border border-white/10 border-r-0 rounded-l-lg text-gray-500 text-sm whitespace-nowrap">
            calyx.ai/
          </span>
          <input
            id="slug"
            name="slug"
            type="text"
            value={slug}
            onChange={(e) => setSlug(e.target.value)}
            placeholder="acme-corp"
            required
            pattern="^[a-z0-9-]+$"
            disabled={loading}
            className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-r-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
          />
        </div>
        <p className="text-xs text-gray-500 mt-1">This will be your workspace URL. Only lowercase letters, numbers, and hyphens allowed.</p>
      </div>

      <CalyxButton 
        type="submit" 
        className="w-full py-3 text-lg mt-8"
        disabled={loading || !name || !slug}
      >
        {loading ? (
          <div className="flex items-center justify-center space-x-2">
            <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
            <span>Creating...</span>
          </div>
        ) : 'Create Organization'}
      </CalyxButton>
    </form>
  )
}
