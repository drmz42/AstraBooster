# AstraBooster

![AstraBooster — evidence-driven engineering for AI agents by DRMZ Lab](AstraBooster-social-preview.jpg)

**Outcome-first engineering for AI coding agents.**

AstraBooster is a lightweight, model-agnostic Agent Skill that helps coding agents deliver observable results rather than stop at plausible code, a green build, or a reassuring UI notification.

It gives an agent a repeatable method to define the real user outcome, choose verification proportional to risk, trace the result to its destination, correct defects within scope, and hand off evidence. No daemon, API key, paid service, or additional framework is required.

> An independent, community-developed skill. Not affiliated with or endorsed by OpenAI, Anthropic, Codex, Claude, or Astra. It does not unlock models or change reasoning-effort settings.

[Русский](README.ru.md) · [Strategy](docs/STRATEGY.md) · [Install](#installation) · [Examples](#examples) · [Security](SECURITY.md) · [MIT License](LICENSE)

## The problem

A feature can build successfully while failing its actual purpose:

- The contact form says **“Thanks”** but the message never arrives.
- The API responds **200 OK** but an asynchronous job or database write fails.
- The dashboard looks finished but its main action does nothing.
- The agent runs expensive end-to-end suites for a minor copy edit—or skips essential checks for a payment flow.

AstraBooster treats **verified outcomes** as the goal.

## The method

```mermaid
flowchart LR
    A[Outcome] --> B[Inspect]
    B --> C[Classify risk]
    C --> D[Implement]
    D --> E[Verify effect]
    E -->|Defect, safe to fix| D
    E -->|Verified| F[Evidence handoff]
    E -->|Needs approval| G[Explicit boundary]
```

**Five evidence levels:** changed → build-checked → behavior-checked → flow-checked → effect-confirmed. An agent must report the highest level it actually observed, not the level it hopes it achieved.

| Principle | What it does |
| --- | --- |
| **Evidence before claims** | Traces a user action through to persisted data, a test inbox, a job result, or another receiving system. |
| **Risk-proportional checks** | Uses a focused check for a small edit and deeper integration checks for auth, money, data or concurrency. |
| **Bounded self-correction** | Fixes concrete failures and reruns affected checks without endless blind retries. |
| **Safe autonomy** | Respects the repo policy, tool permissions and explicit approval gates for production or external effects. |
| **Independent review when useful** | Integrates with an existing second agent only when the change warrants the expense. |
| **Compact context** | Loads specialist references only when relevant; no duplicate global rules or heavyweight orchestration. |
| **UI acceptance** | Reviews a rendered screen, its primary action, mobile layouts and meaningful failure states. |

### Product strategy

AstraBooster is designed as **a portable quality layer, not another coding agent**. It works with existing tools, tests, repositories, project instructions and task coordinators. The core stays universal; private infrastructure policies belong in each project, not in the public skill.

Read the [product strategy and architecture](docs/STRATEGY.md) for positioning, workflow, use cases, differentiation and extension principles. [Стратегия по-русски](docs/STRATEGY.ru.md).

## Potential efficiency gains

AstraBooster is designed to reduce the **total cost of an accepted task**, rather than merely minimize the cost of a single model call. The following ranges are planning targets for complex, multi-step work; actual outcomes depend on task type, existing engineering practices, model, reasoning effort and tool access.

| Metric | Potential improvement |
| --- | ---: |
| Less manual intervention | 30–50% |
| Fewer correction cycles | 20–40% |
| Fewer missed defects | 20–40% |
| Higher overall productivity | 15–30% |
| Shorter time to accepted result | 10–25% |
| Lower total token usage per accepted task | 5–20% |

These are illustrative target ranges, not measured performance statistics. Simple edits may see little benefit or incur additional overhead. Higher reasoning effort and independent review can increase initial cost; the economic value comes from avoiding unnecessary rework across the entire delivery cycle.

## Installation

### ChatGPT (web and supported apps)

[**Download the latest plugin ZIP**](https://github.com/drmz42/AstraBooster/releases/latest) · Current release: [AstraBooster-2.2.0.zip](https://github.com/drmz42/AstraBooster/releases/download/v2.2.0/AstraBooster-2.2.0.zip)

**Install**

1. Download the named `AstraBooster-<version>.zip` release asset, not GitHub's automatically generated Source code archive.
2. Open [ChatGPT Plugins](https://chatgpt.com/plugins) on the web. In the plugin management area, choose **New Plugin** or the ZIP upload option available to your account/workspace.
3. Select the ZIP and confirm **Add plugin**. Open the plugin details and install it if prompted.

**Use**

In a supported ChatGPT conversation, type `@AstraBooster` and select the plugin from the mention menu (or open its card and choose **Try in chat**). Then describe your task. Selecting the actual plugin mention activates the installed integration; plain text alone is not proof that the skill was loaded.

Examples:

```text
@AstraBooster Audit this project's architecture, identify material risks,
and verify the conclusions against the available repository files.
```

```text
@AstraBooster Investigate this bug, reproduce it in an authorized test
environment, fix the cause, and report the verified result.
```

**Update:** Download the newer ZIP, open the existing plugin's details, and use **Upload new version** if available and permitted. Do not create a second plugin with the same package name: the importer may reject it as a duplicate.

ZIP upload and skill access depend on account, workspace, client and conversation mode. Installation and mention-based access have been confirmed in ChatGPT on the web; desktop/mobile use is conditional on the plugin being available in that client. AstraBooster does not grant repository, terminal, server or network access by itself, and cannot verify an outcome without the necessary tools and permissions.

See [OpenAI's plugin instructions](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) for current upload and update options.

### Codex and Claude Code

Copy the entire `astra-booster/` directory into a supported skill location:

| Host | Project scope | User scope |
| --- | --- | --- |
| Codex | `.agents/skills/astra-booster/` | `~/.agents/skills/astra-booster/` |
| Claude Code | `.claude/skills/astra-booster/` | `~/.claude/skills/astra-booster/` |

The installed folder must contain `SKILL.md`, `references/`, and `agents/`. **Keep existing `AGENTS.md` and `CLAUDE.md` intact.** Optional additions are in [examples](examples/).

Invoke `$astra-booster` in Codex. In supported Claude Code installations use `/astra-booster`, or allow skill discovery from its description. Tool availability and authorizations remain controlled by the host.

## Recommended reasoning effort for Astra

For quality-first, complex engineering tasks with GPT-6.2 Astra, AstraBooster recommends **Extra High (`xhigh`)**. Use **Maximum (`max`)** for particularly demanding tasks when the selected model, host and budget support it.

| Workload | Astra reasoning effort |
| --- | --- |
| Complex implementation, debugging, architecture and end-to-end acceptance | `xhigh` |
| High-risk or exceptionally demanding engineering and independent review | `max`, when supported and justified |

Select the model and effort in your agent's model settings before starting the task, then invoke `$astra-booster`. This is a quality-first recommendation, not a mandatory runtime requirement: simple tasks may use less effort, and other compatible models may use their own supported settings. Higher effort can increase latency and token usage; compare actual quality and cost for your workload. AstraBooster cannot change these settings itself.

Official references: [GPT-6.2 Astra](https://developers.openai.com/api/docs/models/gpt-6.2-astra) · [Reasoning effort](https://developers.openai.com/api/docs/guides/reasoning).

## Examples

**Contact form**

```text
$astra-booster Verify the contact form in staging. Submit a uniquely tagged
request and confirm that the same tag reached the permitted test inbox/CRM.
If delivery cannot be observed, say exactly how far verification reached.
```

**API and persistence**

```text
$astra-booster Fix this API integration. Reuse the current architecture,
check a successful flow and one important failure path, read back the stored
record, and report the real evidence.
```

**Product UI**

```text
$astra-booster Complete the dashboard. Open the rendered UI at desktop and
mobile sizes, exercise the main action and fix important usability defects.
```

**Multi-agent change**

```text
$astra-booster Complete this multi-file feature. Respect existing locks
and task ownership; request independent review only for material risk.
Hand off changed files, actual checks and any blockers.
```

## Repository layout

```text
astra-booster/
  SKILL.md                  # Compact execution protocol
  agents/openai.yaml        # Optional UI metadata
  references/               # Read only what the task needs
docs/                       # Product strategy and architecture
examples/                   # Optional project rules, never auto-merged
tests/                      # Structural validator and scenario library
```

## Scope and security

AstraBooster is a skill, **not an access-control boundary**. It cannot grant permissions or verify inaccessible systems. It neither performs production operations automatically nor authorizes payments, migrations, notifications or destructive actions. Those require the applicable host permissions and user approval. The final report must distinguish confirmed behavior from partial verification.

See [Security](SECURITY.md), [evaluation guidance](astra-booster/references/evaluation.md), and [contributing](CONTRIBUTING.md).

## Licensing and provenance

The public package contains an independent implementation of general software-delivery and acceptance-testing principles. See [NOTICE](NOTICE.md). Original materials in this repository are offered under the [MIT License](LICENSE).
