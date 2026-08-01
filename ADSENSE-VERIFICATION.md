# AdSense and ads.txt verification

## Code verification completed
- Publisher loader: `ca-pub-8379415024436818`.
- `ads.txt`: `google.com, pub-8379415024436818, DIRECT, f08c47fec0942fa0`.
- The quality gate rejects duplicate AdSense loaders and a mismatched ads.txt publisher.
- Privacy disclosures mention advertising, cookies and third-party processing.

## Account-owner verification still required
Code consistency does not prove that the AdSense account is approved or that the publisher ID belongs to the current site owner. In the AdSense account:
1. Confirm the publisher ID is exactly `pub-8379415024436818`.
2. Confirm `fynzo.me` is added and has no ownership or policy warning.
3. Confirm AdSense can fetch `/ads.txt`.
4. Configure consent requirements for the visitor regions served.
5. Do not add manual ad units until the account and site are eligible.
