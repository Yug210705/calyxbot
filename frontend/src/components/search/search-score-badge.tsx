import { cn } from "@/lib/utils";

interface Props {
  score: number;
}

export function SearchScoreBadge({ score }: Props) {
  const percentage = Math.round(score * 100);
  
  let colorClass = "bg-emerald-500/10 text-emerald-500 border-emerald-500/20";
  if (percentage < 70) {
    colorClass = "bg-yellow-500/10 text-yellow-500 border-yellow-500/20";
  }
  if (percentage < 40) {
    colorClass = "bg-red-500/10 text-red-500 border-red-500/20";
  }

  return (
    <span className={cn("inline-flex items-center rounded-md border px-2 py-0.5 text-xs font-semibold", colorClass)}>
      {percentage}% Match
    </span>
  );
}
