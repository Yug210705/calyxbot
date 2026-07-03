/* eslint-disable @typescript-eslint/no-unused-vars */
import { SearchResultItem } from "../types/search";

const now = new Date().toISOString();

const mockResultsStore: Record<string, SearchResultItem[]> = {
  incident: [
    {
      chunk_id: "chunk-inc-1",
      document_id: "doc-3",
      document_title: "Incident Postmortem: SEV-1 Database Outage",
      provider: "google_drive",
      source: "SRE Shared Drive",
      score: 0.94,
      section_heading: "Root Cause Analysis",
      page_number: 2,
      document_status: "READY",
      snippet: "...the primary Postgres cluster became unresponsive due to connection exhaustion. The root cause was identified as a runaway sync job that failed to release database connections during a retry loop. This led to a 45-minute total outage of the ingestion pipeline. Immediate remediation involved...",
    },
    {
      chunk_id: "chunk-inc-2",
      document_id: "doc-15",
      document_title: "Incident Response Playbook",
      provider: "notion",
      source: "Engineering Wiki",
      score: 0.88,
      section_heading: "Declaring an Incident",
      document_status: "READY",
      snippet: "...To declare a SEV-1 or SEV-2 incident, use the `/incident` Slack command in the #engineering channel. This will automatically page the on-call engineer, create a dedicated incident channel, and start a Zoom bridge. Do not attempt to debug silently without...",
    },
    {
      chunk_id: "chunk-inc-3",
      document_id: "doc-5",
      document_title: "Customer Escalation: ACME Corp Integration",
      provider: "slack",
      source: "#escalations-acme",
      score: 0.72,
      document_status: "READY",
      snippet: "...ACME Corp is reporting 500 errors on the new integration endpoint. I've looked at the Datadog logs and it seems related to the recent database incident. Are we still seeing connection drops? We need to update them by EOD...",
    }
  ],
  onboarding: [
    {
      chunk_id: "chunk-onb-1",
      document_id: "doc-1",
      document_title: "Engineering Onboarding Handbook 2024",
      provider: "google_drive",
      source: "Engineering Hub",
      score: 0.95,
      section_heading: "Local Environment Setup",
      page_number: 3,
      document_status: "READY",
      snippet: "...Welcome to Engineering! To get your local environment running, first ensure you have Docker and Homebrew installed. Run `make setup` in the root of the calyx-backend repository. This will spin up the Postgres and Redis containers, run the initial migrations, and seed...",
    },
    {
      chunk_id: "chunk-onb-2",
      document_id: "doc-1",
      document_title: "Engineering Onboarding Handbook 2024",
      provider: "google_drive",
      source: "Engineering Hub",
      score: 0.89,
      section_heading: "Access Requests",
      page_number: 7,
      document_status: "READY",
      snippet: "...For production AWS access, submit a request through the Okta portal. You will need manager approval. Temporary elevation to production requires a JIRA ticket number. GitHub admin access is restricted to the infra team...",
    }
  ],
  sprint: [
    {
      chunk_id: "chunk-spr-1",
      document_id: "doc-2",
      document_title: "Q3 Sprint Planning Notes",
      provider: "notion",
      source: "Product Team",
      score: 0.91,
      section_heading: "Sprint 4: Search Improvements",
      document_status: "READY",
      snippet: "...The primary goal for Sprint 4 is to replace the naive chunker with a recursive markdown-aware chunker. This should improve retrieval quality significantly. If we finish early, we will look into adding a reranking step using Cohere's API...",
    },
    {
      chunk_id: "chunk-spr-2",
      document_id: "doc-2",
      document_title: "Q3 Sprint Planning Notes",
      provider: "notion",
      source: "Product Team",
      score: 0.85,
      section_heading: "Sprint 5: Connectors",
      document_status: "READY",
      snippet: "...Sprint 5 will focus on expanding our connector ecosystem. We need to finalize the Slack integration and begin the initial discovery for Jira and Confluence. The Slack integration is currently blocked by oauth approval...",
    }
  ]
};

const mixedResults: SearchResultItem[] = [
  mockResultsStore.incident[0],
  mockResultsStore.onboarding[0],
  mockResultsStore.sprint[0],
  {
    chunk_id: "chunk-mix-1",
    document_id: "doc-9",
    document_title: "API Rate Limiting Proposal",
    provider: "google_drive",
    source: "Engineering Hub",
    score: 0.65,
    section_heading: "Proposed Limits",
    page_number: 1,
    document_status: "READY",
    snippet: "...We propose a tiered rate limiting strategy: Free tier users are limited to 100 requests per minute, Pro tier to 1000 RPM, and Enterprise users get custom limits. We will implement this using a sliding window algorithm in Redis...",
  }
];

export function getMockSearchResults(query: string): SearchResultItem[] {
  const q = query.toLowerCase();
  
  if (q.includes("incident") || q.includes("outage") || q.includes("sev")) {
    return mockResultsStore.incident;
  }
  
  if (q.includes("onboard") || q.includes("setup")) {
    return mockResultsStore.onboarding;
  }
  
  if (q.includes("sprint") || q.includes("plan") || q.includes("q3")) {
    return mockResultsStore.sprint;
  }

  // Return empty array for complete gibberish to test empty state
  if (q.length > 10 && !q.includes(" ") && !q.includes("a") && !q.includes("e")) {
    return [];
  }
  
  return mixedResults;
}
