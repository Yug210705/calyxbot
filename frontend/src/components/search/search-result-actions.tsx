import { Button } from "@/components/ui/button";
import { SearchResultItem } from "@/lib/types/search";
import { Copy, Link as LinkIcon, Check } from "lucide-react";
import { useState } from "react";
import { toastSuccess, toastError } from "@/components/ui/app-toast";

interface Props {
  result: SearchResultItem;
}

export function SearchResultActions({ result }: Props) {
  const [copiedSnippet, setCopiedSnippet] = useState(false);
  const [copiedMeta, setCopiedMeta] = useState(false);

  const handleCopySnippet = async () => {
    try {
      await navigator.clipboard.writeText(result.snippet);
      setCopiedSnippet(true);
      toastSuccess("Snippet copied to clipboard");
      setTimeout(() => setCopiedSnippet(false), 2000);
    } catch (error) {
      toastError("Failed to copy snippet");
    }
  };

  const handleCopyMeta = async () => {
    try {
      const text = [
        `Document: ${result.document_title}`,
        `Provider: ${result.provider}`,
        `Source: ${result.source}`,
        result.section_heading ? `Heading: ${result.section_heading}` : "",
        result.page_number ? `Page: ${result.page_number}` : "",
        `Chunk ID: ${result.chunk_id}`,
        `Document ID: ${result.document_id}`,
      ].filter(Boolean).join("\n");
      
      await navigator.clipboard.writeText(text);
      setCopiedMeta(true);
      toastSuccess("Source info copied to clipboard");
      setTimeout(() => setCopiedMeta(false), 2000);
    } catch (error) {
      toastError("Failed to copy source info");
    }
  };

  return (
    <div className="flex gap-2">
      <Button 
        variant="outline" 
        size="sm" 
        onClick={handleCopySnippet}
        className="h-8 gap-1.5"
      >
        {copiedSnippet ? <Check className="h-3.5 w-3.5 text-green-500" /> : <Copy className="h-3.5 w-3.5" />}
        <span className="text-xs">Copy snippet</span>
      </Button>
      
      <Button 
        variant="outline" 
        size="sm" 
        onClick={handleCopyMeta}
        className="h-8 gap-1.5"
      >
        {copiedMeta ? <Check className="h-3.5 w-3.5 text-green-500" /> : <LinkIcon className="h-3.5 w-3.5" />}
        <span className="text-xs">Copy source info</span>
      </Button>
    </div>
  );
}
