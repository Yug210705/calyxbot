export function DocumentsSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header Skeleton */}
      <div className="flex justify-between items-center mb-8">
        <div className="space-y-3">
          <div className="h-8 w-48 rounded-md bg-muted"></div>
          <div className="h-4 w-64 rounded-md bg-muted"></div>
        </div>
      </div>
      
      {/* Filters Skeleton */}
      <div className="flex gap-4 mb-6">
        <div className="h-10 w-full max-w-sm rounded-md bg-muted"></div>
        <div className="h-10 w-32 rounded-md bg-muted"></div>
        <div className="h-10 w-32 rounded-md bg-muted"></div>
      </div>

      {/* Table Skeleton */}
      <div className="rounded-xl border bg-card overflow-hidden">
        <div className="border-b px-6 py-4 bg-muted/20">
          <div className="h-5 w-full rounded-md bg-muted"></div>
        </div>
        <div className="divide-y">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="flex items-center justify-between p-4">
              <div className="flex items-center gap-4 w-1/3">
                <div className="h-10 w-10 rounded-lg bg-muted"></div>
                <div className="space-y-2 w-full">
                  <div className="h-4 w-3/4 rounded-md bg-muted"></div>
                  <div className="h-3 w-1/2 rounded-md bg-muted"></div>
                </div>
              </div>
              <div className="h-6 w-24 rounded-full bg-muted"></div>
              <div className="h-4 w-16 rounded-md bg-muted"></div>
              <div className="h-4 w-24 rounded-md bg-muted"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
