# Medical Pricing Model (Excel) — GitHub Repo Template

## Purpose
Excel-based pricing model used for annual rate review and benefit repricing.

## Model Owner
Pricing Team – Medical Insurance

## Workflow (Governance)
1. **No direct commits to `main`**
2. Create a branch (e.g., `rate-review-2026`)
3. Make changes + update documentation
4. Open a Pull Request (PR)
5. Peer review + approval
6. Merge to `main` and tag a release

## Typical Outputs
- Rate impact by product / segment
- Loss ratio movement
- Dislocation analysis
- Validation checks

## Repository Structure
- `model/` : Excel models (pricing + validation)
- `inputs/` : model inputs (CSV / assumptions)
- `outputs/` : exported outputs (CSV)
- `governance/` : review checklists + sign-off templates
- `.github/` : PR templates
