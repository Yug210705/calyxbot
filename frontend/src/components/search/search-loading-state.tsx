export function SearchLoadingState() {
  return (
    <div className="space-y-6 mt-6 w-full max-w-4xl animate-pulse">
      {[1, 2, 3].map((i) => (
        <div key={i} className="flex flex-col gap-3 rounded-xl border bg-card p-5">
          <div className="flex items-center gap-3">
            <div className="h-4 w-1/2 rounded-md bg-muted"></div>
            <div className="h-5 w-16 rounded-full bg-muted"></div>
          </div>
          <div className="flex items-center gap-2">
            <div className="h-4 w-4 rounded bg-muted"></div>
            <div className="h-3 w-32 rounded-md bg-muted"></div>
          </div>
          <div className="space-y-2 mt-2">
            <div className="h-3.5 w-full rounded-md bg-muted"></div>
            <div className="h-3.5 w-5/6 rounded-md bg-muted"></div>
          </div>
        </div>
      ))}
    </div>
  );
}
