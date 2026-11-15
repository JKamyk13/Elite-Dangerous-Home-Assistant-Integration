# Elite Dangerous to Home Assistant

> **Project status: Concept / Early Planning**

## Overview

**Elite Dangerous to Home Assistant** is a planned custom integration for Home Assistant that brings Elite Dangerous Commander data into Home Assistant.

The integration is designed to communicate directly with the **Frontier Companion API (CAPI)** using OAuth 2.0 authentication.

The goal is to provide Home Assistant entities representing selected in-game information, including Commander credits, Fleet Carrier credits, current star system, docking location, and recent in-game activity.

The project is intended to process API data locally within Home Assistant without requiring a separate Windows application or an external Journal service.

## Current Status

**This repository currently contains only the project concept and planning documentation.**

- The Home Assistant integration has not yet been implemented.
- No downloadable integration files are available.
- No installation package or ZIP archive is available.
- Access to the Frontier Companion API (CAPI) has been requested.
- The project is currently waiting for Frontier Developments to review and approve the API access application.
- OAuth 2.0 authentication has not yet been implemented.
- API communication, Journal retrieval, and sensor functionality are not yet available.
- The project has not been tested with a live Elite Dangerous account.

## Planned Features

The following features are planned:

- Frontier Companion API (CAPI) authentication using OAuth 2.0.
- Direct retrieval of Elite Dangerous Journal data from Frontier.
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
- OAuth 2.0 with PKCE, subject to Frontier API support and configuration
- HTTP/HTTPS communication
- Home Assistant entities and services

## Data Sources

The planned primary data source is the **Frontier Companion API (CAPI)**.

The integration is intended to retrieve Commander information and Journal data directly from Frontier's API.

No dependency on Inara API, local Elite Dangerous Journal files, or third-party Journal hosting services is planned.

## Installation

**Installation is not currently possible.**

There are no integration files to download or install. Installation instructions will be published once a working implementation is available.

## Disclaimer

This is an independent community project. It is not affiliated with, endorsed by, or officially supported by Frontier Developments, Elite Dangerous, or Home Assistant.

All product and company names are the property of their respective owners.

## Development

The project is currently in the research and planning stage.

Implementation depends partly on approval of the Frontier Companion API access application. Authentication, API communication, data parsing, and Home Assistant entity support will be developed and tested after API access becomes available.

Development progress and updates will be published in this repository.
