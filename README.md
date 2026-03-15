# AI Network Documentation

An automated network documentation project that discovers and documents network topology, inventory, and configuration from live device state.

## Project Video

Watch the project walkthrough on YouTube:

[![AI Network Documentation project video thumbnail](https://img.youtube.com/vi/31EVg64iUrI/hqdefault.jpg)](https://youtu.be/31EVg64iUrI)

Direct link: https://youtu.be/31EVg64iUrI

## Overview

This project provides tools and workflows to automatically build comprehensive network documentation by connecting to live network devices and collecting their state. It eliminates the need for manual documentation and ensures your network records are always up-to-date.

## Features

- **Live Topology Discovery**: Automatically discovers network topology by logging into devices and analyzing neighbor relationships
- **Automated Documentation**: Generates network diagrams and documentation from discovered state
- **Device Inventory**: Maintains an accurate inventory of network devices based on live data
- **NetBox Integration**: Populates and reconciles NetBox inventory from discovered topology

## Project Structure

```
.
├── .opencode/
│   ├── agents/          # Specialized AI agents for network tasks
│   ├── skills/          # Network discovery and sync workflows
│   └── commands/        # Custom commands
└── AGENTS.md            # Project documentation
```

## Getting Started

This project uses AI agents to perform network discovery and documentation tasks. The agents connect to live network devices to gather current state and configuration.

## License

This project is open source and available for use and modification.
