# Elite Dangerous to Home Assistant

A custom Home Assistant integration for monitoring your Elite Dangerous Commander and Fleet Carrier data through the Frontier Companion API (CAPI).

## Overview

**Elite Dangerous to Home Assistant** brings selected in-game information from Elite Dangerous into Home Assistant.

The integration communicates with the Frontier Companion API (CAPI) and exposes Commander and Fleet Carrier information as Home Assistant entities.

You can monitor your in-game status, credits, ship, and location directly from your Home Assistant dashboard and use this information in automations.

## Features

The integration provides the following entities:

| Entity | Description |
|---|---|
| Commander Credits | Current credit balance of your Commander. |
| Current Ship | Name of the ship currently used by your Commander. |
| Current Station | Station or settlement where your Commander is currently located. |
| Current System | Current star system. |
| Docked | Indicates whether your Commander is currently docked. |
| Fleet Carrier Balance | Current credit balance of your Fleet Carrier. |

## Installation

Choose the installation method that matches your Home Assistant version.

### Home Assistant 2026.11 and newer – Marketplace

The Marketplace is built into Home Assistant and does not require a separate installation.

[![Add Marketplace Repository to My Home Assistant](https://my.home-assistant.io/badges/marketplace_repository.svg)](https://my.home-assistant.io/redirect/marketplace_repository/?owner=JKamyk13&repository=Elite-Dangerous-Home-Assistant-Integration&category=integration)

1. Click the **OPEN MARKETPLACE REPOSITORY ON MY HA** button above.
2. Home Assistant will open the Marketplace with this repository preselected.
3. Add the repository to your Marketplace.
4. Open the repository page.
5. Select **Install**.
6. Restart Home Assistant if requested.

### Home Assistant 2026.10 and older – HACS

For older Home Assistant versions, the integration can be installed using HACS.

[![Open HACS Repository in My Home Assistant](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=JKamyk13&repository=Elite-Dangerous-Home-Assistant-Integration&category=integration)

1. Click the **OPEN HACS REPOSITORY ON MY HA** button above.
2. Add the repository as a custom repository if prompted.
3. Open HACS and download **Elite Dangerous to Home Assistant**.
4. Restart Home Assistant.

## Configuration

After installing the integration:

1. Open **Settings → Devices & Services**.
2. Select **Add Integration**.
3. Search for **Elite Dangerous**.
4. Select the integration.
5. Choose which Client ID you want to use:
   - **Use the integration Client ID** – use the Client ID provided by the integration author.
   - **Use your own Client ID** – enter your own Client ID from a Frontier Developer application.
6. Complete the Frontier OAuth authorization process when prompted.

The Client ID can be selected during integration setup. There is no need to edit integration files manually.

## Home Assistant Entities

The integration exposes the following information:

- **Commander Credits** – Monitor your personal in-game credits.
- **Current Ship** – Track which ship you are currently flying.
- **Current Station** – Monitor your current docking location.
- **Current System** – Track your current star system.
- **Docked** – Check whether your Commander is docked.
- **Fleet Carrier Balance** – Monitor your Fleet Carrier's available credits.

Entity IDs may depend on the configured Commander name.

## Data Source and Authentication

The integration uses the **Frontier Companion API (CAPI)** to retrieve Elite Dangerous account information.

Authentication is handled through OAuth 2.0.

Users can choose to use the project-provided Client ID or configure their own Frontier Client ID.

The integration does not require local access to Elite Dangerous Journal files or a separate Windows application.

## Disclaimer

This software is provided "as is", without any warranty of any kind, express or implied.

**Use it at your own risk.**

This is an independent community project. It is not affiliated with, endorsed by, or officially supported by Frontier Developments, Elite Dangerous, or Home Assistant.

All product and company names are the property of their respective owners.
