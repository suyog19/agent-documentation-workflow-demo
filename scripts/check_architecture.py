from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOMAIN = ROOT / "src" / "domain"
FORBIDDEN_PREFIX = "src.infrastructure"


def imported_modules(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom) and node.module:
        return [node.module]
    return []


def main() -> int:
    violations: list[str] = []

    for path in sorted(DOMAIN.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            for module in imported_modules(node):
                if module == FORBIDDEN_PREFIX or module.startswith(FORBIDDEN_PREFIX + "."):
                    relative = path.relative_to(ROOT).as_posix()
                    violations.append(
                        f"{relative}:{getattr(node, 'lineno', '?')} imports {module}"
                    )

    if violations:
        print("Architecture check failed:")
        for violation in violations:
            print(f"  - {violation}")
        print("\nRule: src/domain must not import src/infrastructure.")
        return 1

    print("Architecture check passed: src/domain has no imports from src/infrastructure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
