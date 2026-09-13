# Pull Request Approval and Merge Quality Gate

Complete this gate before merging a pull request into main.

## 1. Continuous Integration (CI)
- [ ] All CI checks and automated test suites have passed
- [ ] No build or lint warnings introduced by this change

## 2. Review & Conversation Status
- [ ] All review comments and thread discussions are resolved
- [ ] Requested code modifications have been addressed and re-verified

## 3. Documentation
- [ ] Public/internal documentation updated to reflect changes (if applicable)
- [ ] Architecture / ADR / PRD updated if design or schema changed

## 4. Author Self-Review & Peer Approval
- [ ] **Author Attestation:** Author has completed self-review and verified local testing (solo-developer compatible)
- [ ] **Peer Reviewer Approval:** Required approval received (or self-approved for solo author workflows where policy permits)

## 5. Merge Method Selection
Select the appropriate merge method per project policy:
- [ ] **Squash and Merge:** Recommended for feature branches to keep `main` history clean
- [ ] **Rebase and Merge:** Used when commit history is clean and explicitly structured
- [ ] **Merge Commit:** Used for release branch integration or preserving explicit branch graph

## 6. Post-Merge Checks & Verification
- [ ] Verify deployment status in target environment (if auto-deployed)
- [ ] Clean up local and remote feature branches post-merge
- [ ] Update related issue / project board status to Closed/Done
