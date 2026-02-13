# Context Window Erosion.txt Integration Guide

- Source: `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt`
- Total lines: `2556`
- SHA256: `a1f504ca80aa86c5dc88fbc455c9367f66960f0809ff0d7f0de364e1d519e439`
- Memory chunks: `22`
- Observation IDs: `342..363`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Constraint-heavy document: treat as canonical rules, not optional guidance.

## Anchor Lines

- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:235` Orchestrator Autonomy: How much decision-making authority should the Orchestrator have?
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:245` Failure Handling: If a Fixer breaks something (Validator fails), should Orchestrator:
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:313` Calculate Dependency Graph - which fixes must happen before others
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:436` Doesn't trace to termination	"I think this works"	Scout must VERIFY
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:453` Orchestrator MUST escalate to main context when:
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:482` For the Scout's "source of truth" JSON, should it include:
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:490` When multiple issues require escalation, should I:
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:608` "constraints": {
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:627` "must_escalate": ["strategy_selection", "architectural_changes"]
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:631` "must_include": ["file_paths", "integration_points", "code_snippets", "suggested_fixes"],
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:641` "scout_output_schema": {
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:716` 2. Evaluate each strategy against zero-tech-debt constraint
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:814` 5. Agent must release lock when complete
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1029` Apply the APPROVED fix strategy to your assigned file(s). Your work must be:
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1514` "reason": "Core module must load before anything else",
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1649` Which fix strategy should we execute?
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1782` Found issue in engine/design/__init__.py:16 - LoadCalculation should be Load.
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1890` Step 2. [This is a you problem ;-P , because it's pure strategy. ] Design a breathtaking load calculation module. Critical Development Note: Use 'all the tools in the toolbox' = We've got a bunch of very advanced calculators in this application; can you use them? Some of them? All of them? How will this particular load, affect other loads? = that should be accounted for. Go deep here, it'll pay off in spades when we're integrating other load calculators... in fact... my suggestion is that you parse all the tools to determine ALL the loads we need to calculate and figure out a crisp piece of code that can be manipulated to provide very sophisticated physics modelling that yields unprecedented big picture outputs and triggers warnings in other modules that get surfaced to the main UI page. I'm very much looking forward to reviewing your plan on this one.
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1896` Please carefully consider context window in this calculation as it will be computationally intense for some agents. I would rather deploy more agents per task than less. Also, please consider how this one wrapped up, and how we can use this - if viewed as a development strategy - to drive our ongoing efforts. For example, you now know that if you hit a stub, or an import that could simply 'be removed', your human team will not be a fan of that decision. Based on our leanings, should we create another Agent = 'The EPO Human Advocacy Agent'. My initial suggestion is that this agent considers the 'EPO human element' and performs an analysis on any/all failures, and considers what 'the user of the [tool name]' would want to perform their job to yield a delightful outcome, while experiencing a delightful UI and system experience. [something along those lines]
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1898` #Other notes: Ralf Wiggum was NOT deployed as far as I could see, this cycle should be included everywhere appropriate [even though in this case it likely wouldn't have been used].
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1922` My Role (Main Context) should be LIMITED to:
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:1930` Everything else should be delegated to agents.
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:2337` │     • IMPLEMENT: Feature should be built, not removed           │
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:2385` 1. **Stage Files** - Determine which files should be in commit
- `one integration at a time/Agent Deployment Strategy/Context Window Erosion.txt:2450` - If code is referenced, it should exist

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
