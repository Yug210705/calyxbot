import { ProcessingTimelineItem } from "@/lib/types/documents";
import { Check, Circle, Loader2, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface Props {
  timeline: ProcessingTimelineItem[];
}

export function DocumentProcessingTimeline({ timeline }: Props) {
  if (!timeline || timeline.length === 0) return null;

  return (
    <div className="rounded-xl border bg-card p-6">
      <h3 className="text-sm font-semibold mb-6">Processing Pipeline</h3>
      
      <div className="relative border-l border-muted ml-3 space-y-6">
        {timeline.map((stage) => {
          const isCompleted = stage.status === "completed";
          const isCurrent = stage.status === "current";
          const isStageFailed = stage.status === "failed";
          
          return (
            <div key={stage.key} className="relative pl-6">
              <div className={cn(
                "absolute -left-[11px] top-0.5 flex h-[22px] w-[22px] items-center justify-center rounded-full border-2 bg-background",
                isCompleted ? "border-primary bg-primary text-primary-foreground" : 
                isCurrent ? "border-primary text-primary" : 
                isStageFailed ? "border-red-500 text-red-500" :
                "border-muted text-muted-foreground"
              )}>
                {isCompleted ? <Check className="h-3 w-3" /> :
                 isCurrent ? <Loader2 className="h-3 w-3 animate-spin" /> :
                 isStageFailed ? <X className="h-3 w-3" /> :
                 <Circle className="h-2 w-2 fill-current opacity-20" />}
              </div>
              <div>
                <p className={cn(
                  "text-sm font-medium",
                  isCompleted ? "text-foreground" : 
                  isCurrent ? "text-primary" : 
                  isStageFailed ? "text-red-500" :
                  "text-muted-foreground"
                )}>
                  {stage.label}
                </p>
                {stage.timestamp && (
                  <p className="text-xs text-muted-foreground mt-1">
                    {new Date(stage.timestamp).toLocaleString([], { 
                      dateStyle: 'short', 
                      timeStyle: 'short' 
                    })}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
