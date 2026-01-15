## Peer Review Checklist (Pricing Model)

### Model integrity
- [ ] No hardcoded cells in calculation areas (inputs only)
- [ ] Formula consistency checks passed
- [ ] Named ranges (if used) updated and consistent

### Assumptions & alignment
- [ ] Assumptions consistent with reserving / finance sign-off
- [ ] Trend assumptions documented in `ASSUMPTIONS.md`
- [ ] Any methodology changes documented in `CHANGELOG.md`

### Outputs & reasonableness
- [ ] Validation workbook updated (`model/Validation_Checks.xlsx`)
- [ ] Rate impact is within expected range vs prior period
- [ ] Dislocation analysis reviewed for tail scenarios

### Documentation
- [ ] `README.md` updated if workflow/structure changed
- [ ] `DATA_DICTIONARY.md` updated if new fields added
