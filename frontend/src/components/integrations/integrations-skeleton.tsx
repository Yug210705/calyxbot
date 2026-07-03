export function IntegrationsSkeleton() {
  return (
    <div className="space-y-10 animate-pulse">
      {/* Header Skeleton */}
      <div className="space-y-3">
        <div className="h-8 w-1/4 rounded-md bg-muted"></div>
        <div className="h-4 w-1/3 rounded-md bg-muted"></div>
      </div>
      
      {/* Connected Integrations Skeleton */}
      <div className="space-y-4">
        <div className="h-6 w-48 rounded-md bg-muted"></div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2].map((i) => (
            <div key={i} className="h-48 rounded-xl bg-muted"></div>
          ))}
        </div>
      </div>

      {/* Available Integrations Skeleton */}
      <div className="space-y-4">
        <div className="h-6 w-48 rounded-md bg-muted"></div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-40 rounded-xl bg-muted"></div>
          ))}
        </div>
      </div>
    </div>
  );
}
