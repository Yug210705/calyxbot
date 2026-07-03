import { apiFetch } from "./client";
import { DocumentListItem, DocumentDetail, DocumentListResponse } from "../types/documents";
import { mockDocumentsList, mockDocumentDetails } from "../mocks/documents";
import { shouldFallbackToMock } from "./fallback";

const USE_UI_MOCKS = process.env.NEXT_PUBLIC_USE_UI_MOCKS === "true";

export type GetDocumentsFilters = {
  q?: string;
  provider?: string;
  status?: string;
  limit?: number;
  offset?: number;
};

export async function getDocuments(orgId: string, filters?: GetDocumentsFilters): Promise<DocumentListResponse> {
  try {
    const query = new URLSearchParams();
    if (filters?.q) query.append("q", filters.q);
    if (filters?.provider && filters.provider !== "all") query.append("provider", filters.provider);
    if (filters?.status && filters.status !== "all") query.append("status", filters.status);
    if (filters?.limit) query.append("limit", filters.limit.toString());
    if (filters?.offset) query.append("offset", filters.offset.toString());
    
    const queryString = query.toString();
    const endpoint = `/documents${queryString ? `?${queryString}` : ""}`;
    
    return await apiFetch<DocumentListResponse>(endpoint, { 
      headers: { "X-Organization-Id": orgId }
    });
  } catch (error) {
    if (USE_UI_MOCKS || shouldFallbackToMock(error)) {
      console.warn("Real API failed, falling back to mock data for documents list", error);
      return {
        items: mockDocumentsList as any, // Mock data format might slightly differ but it's a fallback
        total: mockDocumentsList.length,
        page: 1,
        size: 50
      };
    }
    throw error;
  }
}

export async function getDocumentById(id: string, orgId: string): Promise<DocumentDetail> {
  try {
    return await apiFetch<DocumentDetail>(`/documents/${id}`, { 
      headers: { "X-Organization-Id": orgId }
    });
  } catch (error) {
    if (USE_UI_MOCKS || shouldFallbackToMock(error)) {
      console.warn("Real API failed, falling back to mock data for document detail", error);
      const mockDetail = mockDocumentDetails[id];
      if (mockDetail) return mockDetail as any;
      throw new Error("Document not found");
    }
    throw error;
  }
}
