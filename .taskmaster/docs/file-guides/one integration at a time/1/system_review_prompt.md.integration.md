# system_review_prompt.md Integration Guide

- Source: `one integration at a time/1/system_review_prompt.md`
- Total lines: `1787`
- SHA256: `9766eaf26e067836e686fad641612858e31baa282b175e2a06dfc885c92e6829`
- Memory chunks: `15`
- Observation IDs: `166..180`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/1/system_review_prompt.md:1` # JFDI System Review Prompt Template
- `one integration at a time/1/system_review_prompt.md:65` - Pattern Bible: `/home/bozertron/EPO - JFDI - Maestro/CLAUDE_jfdi_pattern_bible.md`
- `one integration at a time/1/system_review_prompt.md:141` You MUST pause and create a checkpoint report if ANY of these occur:
- `one integration at a time/1/system_review_prompt.md:255` - JavaScript state (should be Rust-only)
- `one integration at a time/1/system_review_prompt.md:266` 1. **Pattern Bible** (AUTHORITATIVE SOURCE):
- `one integration at a time/1/system_review_prompt.md:267` - `/home/bozertron/EPO - JFDI - Maestro/CLAUDE_jfdi_pattern_bible.md`
- `one integration at a time/1/system_review_prompt.md:276` - Any other docs in `/home/bozertron/EPO - JFDI - Maestro/docs/` related to this subsystem
- `one integration at a time/1/system_review_prompt.md:360` - List types that SHOULD be in Pattern Bible but aren't
- `one integration at a time/1/system_review_prompt.md:361` - Explain why they should be documented
- `one integration at a time/1/system_review_prompt.md:409` - List files that SHOULD exist but don't
- `one integration at a time/1/system_review_prompt.md:498` **Intended Integration (What SHOULD BE):**
- `one integration at a time/1/system_review_prompt.md:506` - Connections that should exist but don't
- `one integration at a time/1/system_review_prompt.md:507` - Events that should be emitted but aren't
- `one integration at a time/1/system_review_prompt.md:508` - Data that should flow but doesn't
- `one integration at a time/1/system_review_prompt.md:556` - [How it violates JFDI principles]
- `one integration at a time/1/system_review_prompt.md:705` **6.4 Adherence to JFDI Principles**
- `one integration at a time/1/system_review_prompt.md:788` **Dependencies**: [What must be fixed first]
- `one integration at a time/1/system_review_prompt.md:917` 4. ✅ **REALITY CHECK**—document what IS, not what should be (save recommendations for Section 7)
- `one integration at a time/1/system_review_prompt.md:919` 6. ✅ **PATTERN BIBLE IS LAW**—all recommendations must align with JFDI architectural principles
- `one integration at a time/1/system_review_prompt.md:1383` - Document what IS, not what should be
- `one integration at a time/1/system_review_prompt.md:1774` **Next Step**: [What should happen next]
- `one integration at a time/1/system_review_prompt.md:1787` **Template saved**: `/home/bozertron/EPO - JFDI - Maestro/system_review_prompt.md`

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
