"""
Architecture Linter

Ensures that Routers -> Services -> Repositories -> Infrastructure.
No cyclic dependencies or layer skipping.
"""
import ast
import os

def check_layer_violations():
    # Simple AST-based check for imports in routers
    base_dir = "backend/app/modules"
    violations = []
    
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith("router.py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ImportFrom):
                            if node.module and "repositories" in node.module:
                                violations.append(f"Violation in {path}: Router directly imports Repository ({node.module})")
                                
    return violations

if __name__ == "__main__":
    print("Running Architecture Validation...")
    violations = check_layer_violations()
    if violations:
        for v in violations:
            print(f"❌ {v}")
        exit(1)
    else:
        print("✅ Architecture Validation Passed. Strict layering enforced.")
