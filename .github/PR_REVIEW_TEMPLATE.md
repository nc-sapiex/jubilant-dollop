# Pull Request Review Checklist

Use this checklist to perform a structured review of the proposed changes.

## Review Checklist

### 1. Correctness & Logic
- [ ] Code matches requirements and intended behavior without side effects
- [ ] Edge cases, boundary conditions, and null/undefined cases handled properly
- [ ] Error handling is complete and informative

### 2. Security
- [ ] No secrets, private keys, or API tokens committed
- [ ] Inputs validated and sanitized against injection risks
- [ ] Authentication and authorization checks enforced appropriately

### 3. Performance & Resources
- [ ] No inefficient loops, N+1 queries, or memory leaks
- [ ] Resource cleanup implemented where applicable

### 4. Readability & Maintainability
- [ ] Code is clear, self-documenting, and free of dead code
- [ ] Functions and variables have descriptive, standard names

### 5. Tests & Coverage
- [ ] Unit/integration tests cover new or modified functionality
- [ ] Tests verify both happy path and failure conditions

## Review Outcome Templates

Copy and paste the relevant section into your review summary:

---

### Approve

```markdown
### 🟢 Review Outcome: APPROVED

**Summary:**
Reviewed the changes and verified correctness, security, tests, and readability.

- [x] All review checklist items satisfied
- [x] Code is ready for merge
```

---

### Request Changes

```markdown
### 🔴 Review Outcome: CHANGES REQUESTED

**Summary:**
The pull request requires the following modifications before merge:

1. [Issue/Question 1]
2. [Issue/Question 2]

**Required Actions:**
- [ ] Address feedback points listed above
- [ ] Re-run validation and notify reviewer
```

---

### Comment Only

```markdown
### 🟡 Review Outcome: COMMENT / FEEDBACK

**Summary:**
Non-blocking suggestions and questions provided below.

- [ ] [Optional question or refactoring suggestion]
```
