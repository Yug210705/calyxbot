import { DocumentDetail } from "@/lib/types/documents";

interface Props {
  document: DocumentDetail;
}

export function DocumentMetadataPanel({ document }: Props) {
  const metadata = [
    { label: "Document ID", value: document.id },

    { label: "MIME Type", value: document.mime_type },
    { label: "Checksum (SHA-256)", value: document.checksum },
    { 
      label: "Created", 
      value: new Date(document.created_at).toLocaleString([], { 
        dateStyle: 'medium', 
        timeStyle: 'short' 
      }) 
    },
    { 
      label: "Last Updated", 
      value: new Date(document.updated_at).toLocaleString([], { 
        dateStyle: 'medium', 
        timeStyle: 'short' 
      }) 
    },
  ];

  return (
    <div className="rounded-xl border bg-card overflow-hidden">
      <div className="border-b px-6 py-4 bg-muted/20">
        <h3 className="text-sm font-semibold">Metadata</h3>
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
