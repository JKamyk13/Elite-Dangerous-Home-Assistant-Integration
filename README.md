# Inara to Home Assistant – Elite Dangerous

> **Project status: Concept / Early Planning**

## Overview

**Inara to Home Assistant** is a planned custom integration for Home Assistant, designed to bring Elite Dangerous Commander data into Home Assistant.

The project aims to retrieve Commander information and Journal data using the Frontier Companion API (CAPI), potentially with the help of an external Journal service such as Journal Limpet.

The long-term goal is to provide Home Assistant entities representing selected in-game information, including Commander credits, Fleet Carrier credits, current star system, docking location, and recent activity.

## Current Status

**This repository currently contains only the project concept and planning documentation.**

- The Home Assistant integration has not been implemented.
- No downloadable integration files are available.
- No installation package or ZIP archive is available.
- Access to the Frontier Companion API (CAPI) has been requested. **I am currently waiting for Frontier Developments to approve the API access application.**
- Frontier API authentication has not yet been implemented.
- Data retrieval and sensor functionality have not been completed.
- The project has not been tested with a live Elite Dangerous account.

## Planned Features

The following features are planned:

- Frontier Companion API authentication.
- Retrieval of Elite Dangerous Journal data.
- Commander credit balance.
- Fleet Carrier credit balance.
- Current star system.
- Current station or settlement.
- Docking status (`IDLE` when not docked).
- Last recorded in-game activity.
- Manual data synchronization through Home Assistant.

These features are planned and are not currently available.

## Planned Technology

- Home Assistant Custom Integration
- Python
- Frontier Companion API (CAPI)
- OAuth 2.0 authentication
- HTTP/HTTPS data retrieval

An external Journal service may be evaluated as an alternative to implementing the entire Frontier authentication and Journal retrieval workflow directly.

## Installation

**Installation is not currently possible.**

There are no integration files to download or install. Instructions will be added once a working implementation is available.

## Disclaimer

This is an independent community project concept. It is not affiliated with, endorsed by, or officially supported by Frontier Developments, Elite Dangerous, or Home Assistant.

All product and company names are the property of their respective owners.

## Development

The project is currently in the research and planning stage. Implementation details, API access requirements, and the final architecture are still being evaluated.

Development progress and updates will be published in this repository as the project progresses.
