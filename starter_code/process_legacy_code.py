import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    tree = ast.parse(source_code)

    module_docstring = ast.get_docstring(tree) or ""
    function_docstrings = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node)
            if doc:
                function_docstrings.append(
                    {
                        "function_name": node.name,
                        "docstring": doc.strip(),
                    }
                )

    rule_mentions = re.findall(r"Business Logic Rule\s*\d+", source_code, flags=re.IGNORECASE)

    content_parts = []
    if module_docstring:
        content_parts.append(f"Module notes: {module_docstring.strip()}")
    if function_docstrings:
        joined = "; ".join(
            [f"{item['function_name']}: {item['docstring']}" for item in function_docstrings]
        )
        content_parts.append(f"Function logic docs: {joined}")

    return {
        "document_id": "legacy-code-001",
        "content": " | ".join(content_parts),
        "source_type": "Code",
        "author": "legacy_pipeline",
        "timestamp": None,
        "source_metadata": {
            "rule_mentions": sorted(set(rule_mentions)),
            "function_count": len(function_docstrings),
            "functions_with_docstrings": [d["function_name"] for d in function_docstrings],
        },
    }

