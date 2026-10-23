# Next.js formal verification baseline

Source repository: https://github.com/PiquoInterest/next.js

Pinned source commit: `ba182aa1a68185844738ed60529cdf6ff6aac683`
Pinned source tree: `08acd018d5d472bda2f02a0a4e17de4e6ff30b5b`
Linear project: https://linear.app/highlvl/project/nextjs-formal-verification-c1ef0bdb21b9

## Run inventory

From repository root:

```bash
python3 formal-verification/tools/inventory_entrypoints.py
```

This writes `formal-verification/inventory/candidates.json`. Run against the pinned commit, not the research branch, when building the baseline inventory, or record the research branch SHA separately.

**Important:** The tool only identifies candidate functions by source patterns. It does not establish entrypoint reachability, completeness, proof coverage, or vulnerability.

## Verification completion contract

1. Enumerate all concrete externally reachable entrypoints and attach exact symbols and source links.
2. Generate proof obligations with explicit assumptions and expected behavior.
3. Prove against a sound model linked to the implementation; distinguish abstract model proofs from implementation-linked proofs.
4. Save machine checker output, exact toolchain versions and source hashes.
5. Treat unproved, timed-out and unsupported cases as incomplete.

## Privacy

The destination repository currently reports **public** visibility. Do not commit confidential findings, private evidence or credentials. Changing privacy requires an explicit repository settings action and verification.
