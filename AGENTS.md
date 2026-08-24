# Coding Agent Instructions

For changes under `src/`:

1. Read `docs/architecture.md` before implementation.
2. Identify the architecture constraints relevant to the change.
3. Inspect the existing code and tests before choosing an implementation.
4. Run the feature tests:

   ```bash
   python -m unittest discover -s tests -v
   ```

5. Run the architecture validation:

   ```bash
   python scripts/check_architecture.py
   ```

6. In the completion response, report the documentation consulted, the validation commands executed, and whether they passed.

`docs/architecture.md` remains authoritative. Do not duplicate its technical rules here.
