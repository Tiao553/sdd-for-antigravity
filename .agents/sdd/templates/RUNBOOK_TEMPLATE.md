# RUNBOOK: {Feature Name}

> Production deployment steps and operational procedures

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Date** | {YYYY-MM-DD} |
| **Status** | {Draft / Approved} |

---

## Pre-flight Checklist

- [ ] All CI/CD pipelines passed
- [ ] Database backups verified
- [ ] Required secrets injected into production environment
- [ ] Smoke tests verified in staging

---

## Deployment Steps

| Step | Action | Verifier |
|------|--------|----------|
| 1 | {Deploy action: e.g., apply Terraform} | {Command/Check} |
| 2 | {Deploy action: e.g., run dbt run} | {Command/Check} |

---

## Rollback Plan

**Trigger condition:** {When to rollback, e.g., >5% error rate}

1. {Rollback step 1}
2. {Rollback step 2}

---

## Observability & SLA

- **Primary Metrics:** {Metrics to monitor, e.g., CPU, memory, row count}
- **Log Location:** {Where to find logs, e.g., Datadog, CloudWatch}
- **Alerts Configured:** {List of critical alerts}
- **SLA:** {Uptime or latency target}
