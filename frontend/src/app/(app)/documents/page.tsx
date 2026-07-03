"use client";

import { useState } from "react";
import { useDocuments } from "@/lib/hooks/use-documents";
import { useDocumentDetail } from "@/lib/hooks/use-document-detail";
import { DocumentsHeader } from "@/components/documents/documents-header";
import { DocumentsFilters } from "@/components/documents/documents-filters";
import { DocumentsTable } from "@/components/documents/documents-table";
import { DocumentDetailSheet } from "@/components/documents/document-detail-sheet";
import { DocumentsSkeleton } from "@/components/documents/documents-skeleton";
import { DocumentsErrorState } from "@/components/documents/documents-error-state";
import { DocumentsEmptyState } from "@/components/documents/documents-empty-state";
import { DocumentsNoResultsState } from "@/components/documents/documents-no-results-state";

export default function DocumentsPage() {
  const orgId = "00000000-0000-0000-0000-000000000001";
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Hook for main list and filtering
  const {
    documents,
    filteredDocuments,
    search,
    providerFilter,
    statusFilter,
    setSearch,
    setProviderFilter,
    setStatusFilter,
    isLoading,
    error,
    refresh
  } = useDocuments(orgId);

  // Hook for detail sheet
  const {
    selectedDocument,
    isOpen,
    openDocument,
    closeDocument,
    isLoadingDetail
  } = useDocumentDetail(orgId);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await refresh();
    setIsRefreshing(false);
  };

  const handleClearFilters = () => {
    setSearch("");
    setProviderFilter("all");
    setStatusFilter("all");
  };

  // 1. Initial Loading State
  if (isLoading) {
    return <DocumentsSkeleton />;
  }

  // 2. Error State
  if (error) {
    return <DocumentsErrorState onRetry={handleRefresh} message={error.message} />;
  }

  // 3. Absolute Empty State (no documents exist at all)
  if (documents.length === 0) {
    return (
      <div className="space-y-6 pb-8">
        <DocumentsHeader onRefresh={handleRefresh} isRefreshing={isRefreshing} />
        <DocumentsEmptyState />
      </div>
    );
  }

  // 4. Main UI
  return (
    <div className="space-y-6 pb-8">
      <DocumentsHeader onRefresh={handleRefresh} isRefreshing={isRefreshing} />
      
      <DocumentsFilters 
        search={search}
        onSearchChange={setSearch}
        providerFilter={providerFilter}
        onProviderChange={setProviderFilter}
        statusFilter={statusFilter}
        onStatusChange={setStatusFilter}
      />

      {/* Conditionally render table or no-results state */}
      {filteredDocuments.length === 0 ? (
        <DocumentsNoResultsState onClearFilters={handleClearFilters} />
      ) : (
        <DocumentsTable 
          documents={filteredDocuments} 
          onDocumentClick={openDocument} 
        />
      )}

      {/* Detail Sheet Overlay */}
      <DocumentDetailSheet 
        document={selectedDocument}
        isOpen={isOpen}
        onClose={closeDocument}
        isLoading={isLoadingDetail}
      />
    </div>
  );
}
