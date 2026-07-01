import { expect, Response, APIResponse } from '@playwright/test';

export async function assertSuccessEnvelope(response: Response | APIResponse) {
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body).toHaveProperty('success', true);
  expect(body).toHaveProperty('data');
  return body.data;
}

export async function assertErrorEnvelope(response: Response | APIResponse, expectedStatus: number = 400) {
  expect(response.status()).toBe(expectedStatus);
  const body = await response.json();
  expect(body).toHaveProperty('success', false);
  expect(body).toHaveProperty('error');
  expect(body.error).toHaveProperty('code');
  expect(body.error).toHaveProperty('message');
  expect(body.error).toHaveProperty('request_id');
  return body.error;
}

export function assertRequestId(response: Response | APIResponse) {
  const requestId = response.headers()['x-request-id'];
  expect(requestId).toBeTruthy();
  expect(typeof requestId).toBe('string');
}

export function assertSecurityHeaders(response: Response | APIResponse) {
  const headers = response.headers();
  // Basic security headers that might be set by Next.js or the backend
  if (headers['x-frame-options']) {
    expect(headers['x-frame-options']).toMatch(/SAMEORIGIN|DENY/i);
  }
  if (headers['x-content-type-options']) {
    expect(headers['x-content-type-options']).toBe('nosniff');
  }
}
