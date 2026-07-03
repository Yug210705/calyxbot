import { DashboardChecklistItem } from "@/lib/types/dashboard";
import { CheckCircle2, Circle } from "lucide-react";
import Link from "next/link";

interface Props {
  checklist: DashboardChecklistItem[];
}

export function OnboardingChecklist({ checklist }: Props) {
  const completedCount = checklist.filter(c => c.completed).length;
  const totalCount = checklist.length;
  const progressPercentage = totalCount === 0 ? 0 : Math.round((completedCount / totalCount) * 100);

  if (checklist.length === 0) return null;

  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
      <div className="p-6 pb-4 flex items-center justify-between">
        <div>
          <h3 className="font-semibold leading-none tracking-tight">Getting Started</h3>
          <p className="text-sm text-muted-foreground mt-1.5">{completedCount} of {totalCount} tasks completed</p>
        </div>
        <div className="h-10 w-10 shrink-0 flex items-center justify-center rounded-full bg-primary/10 text-primary text-xs font-bold">
          {progressPercentage}%
        </div>
      </div>
      <div className="p-6 pt-0 space-y-4">
        {checklist.map(item => (
          <div key={item.id} className="flex gap-3">
            <div className="mt-0.5">
              {item.completed ? (
                <CheckCircle2 className="h-5 w-5 text-green-500" />
              ) : (
                <Circle className="h-5 w-5 text-muted-foreground opacity-30" />
              )}
            </div>
            <div className="flex-1 space-y-1">
              <div className="flex items-center">
                {item.href && !item.completed ? (
                  <Link href={item.href} className="text-sm font-medium hover:underline decoration-primary underline-offset-4">
                    {item.label}
                  </Link>
                ) : (
                  <p className={`text-sm font-medium ${item.completed ? 'text-muted-foreground line-through' : ''}`}>
                    {item.label}
                  </p>
                )}
              </div>
              {item.description && (
                <p className="text-xs text-muted-foreground">{item.description}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
