# Work Order Template

**Work Order ID:** WO-[NNN]
**Fiefdom:** [NAME]
**Building:** `[FILE_PATH]`
**Room:** [FUNCTION/CLASS_NAME]
**Line Range:** [START]-[END]

## Metrics
| Metric | Value |
|--------|-------|
| Tokens | [N] |
| Complexity | [N] |
| Responsibility Class | [CLASS] |
| Agents Required | [N] |
| Wave | [N] |

## Dependencies
- [NONE or list of WO-IDs from previous waves]

## Border Impact
- [NONE or border ID + description of impact]

## Action
### DO THIS:
1. [EXACT INSTRUCTION]
2. [EXACT INSTRUCTION]
3. [EXACT INSTRUCTION]

### DO NOT:
- [CONSTRAINT]
- [CONSTRAINT]

## Verification
### Automated:
- [TEST COMMAND OR CHECK]

### Existing Tests:
- `[TEST COMMAND]`

## Git Commit
```text
[Tier N][FIEFDOM][ROOM] description
type(scope): concise description
- key change 1
```
