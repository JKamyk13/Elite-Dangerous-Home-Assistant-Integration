"""Constants for the Elite Dangerous integration."""

from datetime import timedelta

DOMAIN = "elite_dangerous"
NAME = "Elite Dangerous"
BUILTIN_CLIENT_ID = "82485895-c9e5-46d7-8a17-b40ab0624d5d"

AUTHORIZATION_URL = "https://auth.frontierstore.net/auth"
TOKEN_URL = "https://auth.frontierstore.net/token"
CAPI_URL = "https://companion.orerve.net"

UPDATE_INTERVAL = timedelta(minutes=1)
FLEET_CARRIER_UPDATE_INTERVAL = timedelta(minutes=10)
