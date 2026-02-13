# LLM_BEHAVIOR_SPEC.md Integration Guide

- Source: `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md`
- Total lines: `437`
- SHA256: `416fa9e9caf1d96e6a8e64b01feec8dca671fde2d140fe2d68fc228fb24e0f4c`
- Memory chunks: `4`
- Observation IDs: `447..450`

## Why This Is Painful

- Medium-large surface area: requires strict scope control during integration.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:23` ### Primary Chat: maestro
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:25` **CRITICAL:** The primary chat LLM is ALWAYS named `maestro` (lowercase 'm').
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:123` Settings panel should present:
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:169` | **1** | Catastrophic Block | BLOCKED | Actions that could nuke codebase |
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:181` **CRITICAL:** LLMs must NOT self-engage Agent mode.
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:187` 3. LLM must explain why they ignored the rules
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:214` The standing orders document that ALL LLM Generals must follow.
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:219` - Naming conventions (maestro = lowercase)
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:260` > "ALL the data we can acquire on that explicit circuit in every way should be available to the engineers."
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:294` 2. NO stubs, EVER - must be life-or-death to justify
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:300` - Primary chat LLM is always "maestro" (lowercase 'm')
- `one integration at a time/docs/LLM_BEHAVIOR_SPEC.md:314` # Primary chat - maestro (your choice of model)

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
