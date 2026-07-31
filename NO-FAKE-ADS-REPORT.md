# Pre-AdSense placeholder cleanup

- Removed all empty or simulated advertising boxes from every HTML page.
- Removed visible labels such as `Ad`, `Ad space`, and `AdSense unit` where they represented empty placeholders.
- Removed the unused `.ad` placeholder CSS rule.
- Confirmed that no AdSense ad-serving script is installed before approval.
- Confirmed that no fake publisher ID remains.
- Updated the About page so it does not imply that advertising is currently active.
- Bumped the service-worker cache to `fynzo-v4` so browsers refresh the cleaned pages.

After AdSense approval, add real ad units only with the exact publisher ID supplied by Google and use clear labels such as `Advertisement` or `Sponsored Links` where a label is needed.
