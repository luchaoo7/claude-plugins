# Claude Plugins

A collection of plugins for Claude, published as the `luchaoo7-plugins` marketplace.

## Plugins

| Plugin | Description |
|--------|-------------|
| [project-discovery](./project-discovery) | Takes a software project from a raw idea to approved planning documents — PRD, MVP scope, lightweight TRD, UX flows and wireframes, design system and database schema — with a decision log and requirement traceability. |

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

### Claude desktop app / claude.ai

Add this repository as a plugin marketplace from the plugin settings, or download a plugin's folder and upload it.

## Usage

Each plugin has its own README covering what it does and how to use it. Follow the links in the table above.

## Licence

Each plugin's licence is in its own folder.
