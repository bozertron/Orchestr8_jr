# Task ID: 23

**Title:** Emergence Animation CSS Verification

**Status:** pending

**Dependencies:** 15

**Priority:** medium

**Description:** Verify emergence animations in orchestr8.css conform to canon rules: things EMERGE from the void, NO breathing/pulsing animations. Ensure keyframe definitions align with MaestroView emergence patterns.

**Details:**

1. Audit current emergence animations in orchestr8.css (lines 56-83):
```css
@keyframes emergence {
    0% { opacity: 0; transform: translateY(12px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes emergence-fade {
    0% { opacity: 0; }
    100% { opacity: 1; }
}

@keyframes emergence-scale {
    0% { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
}
```

2. Compare with MaestroView.vue transitions (lines 852-869):
```css
.emerge-enter-active {
    transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1);
}
.emerge-enter-from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
}
```

3. Verify NO breathing animations exist:
   - Search for 'pulse', 'breathe', 'infinite'
   - Remove any found

4. Update emergence timing to match MaestroView:
   - Duration: 400ms (vs current unspecified)
   - Easing: cubic-bezier(0.16, 1, 0.3, 1)
   - Transform: translateY(20px) scale(0.95)

5. Ensure animation-fill-mode: both for persistent state

6. Update orchestr8.css:
```css
@keyframes emergence {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.95);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.emerged-message {
    animation: emergence 400ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
```

**Test Strategy:**

1. Trigger panel/message emergence and observe animation
2. Verify no infinite/looping animations
3. Check animation timing feels consistent
4. Record and compare to MaestroView emergence
