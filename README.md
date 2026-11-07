# Claude Plugins

A collection of plugins for Claude, published as the `luchaoo7-plugins` marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [project-discovery](./project-discovery) | Takes a new or existing software project to approved planning documents — PRD, MVP scope, lightweight TRD, UX flows and wireframes, design system and database schema — with a decision log and requirement traceability. |
| [vibe-code-auditor](./vibe-code-auditor) | Audits codebases, especially AI-generated / vibe-coded ones, for bloat, duplication, dead code, complexity, security risks and architecture weaknesses, then produces a prioritised report with before/after refactoring examples and applies only the changes you approve. |

## Installation

Add the marketplace once, then install any plugin from it.

### Claude Code

From your terminal, without starting a session:

```
claude plugin marketplace add luchaoo7/claude-plugins
claude plugin install <plugin-name>@luchaoo7-plugins
```

Or inside a session:

```
/plugin marketplace add luchaoo7/claude-plugins
/plugin install <plugin-name>@luchaoo7-plugins
/reload-plugins
```

#### Updating

To pick up new plugins and new versions, refresh the marketplace and then update the plugins you have installed.

From your terminal:

```
claude plugin marketplace update luchaoo7-plugins
claude plugin update <plugin-name>@luchaoo7-plugins
```

Or inside a session:

```
/plugin marketplace update luchaoo7-plugins
/plugin update <plugin-name>@luchaoo7-plugins
/reload-plugins
```

### Claude desktop app / claude.ai

Add this repository as a plugin marketplace from the plugin settings, or download a plugin's folder and upload it.

## Usage

Each plugin has its own README covering what it does and how to use it. Follow the links in the table above.

## Licence

Each plugin's licence is in its own folder.
