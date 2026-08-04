# Security Policy

## Supported Versions

Since this is a continuously deployed DevOps portfolio and Serverless API, we currently support the latest `main` branch deployment. 

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | :white_check_mark: |
| < v1.0  | :x:                |

## Reporting a Vulnerability

Security is a top priority for our DevSecOps infrastructure. If you discover a vulnerability in the Terraform code, Serverless Lambda API, or CI/CD pipelines, please follow these steps:

1. **Do not open a public issue.** This ensures that malicious actors cannot exploit the vulnerability before we can patch it.
2. Email your findings directly to `[EMAIL_ADDRESS]`
3. Please include the following in your report:
   - A detailed description of the vulnerability.
   - Steps to reproduce the issue.
   - Any relevant logs, screenshots, or code snippets.

### What to expect:
- You will receive an acknowledgment of your report within 48 hours.
- If the vulnerability is verified, we will work on a patch immediately and aim to deploy the fix via our automated CI/CD pipeline within 5 business days.
- We will notify you once the fix has been pushed to production.

Thank you for helping keep our infrastructure secure!
