import { logout } from '@/app/auth/actions'
import { CalyxButton } from '@/components/CalyxButton'

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <form action={logout}>
            <CalyxButton type="submit" variant="destructive">
              Sign out
            </CalyxButton>
          </form>
        </div>
        
        <div className="p-8 rounded-xl border border-white/10 bg-white/5">
          <p className="text-gray-400">Welcome to Calyx. Your cognitive enterprise begins here.</p>
        </div>
      </div>
    </div>
  )
}
