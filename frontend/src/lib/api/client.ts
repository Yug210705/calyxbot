/* eslint-disable @typescript-eslint/no-explicit-any */
export type ApiOptions = RequestInit & {
  organizationId?: string;
};

export class ApiError extends Error {
  status: number;
  data: any;

  constructor(status: number, message: string, data?: any) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = "ApiError";
  }
}

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function apiFetch<T>(path: string, options: ApiOptions = {}): Promise<T> {
  const { organizationId, headers, ...rest } = options;

  const requestHeaders = new Headers(headers);
  requestHeaders.set("Content-Type", "application/json");

  // In a real app, attach auth token here
  // const token = await getAuthToken();
  // if (token) requestHeaders.set("Authorization", `Bearer ${token}`);

  if (organizationId) {
    requestHeaders.set("X-Organization-Id", organizationId);
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...rest,
    headers: requestHeaders,
  });

  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      errorData = { message: response.statusText };
    }
    throw new ApiError(response.status, errorData.message || "An error occurred", errorData);
  }

  // Handle empty responses
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}
