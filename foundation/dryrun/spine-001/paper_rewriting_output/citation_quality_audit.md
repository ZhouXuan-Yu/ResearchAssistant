# Citation Quality Audit

- Output directory: `C:\Users\ZhouXuan\Desktop\OH-WorkSpace\foundation\dryrun\spine-001\paper_rewriting_output`
- Scene: journal
- Target citation count: 0
- Entries analyzed: 25
- Scope: candidate diagnostics, not final cited-reference coverage, source-content support or manuscript readiness; recency/type scores are heuristic.
- Verified: 18 | Mismatched: 1 | Dead: 0
- Overall quality score: 88/100
- Status: PASS

> Each entry below includes a teaching note explaining *why* the citation quality matters.

## Per-Citation Analysis

| ID | DOI | Type | Resolves | Title Match | Year Match | Score | Status |
|---|---|---|---|---|---|---|---|
| C01 | 10.1109/cvpr52729.2023.01386 | sota | yes | 100% | yes | 85 | verified |
| C01 | 10.1109/cvpr52729.2023.01386 | sota | yes | 100% | yes | 85 | verified |
| C02 | 10.1109/cvpr52688.2022.01150 | sota | yes | 100% | yes | 85 | verified |
| C03 | 10.1109/cvprw56347.2022.00074 | sota | yes | 100% | yes | 85 | verified |
| C04 | 10.1109/cvprw63382.2024.00606 | sota | yes | 100% | yes | 95 | verified |
| C05 | 10.1016/j.patcog.2024.110357 | sota | yes | 83% | yes | 95 | verified |
| C06 | 10.1016/j.imavis.2023.104715 | sota | yes | 83% | yes | 85 | verified |
| C07 | 10.1016/j.patrec.2025.07.016 | sota | yes | 79% | yes | 95 | verified |
| C08 | 10.1109/prai59366.2023.1033202 | sota | yes | 100% | yes | 85 | verified |
| C09 | 10.1145/3663976.3663985 | sota | yes | 100% | yes | 95 | verified |
| C10 | 10.1016/j.imavis.2026.105930 | sota | yes | 82% | yes | 100 | verified |
| C11 | 10.1007/s11760-026-05207-7 | sota | yes | 84% | yes | 100 | verified |
| C12 | 10.5220/0012298400003636 | sota | yes | 100% | yes | 95 | verified |
| C13 | 10.1109/iciip68302.2025.113462 | sota | yes | 100% | yes | 95 | verified |
| C14 | 10.1109/iciip68302.2025.113461 | sota | yes | 100% | yes | 95 | verified |
| C15 | 10.1117/12.3076237 | sota | yes | 100% | yes | 95 | verified |
| C16 | arXiv:2412.06674 | sota | no | 0% | no | 85 | pending |
| C17 | arXiv:2606.14735 | sota | no | 0% | no | 90 | pending |
| C18 | arXiv:2111.13156 | sota | no | 0% | no | 65 | pending |
| C19 | arXiv:2208.03550 | sota | no | 0% | no | 75 | pending |
| C20 | arXiv:2407.02934 | sota | no | 0% | no | 85 | pending |
| C21 | arXiv:2311.08094 | sota | no | 0% | no | 75 | pending |
| C22 | 10.2139/ssrn.6811533 | sota | yes | 100% | yes | 100 | verified |
| C23 | 10.2139/ssrn.5123368 | sota | yes | 100% | yes | 95 | verified |
| C24 | 10.37547/ibast/volume06issue08 | sota | yes | 67% | yes | 70 | mismatched |

### C16 — 

Status: **pending**

> The bank records a specific non-DOI verification source. This run has not rechecked that source and has not resolved a DOI. Reuse the actual recorded source check when applicable; a flag or identifier alone is not new verification.

### C17 — 

Status: **pending**

> The bank records a specific non-DOI verification source. This run has not rechecked that source and has not resolved a DOI. Reuse the actual recorded source check when applicable; a flag or identifier alone is not new verification.

### C18 — 

Status: **pending**

> The bank records a specific non-DOI verification source. This run has not rechecked that source and has not resolved a DOI. Reuse the actual recorded source check when applicable; a flag or identifier alone is not new verification.

### C19 — 

Status: **pending**

> The bank records a specific non-DOI verification source. This run has not rechecked that source and has not resolved a DOI. Reuse the actual recorded source check when applicable; a flag or identifier alone is not new verification.

### C20 — 

Status: **pending**

> The bank records a specific non-DOI verification source. This run has not rechecked that source and has not resolved a DOI. Reuse the actual recorded source check when applicable; a flag or identifier alone is not new verification.

### C21 — 

Status: **pending**

> The bank records a specific non-DOI verification source. This run has not rechecked that source and has not resolved a DOI. Reuse the actual recorded source check when applicable; a flag or identifier alone is not new verification.

### C24 — 10.37547/ibast/volume06issue08-02

Status: **mismatched**

- Title similarity 0.67 below 0.75 threshold. Crossref title: 'Lightweight Transformer-Fourier Fusion Framework for Efficient Image Super-Resolution'

> Partial title match (67%). The DOI resolves but the title doesn't match your citation text. Check whether the DOI is correct or the citation text needs updating.

## Citation Diversity Gaps

**Missing foundational method or theory papers.** Only 0 of 25 entries (0%). Cite the 2-3 methods your work builds on. Explain inheritance clearly. Consider adding 1-3 foundational method or theory paper references.

**Missing dataset, benchmark, or evaluation protocol papers.** Only 0 of 25 entries (0%). Cite the datasets you evaluate on. Report dataset statistics. Consider adding 1-3 dataset, benchmark, or evaluation protocol paper references.

**Missing survey, review, or meta-analysiss.** Only 0 of 25 entries (0%). Cite 1-2 recent surveys to position your work in the broader landscape. Consider adding 1-3 survey, review, or meta-analysis references.

**Missing domain-application or impact papers.** Only 0 of 25 entries (0%). Optional unless your contribution is application-motivated. Consider adding 1-3 domain-application or impact paper references.


## Scene-Specific Citation Strategy

For **journal** papers, your citation strategy should:

- **direct task or state-of-the-art paper**: Must cite the 3-5 most recent competing methods. Missing these is a desk-reject risk.
- **foundational method or theory paper**: Cite the 2-3 methods your work builds on. Explain inheritance clearly.
- **dataset, benchmark, or evaluation protocol paper**: Cite the datasets you evaluate on. Report dataset statistics.
- **survey, review, or meta-analysis**: Cite 1-2 recent surveys to position your work in the broader landscape.
- **domain-application or impact paper**: Optional unless your contribution is application-motivated.
- **limitation, robustness, reproducibility, or ethics paper**: Include 1-2 limitation/robustness papers to show awareness of field challenges.

## Citation Strategy Principles

- **Diversity over density.** A narrow citation pool makes your Introduction read as insular. Mix SOTA, foundational, benchmark, survey, and application papers.
- **Relevant coverage.** Use current competing evidence and the original methods needed by the argument; derive count and age expectations from the selected task and venue, not a universal three-year quota.
- **Verify identity and support.** Resolve a stable identifier and compare metadata and source content. An unavailable index is an unresolved lookup, not evidence of fabrication.
- **Type matters by venue.** Journals expect deep SOTA coverage. Reports expect broad survey coverage. Competitions expect benchmark and leaderboard coverage. Match your strategy to your scene.
