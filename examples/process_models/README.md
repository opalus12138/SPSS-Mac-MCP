# PROCESS Models End-to-End Validation

This directory contains end-to-end tests for **6 common Andrew Hayes PROCESS models**
running through SPSS-Mac-MCP on macOS with SPSS 27 + PROCESS v4.1.

## Test Matrix

| Model | Type | Structure | Status |
|---|---|---|---|
| 1  | Moderation | X × W → Y | ✅ |
| 4  | Simple Mediation | X → M → Y | ✅ |
| 6  | Serial Mediation | X → M1 → M2 → Y | ✅ |
| 7  | First-Stage Moderated Mediation | (X × W) → M → Y | ✅ |
| 14 | Second-Stage Moderated Mediation | X → (M × W) → Y | ✅ |
| 58 | Both-Stage Moderated Mediation | (X × W) → (M × W) → Y | ✅ |

**Result: 6/6 PASS**, with 99.7% raw-output compression
(937KB raw → 1.4–3.7KB clean per model).

## Output Files

Each `outputs/M*.txt` is the post-processed PROCESS result block,
ready to paste into a paper or feed to an LLM.

## Running

```bash
# From this directory, with spss-mac-mcp installed:
python test_6_models.py
```

Requirements:
- IBM SPSS Statistics 20-31 (validated on 27)
- PROCESS macro v4.1 (auto-detected from ~/Downloads or set PROCESS_MACRO_PATH)
- Data file: `../full_validation/datasets/firm_panel.sav`
