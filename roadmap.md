# Benford Lens Roadmap

Benford Lens v1.0.1 is publicly available with the planned analysis, preprocessing,
drill-down, reporting, internationalization, and macOS/Windows packaging scope complete.

## Required follow-up milestone — trusted desktop distribution

The remaining product milestone is to reduce operating-system trust warnings for public
downloads. It is complete when:

- the macOS Apple Silicon package is signed with a Developer ID certificate, notarized,
  stapled, and verified on a clean supported Mac;
- Windows uses one approved signed distribution path—Microsoft Store signing or
  Authenticode signing for the executable and installer—and is verified on a clean
  supported Windows 11 machine; and
- the Release notes and checksum instructions accurately describe the selected signing
  and verification paths.

Signing credentials, paid enrollment, Store submission, and distribution builds remain
maintainer-approved actions.

## Ongoing maintenance

Dependency and security updates, regression tests, translation parity, and documentation
updates continue as maintenance work. They are not separate product milestones.
