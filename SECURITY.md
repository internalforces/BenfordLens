# Security Policy

## Supported versions

Security fixes are provided for the latest published release and the current `main` branch.
Older releases may be assessed, but users should normally upgrade to the latest verified package.

## Report a vulnerability privately

Use GitHub's
[private vulnerability reporting form](https://github.com/internalforces/BenfordLens/security/advisories/new).
Please do not open a public issue for a suspected vulnerability.

Include only what is needed to reproduce the problem:

- affected version, operating system, and install method;
- impact and required preconditions;
- minimal steps or a proof of concept using synthetic data;
- suggested mitigation, if known.

Never submit a real user dataset, credential, personal information, or confidential file. The
application has no server component, so maintainers will not ask for remote access to user data.

Maintainers aim to acknowledge a report within 7 days, provide a status update within 14 days,
and coordinate disclosure after a fix or mitigation is available. Timelines may vary with
severity and maintainer availability.

## Relevant security boundary

Reports are particularly useful when they concern:

- unexpected data leaving the local machine;
- modification of an original CSV/XLSX input;
- unsafe parsing, code execution, or path handling;
- dependency, build, package, checksum, or release-integrity concerns.

Unsigned-platform warnings, requests for a new feature, and questions about whether Benford's Law
fits a dataset are not vulnerabilities. See [Support](SUPPORT.md) for those topics.
