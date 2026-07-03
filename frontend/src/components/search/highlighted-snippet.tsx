/* eslint-disable @typescript-eslint/no-unused-vars */
import { cn } from "@/lib/utils";
import React from "react";

type HighlightedSnippetProps = {
  text: string;
  query: string;
  className?: string;
};

export function HighlightedSnippet({ text, query, className }: HighlightedSnippetProps) {
  if (!query.trim()) {
    return <span className={className}>{text}</span>;
  }

  // Split query into words, filter out empty ones
  const terms = query
    .toLowerCase()
    .split(/\s+/)
    .filter((t) => t.length > 2); // Ignore very short words like "a", "of", "in"

  if (terms.length === 0) {
    return <span className={className}>{text}</span>;
  }

  // Create a regex that matches any of the terms, case-insensitive
  const escapedTerms = terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const regex = new RegExp(`(${escapedTerms.join('|')})`, 'gi');

  const parts = text.split(regex);

  return (
    <span className={className}>
      {parts.map((part, i) => {
        const isMatch = terms.some((term) => part.toLowerCase() === term);
        return isMatch ? (
          <mark key={i} className="bg-primary/20 text-foreground font-semibold rounded-sm px-0.5 py-0.5">
            {part}
          </mark>
        ) : (
          <React.Fragment key={i}>{part}</React.Fragment>
        );
      })}
    </span>
  );
}
