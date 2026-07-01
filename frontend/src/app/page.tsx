"use client";

import Link from "next/link";


export default function Home() {
  return (
    <div className="min-h-screen bg-black text-zinc-50 font-sans selection:bg-indigo-500/30">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-black/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <svg className="w-6 h-6 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            <span className="font-bold text-xl tracking-tight">Calyx</span>
          </div>
          <div className="flex items-center gap-4">
            <Link 
              href="/login" 
              className="text-sm font-medium text-zinc-400 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link 
              href="/signup" 
              className="text-sm font-medium bg-white text-black px-4 py-2 rounded-full hover:bg-zinc-200 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="pt-32 pb-16 px-6">
        <div className="max-w-7xl mx-auto text-center mt-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-sm font-medium mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500"></span>
            </span>
            Calyx Alpha is now live
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8">
            The intelligent <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
              engineering knowledge base
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Centralize your architecture decisions, system designs, and institutional memory. Powered by a semantic engine designed specifically for engineering teams.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
              href="/signup" 
              className="group flex items-center gap-2 bg-indigo-500 text-white px-6 py-3 rounded-full font-medium hover:bg-indigo-600 transition-all shadow-[0_0_40px_-10px_rgba(99,102,241,0.5)] hover:shadow-[0_0_60px_-10px_rgba(99,102,241,0.7)]"
            >
              Start for free
              <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </Link>
            <Link 
              href="/login" 
              className="flex items-center gap-2 bg-white/5 text-white border border-white/10 px-6 py-3 rounded-full font-medium hover:bg-white/10 transition-colors"
            >
              Sign In to Workspace
            </Link>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-7xl mx-auto mt-32 grid md:grid-cols-3 gap-6">
          <div className="bg-white/5 border border-white/10 p-8 rounded-3xl hover:bg-white/[0.07] transition-colors group">
            <div className="bg-indigo-500/20 p-3 rounded-2xl w-fit mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </div>
            <h3 className="text-xl font-semibold mb-3">Semantic Memory</h3>
            <p className="text-zinc-400 leading-relaxed">
              Don&apos;t just store documents. Calyx understands relationships between systems, dependencies, and architectural decisions.
            </p>
          </div>
          
          <div className="bg-white/5 border border-white/10 p-8 rounded-3xl hover:bg-white/[0.07] transition-colors group">
            <div className="bg-purple-500/20 p-3 rounded-2xl w-fit mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-purple-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <h3 className="text-xl font-semibold mb-3">Enterprise RBAC</h3>
            <p className="text-zinc-400 leading-relaxed">
              Granular access control ensuring that sensitive architecture designs remain secure across large engineering organizations.
            </p>
          </div>

          <div className="bg-white/5 border border-white/10 p-8 rounded-3xl hover:bg-white/[0.07] transition-colors group">
            <div className="bg-pink-500/20 p-3 rounded-2xl w-fit mb-6 group-hover:scale-110 transition-transform">
              <svg className="w-6 h-6 text-pink-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
            </div>
            <h3 className="text-xl font-semibold mb-3">Instant Retrieval</h3>
            <p className="text-zinc-400 leading-relaxed">
              Find exactly why a decision was made three years ago with sub-second, context-aware search capabilities.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
