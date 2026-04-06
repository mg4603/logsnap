# ADR 0004: Separate unit and integration test directories

**Status: Accepted**
**Date: 07-04-2026**

## Context
Tests need to be organized appropriately to ensure ease of 
navigation, low maintenance overhead, clear intent, fast CI, 
and focused tests.

## Decision
To use a split structure with unit and integration subdirectories.
Unit tests are placed in `tests/unit/` while integration tests are
placed in `tests/integration/`.

## Alternatives Considered
- flat structure: rejected because as test count grows, it becomes
  harder to navigate, slows focused test execution and CI, blurs
  test intent and increases maintenance overhead

## Consequences
### Positive
- Clear logical separation of tests by type

### Negatives
- Upfront organizational overhead
- Encourage rigid boundaries leading to duplicated config and
  adjustments to tooling
