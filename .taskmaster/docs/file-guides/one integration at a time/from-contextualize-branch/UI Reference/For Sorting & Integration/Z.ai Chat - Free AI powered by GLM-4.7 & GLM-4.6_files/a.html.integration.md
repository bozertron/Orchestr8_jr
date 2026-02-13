# a.html Integration Guide

- Source: `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html`
- Total lines: `636`
- SHA256: `476e19f9fa2d402a3b3aa5b44c88652c8148bb52bb2cd54cd434d1148093f8ac`
- Memory chunks: `6`
- Observation IDs: `570..575`

## Why This Is Painful

- Large surface area: high chance of hidden coupling and missed assumptions.
- Visual canon risk: color/motion contract regressions are easy to introduce.

## Anchor Lines

- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html:281` <button id="btn-fix-bug">Restore (Gold)</button>
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html:341` uniform float uState; // 0=Gold, 1=Blue(Broken)
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html:358` // STATE LOGIC (Gold vs Blue):
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html:371` // Gold State
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html:372` targetColor = vec3(0.83, 0.68, 0.21); // Gold
- `one integration at a time/from-contextualize-branch/UI Reference/For Sorting & Integration/Z.ai Chat - Free AI powered by GLM-4.7 & GLM-4.6_files/a.html:413` uState: { value: 0.0 }     // 0 = Gold, 1 = Blue

## Integration Use

- Read this first to avoid re-deriving constraints.
- Implement against these anchors, then verify in runtime tests.
