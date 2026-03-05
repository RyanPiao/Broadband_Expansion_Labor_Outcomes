# Day 1 (Monday) — Problem Framing

## Project
**Title:** Semiconductor Production Cycles and U.S. Tech Employment Adjustment

## Research question
How do swings in U.S. semiconductor/electronics industrial production relate to short-run changes in U.S. software publishing employment?

## Why this matters
Chip cycles are often treated as "hardware-only" shocks, but modern software delivery (AI tooling, cloud infra dependencies, embedded stacks) can transmit hardware bottlenecks into software labor demand.

## Baseline hypothesis
- H1: Positive semiconductor production growth is associated with higher software employment growth over the following 1–6 months.
- H2: Negative semiconductor shocks coincide with slower software hiring momentum.

## Unit and period
- Unit: monthly U.S. macro time series
- Period target: 2000-present (subject to overlap across series)

## Candidate variables
- Semiconductor/electronic component production index (FRED: `IPG3344S`)
- Software publishing employment (FRED: `USINFO`)
- Total nonfarm payroll (control, FRED: `PAYEMS`)

## Day 1 output
- Question and estimand locked
- Data map and practical extraction plan ready for Day 2
