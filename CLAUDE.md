# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Context

This is **AI Engineering Hackathon — Challenge 3: Supporting Casework Decisions**. The goal is a prototype tool that helps a caseworker understand a case quickly, see relevant policy, know what action is required, and flag deadline breaches — without requiring an LLM to run.

The current build direction adapts the original government casework challenge into a **Claude License application decision system**, where a caseworker evaluates license applications against four criteria: profession, objective, income background, and prior 60-day free trial usage (granted on the basis of a GitHub project technical demonstration).

## No Build System

There is no package.json, bundler, or test runner. The prototype is a **self-contained `index.html`** using React 18 + Babel Standalone + Tailwind CSS via CDN — open directly in any browser, no server needed. All data is embedded as JS constants in the HTML.

The separate JSON files (`cases.json`, `policy-extracts.json`, `workflow-states.json`, and the Claude-license equivalents) serve as the canonical data source and schema reference, not as runtime-loaded files.

## Data Architecture

Three JSON files define the entire domain model. They are coupled: a case's `case_type` determines which policies and which workflow branch apply.

**`cases.json`** — 10 synthetic cases, each with:
- `case_type`: `benefit_review` | `licence_application` | `compliance_check`
- `status`: the current workflow state (must be a valid state from `workflow-states.json`)
- `applicant`: name, reference, date_of_birth
- `timeline[]`: ordered events (`date`, `event`, `note`) — the audit trail
- `case_notes`: free-text summary from the previous officer

**`policy-extracts.json`** — 10 policies, each with:
- `policy_id`: e.g. `POL-BR-003`
- `applicable_case_types[]`: which case types this policy governs
- `body`: the rule text including thresholds (28-day reminder, 56-day escalation, etc.)

**`workflow-states.json`** — a state machine for all three case types. Each state has:
- `allowed_transitions[]`: valid next states
- `required_actions[]`: what the caseworker must do in this state
- `escalation_thresholds` (on `awaiting_evidence`): `reminder_days` and `escalation_days`

**Policy-to-case-type mapping:**
- `POL-BR-*` → `benefit_review`
- `POL-LA-*` → `licence_application`
- `POL-CC-*` → `compliance_check`

## Claude License Scenario Extension

The Claude license variant uses the same three-file structure but with a new case type `claude_license_application`. Each case carries additional fields:
- `applicant.profession`, `applicant.income_annual`, `applicant.income_band`
- `applicant.github_username`
- `objective` (string)
- `github_demonstration`: `{ project_name, stars, commits_last_30_days, technical_quality, use_case_relevance, has_readme, has_tests }`
- `prior_license`: `{ had_60_day_free, usage_sessions, usage_rating, output_quality_notes }` — captures the prior decision to award a 60-day free trial based on a GitHub demonstration

**Decision criteria weights (for the recommendation engine):**
- Profession appropriateness — which license tier applies (academic/public sector/educational/research/commercial)
- Objective alignment — public benefit, open-source, educational, or pure commercial
- Income band — low (<£30k), low-mid (£30–50k), mid (£50–80k), high (>£80k)
- GitHub demonstration quality — `poor` / `adequate` / `good` / `excellent` × relevance `low` / `medium` / `high`
- Prior trial utilisation — session count + output quality; very low usage (<20 sessions) disqualifies free renewal

## Key Domain Rules (from policy extracts)

| Trigger | Rule |
|---|---|
| Evidence outstanding 28 days | Caseworker issues reminder |
| Evidence outstanding 56 days | Escalate to team leader |
| Benefit award increase >£50/week | Requires team leader sign-off |
| Benefit reduction/cessation | Mandatory reconsideration notice required |
| Licence application: ≥2 substantive objections | Must refer to senior caseworker |
| Compliance check: serious breach | Escalate to senior officer within 2 working days |
| 60-day free trial: no GitHub project | Ineligible — reject free tier |
| 60-day free trial: GitHub quality <adequate | Ineligible — reject free tier |
| Free renewal: <20 sessions in trial | Disqualified from free access |

## UI Pattern Reference

The challenge references the [GOV.UK Design System](https://design-system.service.gov.uk). The prototype follows GOV.UK conventions: black header bar, blue (#1d70b8) links/primary actions, green (#00703c) for approval, red (#d4351c) for rejection, yellow (#ffdd00 + black text) for warnings/escalation.

## What the Prototype Must Demo

Per the challenge brief, a complete prototype can be built without a live LLM and still score full marks. The required features are:
1. Display a case clearly (applicant, timeline, notes)
2. Surface the relevant policy matched by case type
3. Show current workflow state and required next action
4. Flag evidence outstanding beyond the policy threshold
5. Produce a decision recommendation (rule-based is sufficient)

The "AI" layer (case summarisation, free-text objective assessment) is clearly labelled as mocked where not backed by a live model.
