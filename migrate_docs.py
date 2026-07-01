import os
import re

BRAIN_DIR = r"C:\Users\Yug Pathak\.gemini\antigravity\brain\909fb9ab-afce-4bc8-9876-09c0bfa83e89"
ARCH_DIR = r"c:\Users\Yug Pathak\Desktop\calyxbot.ai\architecture"

def create_dirs():
    dirs = [
        "vision",
        "product",
        "system",
        "adr",
        "diagrams",
        "decisions"
    ]
    for d in dirs:
        os.makedirs(os.path.join(ARCH_DIR, d), exist_ok=True)

def write_doc(path, title, content, version="1.0", status="Approved", owner="Architecture Team", related=[]):
    filepath = os.path.join(ARCH_DIR, path)
    header = f"""# {title}

**Version:** {version}
**Status:** {status}
**Last Updated:** 2026-06-30
**Owner:** {owner}
**Related Documents:**
"""
    if related:
        for r in related:
            header += f"- {r}\n"
    else:
        header += "- None\n"
    header += "\n---\n\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + content.strip() + "\n")

def read_file(name):
    path = os.path.join(BRAIN_DIR, name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def migrate_adrs():
    adr_content = read_file("adr.md")
    if not adr_content: return
    adrs = re.split(r'\n## (ADR-\d{3}: .+?)\n', adr_content)
    for i in range(1, len(adrs), 2):
        title = adrs[i].strip()
        content = adrs[i+1].strip()
        if "End of Architecture Decision Records" in content:
            content = content.replace("*End of Architecture Decision Records.*", "").strip()
        match = re.match(r'(ADR-\d{3}):', title)
        if match:
            write_doc(f"adr/{match.group(1)}.md", title, content, related=["[Architecture Overview](../system/architecture-overview.md)"])

def extract_section(text, header_regex):
    match = re.search(header_regex, text)
    if not match: return ""
    start = match.end()
    # Find next level 1 header or end of file
    next_header = re.search(r'\n# \d+\.', text[start:])
    if next_header:
        end = start + next_header.start()
        return text[start:end].strip()
    return text[start:].strip()

def extract_diagrams(text):
    return re.findall(r'(```mermaid\n.*?\n```)', text, re.DOTALL)

def process_design_review():
    dr = read_file("design_review.md")
    if not dr: return

    # Product Scope -> vision/product-vision.md & product/prd.md
    scope = extract_section(dr, r'# 1\. Product Scope')
    write_doc("vision/product-vision.md", "Product Vision", scope, related=["[PRD](../product/prd.md)"])
    write_doc("product/prd.md", "Product Requirements Document (PRD)", scope, related=["[Product Vision](../vision/product-vision.md)"])

    # User Personas -> product/personas.md
    personas = extract_section(dr, r'# 2\. User Personas')
    write_doc("product/personas.md", "User Personas", personas, related=["[RBAC](../system/rbac.md)"])

    # Multi-Tenant Architecture -> system/multi-tenancy.md
    mt = extract_section(dr, r'# 3\. Multi-Tenant Architecture')
    write_doc("system/multi-tenancy.md", "Multi-Tenant Architecture", mt, related=["[Database Design](../system/database-design.md)"])

    # Authentication Flow -> system/security-model.md
    auth = extract_section(dr, r'# 4\. Authentication Flow')
    write_doc("system/security-model.md", "Security & Authentication Model", auth, related=["[RBAC](../system/rbac.md)"])
    
    auth_diagrams = extract_diagrams(auth)
    write_doc("diagrams/auth-sequence.md", "Authentication Sequence Diagrams", "\n\n".join(auth_diagrams), related=["[Security Model](../system/security-model.md)"])

    # Authorization Model -> system/rbac.md
    rbac = extract_section(dr, r'# 5\. Authorization Model')
    write_doc("system/rbac.md", "Role-Based Access Control (RBAC)", rbac, related=["[Security Model](../system/security-model.md)", "[User Personas](../product/personas.md)"])

    # Data Ownership -> (Merge with Database Design)
    data = extract_section(dr, r'# 6\. Data Ownership')
    db = extract_section(dr, r'# 7\. Database Design')
    write_doc("system/database-design.md", "Database Design & Data Ownership", data + "\n\n" + db, related=["[Multi-Tenancy](../system/multi-tenancy.md)"])
    
    er_diagrams = extract_diagrams(db)
    write_doc("diagrams/er-diagram.md", "Entity-Relationship Diagram", "\n\n".join(er_diagrams), related=["[Database Design](../system/database-design.md)"])

def process_memory_engine():
    me = read_file("memory_engine_design.md")
    if not me: return

    write_doc("system/memory-engine.md", "Memory Engine Specification", me, related=["[Knowledge Extraction](../system/knowledge-extraction.md)", "[Architecture Overview](../system/architecture-overview.md)"])
    
    me_diagrams = extract_diagrams(me)
    write_doc("diagrams/memory-graph.md", "Memory Graph Diagrams", "\n\n".join(me_diagrams), related=["[Memory Engine](../system/memory-engine.md)"])
    
    knowledge_src = extract_section(me, r'# 3\. Knowledge Sources')
    write_doc("system/knowledge-extraction.md", "Knowledge Extraction Pipeline", knowledge_src, related=["[Memory Engine](../system/memory-engine.md)"])

def process_sprint_backlog():
    sb = read_file("sprint_1_backlog.md")
    if not sb: return
    write_doc("product/sprint-backlog.md", "Sprint 1 Backlog", sb, related=["[PRD](../product/prd.md)"])

def create_stubs():
    write_doc("system/architecture-overview.md", "Architecture Overview", "This document provides a high-level overview of the Calyx architecture, integrating the various system components.", related=["[Memory Engine](../system/memory-engine.md)", "[Multi-Tenancy](../system/multi-tenancy.md)"])
    write_doc("system/api-standards.md", "API Standards", "This document outlines the REST API design standards, error handling, pagination, and response formats.", related=["[Architecture Overview](../system/architecture-overview.md)"])
    
    write_doc("diagrams/onboarding-flow.md", "Onboarding Flow Diagram", "*(Diagram pending)*", related=["[Security Model](../system/security-model.md)"])
    write_doc("diagrams/system-overview.md", "System Overview Diagram", "*(Diagram pending)*", related=["[Architecture Overview](../system/architecture-overview.md)"])
    
    write_doc("decisions/open-questions.md", "Open Questions", "Track unresolved architectural questions here.", related=["[Architecture Overview](../system/architecture-overview.md)"])
    write_doc("decisions/technical-debt.md", "Technical Debt", "Track known architectural shortcuts and post-MVP refactoring needs here.", related=["[Architecture Overview](../system/architecture-overview.md)"])
    write_doc("decisions/future-ideas.md", "Future Ideas", "Track post-MVP architectural ideas (e.g., custom roles, graph database migration).", related=["[Architecture Overview](../system/architecture-overview.md)"])
    write_doc("vision/problem-statement.md", "Problem Statement", "Calyx helps companies preserve organizational knowledge so that when employees leave, their knowledge is never lost.", related=["[Product Vision](../vision/product-vision.md)"])
    write_doc("vision/roadmap.md", "Roadmap", "High-level milestones and future roadmap.", related=["[Product Vision](../vision/product-vision.md)"])
    write_doc("product/user-flows.md", "User Flows", "Detailed user flows across the application.", related=["[PRD](../product/prd.md)", "[User Personas](../product/personas.md)"])

    readme_content = """# Calyx Architecture Documentation

Welcome to the Calyx Engineering Knowledge Base. This directory contains the definitive, version-controlled architecture documentation for the project.

## Organization

- **vision/** - High-level goals, problem statement, and roadmap.
- **product/** - Requirements, personas, and sprint backlogs.
- **system/** - Core system architecture, database design, memory engine, and security.
- **adr/** - Architecture Decision Records (ADR).
- **diagrams/** - Mermaid diagrams extracted for easy viewing.
- **decisions/** - Future ideas, open questions, and technical debt tracking.

## Governance

1. **Version Control:** Treat these documents as code.
2. **Updates:** When the architecture changes, update the relevant documents here.
3. **ADRs:** Any major technical decision must result in a new ADR in the `adr/` folder.
"""
    write_doc("README.md", "Calyx Architecture Documentation", readme_content, related=["[Architecture Overview](system/architecture-overview.md)"])

def main():
    create_dirs()
    migrate_adrs()
    process_design_review()
    process_memory_engine()
    process_sprint_backlog()
    create_stubs()
    print("Documentation migration completed successfully.")

if __name__ == "__main__":
    main()
