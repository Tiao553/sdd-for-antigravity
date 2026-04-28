# RUNBOOK: {FEATURE_NAME}

> Production operations guide generated after the validation gate approves release readiness.

## Document Control

| Attribute | Value |
|-----------|-------|
| Feature | {FEATURE_NAME} |
| Generated At | {YYYY-MM-DD} |
| Status | {STATUS} |
| Release Owner | {RELEASE_OWNER} |
| Operations Owner | {OPERATIONS_OWNER} |
| Related Validation | `VALIDATION_REPORT_{FEATURE_NAME}.md` |

---

## Release Summary

{RELEASE_SUMMARY}

### Release Decision

| Check | Required State | Current State |
|-------|----------------|---------------|
| Validation score | At least 90/100 | {VALIDATION_SCORE}/100 |
| Critical findings | 0 | {CRITICAL_ISSUE_COUNT} |
| Rollback plan | Documented and executable | Documented |
| Monitoring | Metrics, logs, and alerts identified | Documented |

---

## Pre-flight Checklist

Complete every item before production deployment.

- [ ] Latest `VALIDATION_REPORT_{FEATURE_NAME}.md` has verdict `Approved for Prod`.
- [ ] CI/CD pipeline completed successfully for the release commit.
- [ ] Required secrets and environment variables are configured in the target environment.
- [ ] Database or stateful backups are verified where applicable.
- [ ] Smoke tests passed in staging or equivalent pre-production environment.
- [ ] Monitoring dashboards and alerts are available to the on-call owner.
- [ ] Rollback owner and communication channel are confirmed.

---

## Deployment Plan

| Step | Action | Command / Evidence | Owner | Expected Result |
|------|--------|--------------------|-------|-----------------|
| 1 | Confirm release artifact and commit SHA | `{RELEASE_VERIFICATION_COMMAND}` | {RELEASE_OWNER} | Release candidate is immutable |
| 2 | Deploy to production | `{DEPLOY_COMMAND}` | {RELEASE_OWNER} | Deployment completes without errors |
| 3 | Run smoke checks | `{SMOKE_TEST_COMMAND}` | {OPERATIONS_OWNER} | Core workflow succeeds |
| 4 | Confirm data or service health | `{HEALTH_CHECK_COMMAND}` | {OPERATIONS_OWNER} | Health indicators are within thresholds |
| 5 | Announce deployment status | `{COMMUNICATION_CHANNEL}` | {RELEASE_OWNER} | Stakeholders receive outcome |

---

## Configuration and Dependencies

| Item | Value / Location | Validation Method |
|------|------------------|-------------------|
| Runtime environment | {RUNTIME_ENVIRONMENT} | `{ENV_CHECK_COMMAND}` |
| Required secrets | {SECRET_REFERENCES} | Secret presence check, no secret values in logs |
| External services | {EXTERNAL_DEPENDENCIES} | Connectivity or contract test |
| Data dependencies | {DATA_DEPENDENCIES} | Freshness and schema checks |
| Feature flags | {FEATURE_FLAGS} | Flag state verified before rollout |

---

## Observability

| Signal | Source | Healthy Threshold | Alert / Owner |
|--------|--------|-------------------|---------------|
| Availability | {AVAILABILITY_SOURCE} | {AVAILABILITY_THRESHOLD} | {ALERT_OWNER} |
| Error rate | {ERROR_RATE_SOURCE} | {ERROR_RATE_THRESHOLD} | {ALERT_OWNER} |
| Latency / duration | {LATENCY_SOURCE} | {LATENCY_THRESHOLD} | {ALERT_OWNER} |
| Data freshness / volume | {DATA_QUALITY_SOURCE} | {DATA_QUALITY_THRESHOLD} | {ALERT_OWNER} |
| Validation regressions | `/validate {FEATURE_NAME}` | Score remains at least 90 | {GATE_OWNER} |

### Operational Notes

{OPERATIONAL_NOTES}

---

## Incident Response

| Symptom | First Check | Escalation | Mitigation |
|---------|-------------|------------|------------|
| Deployment failed | CI/CD logs and deployment output | {RELEASE_OWNER} | Stop rollout and keep previous version active |
| Smoke test failed | Smoke test logs and recent changes | {OPERATIONS_OWNER} | Start rollback decision process |
| Data quality regression | Validation report and quality checks | {GATE_OWNER} | Disable downstream promotion until fixed |
| Elevated errors | Application/runtime logs | {ALERT_OWNER} | Roll back or disable feature flag |

---

## Rollback Plan

**Rollback trigger:** {ROLLBACK_TRIGGER}

| Step | Action | Command / Evidence | Owner | Expected Result |
|------|--------|--------------------|-------|-----------------|
| 1 | Freeze further rollout | `{FREEZE_COMMAND}` | {RELEASE_OWNER} | No new production changes continue |
| 2 | Restore previous known-good version | `{ROLLBACK_COMMAND}` | {RELEASE_OWNER} | Previous version is active |
| 3 | Validate service or pipeline health | `{POST_ROLLBACK_CHECK}` | {OPERATIONS_OWNER} | Health indicators recover |
| 4 | Record incident notes | `{INCIDENT_DOC_LINK}` | {OPERATIONS_OWNER} | Timeline and actions are captured |

---

## Post-deployment Validation

| Validation | Command / Evidence | Pass Criteria |
|------------|--------------------|---------------|
| Smoke test | `{SMOKE_TEST_COMMAND}` | All critical paths pass |
| Quality gate | `/validate {FEATURE_NAME}` | Score remains at least 90 and critical issues remain zero |
| Monitoring review | {MONITORING_DASHBOARD} | No active critical alerts |
| Stakeholder confirmation | {COMMUNICATION_CHANNEL} | Release status acknowledged |

---

## Handoff

| Topic | Owner | Notes |
|-------|-------|-------|
| Release ownership | {RELEASE_OWNER} | Accountable for deployment execution |
| Operations ownership | {OPERATIONS_OWNER} | Accountable for monitoring and incident response |
| Remediation ownership | {DELIVERY_OWNER} | Accountable for defects found after release |
