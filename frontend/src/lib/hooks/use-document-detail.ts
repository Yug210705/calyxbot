import { useState, useCallback } from "react";
import { DocumentDetail } from "../types/documents";
import { getDocumentById } from "../api/documents";

export function useDocumentDetail(orgId: string | undefined) {
  const [selectedDocument, setSelectedDocument] = useState<DocumentDetail | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoadingDetail, setIsLoadingDetail] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const openDocument = useCallback(async (id: string) => {
    if (!orgId) return;
    
    setIsOpen(true);
    setIsLoadingDetail(true);
    setError(null);
    
    // We clear the previous document so the UI shows loading state properly
    // or we could keep it to show stale data while loading.
    setSelectedDocument(null);
    
    try {
      const data = await getDocumentById(id, orgId);
      setSelectedDocument(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to load document details"));
    } finally {
      setIsLoadingDetail(false);
    }
  }, [orgId]);

  const closeDocument = useCallback(() => {
    setIsOpen(false);
    // Optional: delay clearing selectedDocument so the exit animation looks smooth
    setTimeout(() => {
      setSelectedDocument(null);
      setError(null);
    }, 300);
  }, []);

  return {
    selectedDocument,
    isOpen,
    openDocument,
    closeDocument,
    isLoadingDetail,
    error,
  };
}
