# FAQ click interaction fix

## Root cause
The FAQ control had a keyboard `keydown` listener for Enter and Space, but no mouse/touch `click` listener. As a result, the FAQ looked interactive but clicking did not open it.

## Fix
- Added a click listener to every `.faq-q` control.
- Preserved Enter and Space keyboard support.
- The `.open` class now expands the answer, updates `aria-expanded`, and rotates the plus icon.
- Increased the open answer height allowance for longer answers.
- Updated the service-worker cache version so browsers receive the corrected JavaScript.
- Added `faq_tests.py` to validate the handler and every FAQ item's accessibility wiring.
- Added the FAQ test to GitHub Actions.

## Validation
- 171 FAQ items validated.
- Click handler present.
- Keyboard handler present.
- `aria-controls`, answer IDs, `aria-expanded`, role and tabindex validated.
