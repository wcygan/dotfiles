# Motion And Interaction Feedback

## Description

Use this reference when adding transitions, animations, hover states, focus feedback, pressed states, view transitions, skeletons, loading indicators, or micro-interactions. Motion should clarify cause and state, not decorate every change.

Browse current official docs before making precise claims about transition syntax, animation behavior, view transitions, reduced motion, animatable properties, or performance.

## Docs To Browse

- MDN, CSS transitions: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_transitions
- MDN, CSS animations: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations
- MDN, `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- MDN, View Transition API: https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
- web.dev, Animation: https://web.dev/learn/css/animations

## Guidance

- Use motion to show continuity, causality, hierarchy, or feedback.
- Keep common UI transitions short and subtle.
- Prefer animating opacity and transform when possible.
- Avoid motion that changes layout unless the layout change itself is the point.
- Provide a reduced-motion path for nonessential animation.
- Keep focus and keyboard states at least as clear as hover states.

## Checks

- Does motion communicate a state change the user needs?
- Does the component remain understandable with reduced motion?
- Are hover-only cues duplicated for keyboard focus?
- Are long-running animations paused, limited, or purposeful?
