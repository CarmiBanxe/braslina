# Braslina Demo Meeting Notes

- Date: 2026-04-15
- Source: internal demo / process walkthrough
- Topic: Merchant Onboarding procedure and automation opportunities

## Summary

The meeting described the current BANXE merchant onboarding flow using good and bad merchant examples.

The process starts from receiving a merchant website and onboarding questionnaire. Teams then review the merchant’s business type, licensing needs, MCC suitability, website quality, policies, payment logos, checkout behavior, and supporting documents.

The workflow currently involves Sales, IML/Compliance, and Cards/Card Operations teams.

## Key process steps captured from the meeting

1. Receive merchant website and onboarding questionnaire.
2. Review business type against acceptable categories.
3. Check whether the merchant activity requires licensing.
4. Validate desired MCC against the actual business model.
5. Review website quality and completeness.
6. Verify Terms and Conditions, Privacy Policy, Refund / Return / Cancellation Policy.
7. Verify customer service contacts and merchant identity information.
8. Verify card scheme logos and checkout/3DS behavior.
9. Perform a test purchase.
10. Verify receipt / confirmation delivery.
11. Request and verify refund.
12. Store screenshots with dates and keep evidence.
13. Complete final onboarding checklist and package.
14. Register merchant in onboarding register.
15. Re-check merchant periodically after onboarding.

## Pain points identified

- Missing screenshots and lack of preserved evidence
- Website can change after onboarding without prompt detection
- Process is fragmented across folders, spreadsheets, and manual reminders
- Checklist execution is manual and inconsistent
- Responsibility is split across teams, but evidence completeness is not enforced systematically
- Monitoring of turnover and periodic checks is not formalized enough
- CRM/workflow support is weak or absent

## Automation ideas explicitly discussed

- Agent that regularly captures screenshots of merchant websites
- Comparison of new screenshots with previous versions
- Alerts when merchant website changes significantly
- Better register / CRM workflow instead of Google Drive + tables
- Better evidence packaging for audits, brands, and compliance checks

## Operational constraints

- Final responsibility still stays with human teams
- Evidence must be preserved with dates
- Missing evidence should block onboarding
- Initial checks and recurring checks are both important
- Business model clarity is critical for AML / fraud / card scheme risk

## Expected modules derived from the meeting

- Website Monitor Agent
- Merchant Checklist Engine
- Onboarding Register
- CRM Integration
- Test Purchase Log
