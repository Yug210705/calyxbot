import { SearchResultItem } from "@/lib/types/search";

interface Props {
  result: SearchResultItem;
}

export function SearchResultMetadata({ result }: Props) {
  const metadata = [
    { label: "Document ID", value: result.document_id },
    { label: "Chunk ID", value: result.chunk_id },
    { label: "Status", value: result.document_status || "Unknown" },
  ];

  return (
    <div className="rounded-xl border bg-card overflow-hidden">
      <div className="border-b px-6 py-4 bg-muted/20">
        <h3 className="text-sm font-semibold">Source Metadata</h3>
      </div>
      <div className="divide-y text-sm">
        {metadata.map((item, i) => (
          <div key={i} className="flex flex-col sm:flex-row sm:items-center py-3 px-6 gap-1 sm:gap-4">
            <span className="text-muted-foreground w-1/3 shrink-0">{item.label}</span>
            <span className="font-medium truncate" title={item.value}>{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
