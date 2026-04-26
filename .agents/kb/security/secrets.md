# Secret Detection Patterns

> **Domain:** Security
> **Purpose:** Regex patterns and heuristics to detect sensitive credentials and PII in codebases and logs before execution or commit.

## 1. High-Confidence Patterns (Exact Matches)

These patterns match specific, known formats of credentials. If these match, the confidence score is **HIGH (0.95)**.

| Secret Type | Regex Pattern | Action |
|-------------|---------------|--------|
| AWS Access Key | ``(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}`` | REFUSE & REDACT |
| AWS Secret Key | ``(?i)aws(.{0,20})?(?-i)['\"][0-9a-zA-Z\/+]{40}['\"]`` | REFUSE & REDACT |
| GitHub Token | ``(gh[pousr]_[A-Za-z0-9_]{36,255})`` | REFUSE & REDACT |
| Slack Token | ``xox[baprs]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{32}`` | REFUSE & REDACT |
| Google Cloud Key | ``AIza[0-9A-Za-z\\-_]{35}`` | REFUSE & REDACT |
| Stripe API Key | ``(sk|rk)_live_[0-9a-zA-Z]{24}`` | REFUSE & REDACT |
| JWT Token | ``eyJ[a-zA-Z0-9_=]+(?:\.eyJ[a-zA-Z0-9_=]+){2}`` | WARN & VERIFY |

## 2. Heuristic Patterns (Variable Names)

These patterns match variable assignments. They may produce false positives. If these match, confidence is **MEDIUM (0.75)** and the user must be asked for confirmation.

| Pattern Target | Regex Pattern | Action |
|----------------|---------------|--------|
| Generic Passwords | ``(?i)(password|passwd|pwd)[\s]*[:=][\s]*['\"][^\s]+['\"]`` | ASK USER |
| Generic Secrets | ``(?i)(secret|token|api_key|apikey)[\s]*[:=][\s]*['\"][^\s]+['\"]`` | ASK USER |
| Database URIs | ``[a-zA-Z]+:\/\/[a-zA-Z0-9_]+:[a-zA-Z0-9_]+@[a-zA-Z0-9_.-]+:[0-9]+\/[a-zA-Z0-9_]+`` | ASK USER |

## 3. Data Loss Prevention (PII)

Patterns for detecting Personal Identifiable Information.

- **Email Addresses:** `[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+`
- **Social Security Numbers (US):** `\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b`
- **Credit Card Numbers:** `\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\b`

## Implementation Guidance

When the `security-auditor` agent runs:
1. Scan the output strings or `git diff` using these patterns.
2. If any **High-Confidence** pattern matches, immediately trigger a **Hard Stop**, redact the match, and notify the user.
3. Recommend adding the offending file to `.gitignore`.
