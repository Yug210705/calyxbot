import { ApiError } from "./client";

export function shouldFallbackToMock(error: unknown): boolean {
  // If it's our custom ApiError and it has a status code
  if (error instanceof ApiError) {
    // Never fallback on 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
    // The only exception for 404 might be if the API endpoint itself doesn't exist yet, 
    // but the requirement explicitly says "Never fallback on ... 404 for an expected live route"
    if (error.status >= 400 && error.status < 500) {
      return false;
    }
    // Fallback on 5xx
    if (error.status >= 500) {
      return true;
    }
  }

  // Network failures usually come through as TypeError ("Failed to fetch")
  // We can treat anything that isn't explicitly a 4xx ApiError as a candidate for mock fallback 
  // if USE_UI_MOCKS is enabled or if it's a network error.
  
  // For safety, let's say all non-ApiErrors (like network errors) trigger fallback
  return true;
}
