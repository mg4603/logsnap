# ADR 0005: Dedicated module per command group

**Status: Accepted**  
**Date: 07-04-2026**

## Context
Putting all command groups in `main.py` would make it very large,
cluttered and not easy to navigate and maintain as their numbers 
increase. 

## Decision
Create dedicated module per command group that groups all logic
related to it, and maintain `main.py` as a thin wiring layer.

## Alternatives Considered
- All command groups live in main: rejected because this would 
  make `main.py` a God module that is hard to maintain and reason
  about

## Consequences
### Positive
- Easy to reason about command logic
- Easy to maintain

### Negative
- Upfront organization overhead 

