# DocuSense Internal Engineering & Operations Policies
*Version 4.2 | Last Updated: August 2026*

---

## 1. Introduction and Scope
This document outlines the standard operating procedures, security guidelines, and compliance requirements for the engineering, DevOps, and internal IT teams at DocuSense. All employees, contractors, and vendors with access to internal systems must adhere to these guidelines to maintain system integrity and data security. 

Failure to comply with these policies may result in revoked access privileges or disciplinary action. If you require an exception to any policy, you must submit a formal request via the internal IT ticketing system, which requires approval from the Director of Engineering.

## 2. Remote Work and Device Security
With the transition to a hybrid work model, device security is paramount. 
- **Company-Issued Devices:** Work must only be conducted on laptops and mobile devices issued by the DocuSense IT department. Bring Your Own Device (BYOD) is strictly prohibited for accessing source code or production databases.
- **Physical Security:** When working in public spaces (e.g., cafes, airports), employees must use a physical privacy screen and ensure their devices are locked when left unattended for any duration.
- **VPN Requirement:** All access to internal staging and production environments must be routed through the DocuSense corporate VPN. Split-tunneling is disabled by default on all company hardware.

## 3. Identity and Access Management (IAM)
We operate on a principle of least privilege (PoLP).
- **Multi-Factor Authentication (MFA):** All engineers must use FIDO2 hardware security keys (e.g., YubiKey) for multi-factor authentication. SMS-based or Authenticator App MFA is no longer permitted for engineering access.
- **Password Rotation:** Service account passwords must be rotated every 90 days. User passwords must be at least 16 characters long and are exempt from mandatory rotation unless a breach is suspected, per NIST guidelines.
- **Offboarding:** Upon employee termination or resignation, all system access must be revoked within 60 minutes by the automated HR-to-IT provisioning sync.

## 4. Data Retention and Backups
Data integrity and availability are critical to our business continuity and disaster recovery strategies.
- **Primary Database Backups:** To ensure we can recover from catastrophic failures, all primary database backups are retained for a rolling period of 30 calendar days. 
- **Cold Storage Transition:** After 30 days, primary backups are transitioned to AWS Glacier cold storage.
- **Compliance Archiving:** Once in cold storage, financial and user-telemetry backups are kept for up to 7 years to satisfy SOC2 and GDPR compliance purposes.
- **Restoration Testing:** The DevOps team must perform a simulated disaster recovery database restoration on the 15th of every month to verify backup integrity.

## 5. Deployment Cycles and CI/CD
Our deployment philosophy prioritizes stability and minimal disruption to end-users.
- **Approved Deployment Windows:** Production deployments are restricted to Tuesdays and Thursdays between 10:00 AM and 2:00 PM EST. 
- **Friday Deployments:** No deployments are permitted on Fridays. This is a hard rule. The only exception is a P0 critical security hotfix, which must be explicitly approved by the VP of Engineering.
- **Staging Requirements:** All code must bake in the staging environment for a minimum of 24 hours before being promoted to production.

## 6. Incident Response and On-Call Escalation
When production systems experience degradation, the following protocol applies:
- **P0 Incidents:** Complete system outage or critical data breach. The on-call engineer must acknowledge the page within 5 minutes. If unacknowledged, the page escalates directly to the Engineering Manager.
- **P1 Incidents:** Partial degradation of core services. The on-call engineer has 15 minutes to acknowledge.
- **Post-Mortem Requirement:** Any P0 or P1 incident requires a blameless root-cause analysis (RCA) document to be completed and shared with the engineering org within 72 hours of incident resolution.