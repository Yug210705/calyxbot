import { type NextRequest, NextResponse } from 'next/server'
import { createServerClient } from '@supabase/ssr'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  })

  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
  const isMockUi = process.env.NEXT_PUBLIC_USE_UI_MOCKS === "true";

  // If Supabase environment variables are missing, assume we are in a mock/demo environment
  // and bypass the authentication checks to prevent the middleware from crashing.
  if (!supabaseUrl || !supabaseKey || isMockUi || supabaseUrl === 'https://mock.supabase.co') {
    console.warn('Bypassing auth (Missing credentials or Mock environment detected).');
    return supabaseResponse;
  }

  const supabase = createServerClient(
    supabaseUrl,
    supabaseKey,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value))
          supabaseResponse = NextResponse.next({
            request,
          })
          cookiesToSet.forEach(({ name, value, options: cookieOptions }) =>
            supabaseResponse.cookies.set(name, value, cookieOptions)
          )
        },
      },
    }
  )

  const {
    data: { user },
  } = await supabase.auth.getUser()

  // Protected routes
  const isMockEnv = process.env.USE_MOCK_ENV === 'true';
  const protectedRoutes = ['/dashboard', '/integrations', '/documents', '/search', '/settings'];
  const isProtected = protectedRoutes.some(route => request.nextUrl.pathname.startsWith(route));
  
  if (!isMockEnv && isProtected && !user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // If user is logged in, don't let them visit login/signup
  if ((request.nextUrl.pathname.startsWith('/login') || request.nextUrl.pathname.startsWith('/signup')) && user) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return supabaseResponse
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * Feel free to modify this pattern to include more paths.
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
