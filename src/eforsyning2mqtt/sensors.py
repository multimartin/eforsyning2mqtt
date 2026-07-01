"""
Definitions of all MQTT/Home Assistant sensors.
"""

SENSORS = {

    #
    # Temperatures
    #
    "temp-forward": {
        "name": "Forward temperature",
        "device_class": "temperature",
        "state_class": "measurement",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-up",
    },

    "temp-return": {
        "name": "Return temperature",
        "device_class": "temperature",
        "state_class": "measurement",
        "unit": "°C",
        "icon": "mdi:thermometer-chevron-down",
    },

    "temp-cooling": {
        "name": "Cooling",
        "device_class": "temperature",
        "state_class": "measurement",
        "unit": "°C",
        "icon": "mdi:snowflake-thermometer",
    },

    #
    # Energy
    #
    "energy-used": {
        "name": "Energy used",
        "device_class": "energy",
        "state_class": "total_increasing",
        "unit": "kWh",
        "icon": "mdi:lightning-bolt",
    },

    "energy-end": {
        "name": "Energy total",
        "device_class": "energy",
        "state_class": "total",
        "unit": "kWh",
        "icon": "mdi:counter",
    },

    "energy-use-prognosis": {
        "name": "Energy forecast",
        "device_class": "energy",
        "state_class": "measurement",
        "unit": "kWh",
        "icon": "mdi:chart-line",
    },

    #
    # Water
    #
    "water-used": {
        "name": "Water used",
        "state_class": "measurement",
        "unit": "m³",
        "icon": "mdi:water",
    },

    "water-end": {
        "name": "Water total",
        "state_class": "total",
        "unit": "m³",
        "icon": "mdi:water",
    },

    #
    # Billing
    #
    "billing/Amount-Paid": {
        "name": "Amount paid",
        "state_class": "measurement",
        "unit": "DKK",
        "icon": "mdi:cash-check",
    },

    "billing/Amount-Remaining": {
        "name": "Amount remaining",
        "state_class": "measurement",
        "unit": "DKK",
        "icon": "mdi:cash-minus",
    },

    "billing/MWh-Price": {
        "name": "MWh price",
        "state_class": "measurement",
        "unit": "DKK",
        "icon": "mdi:currency-usd",
    },

    "billing/M3-Price": {
        "name": "m³ price",
        "state_class": "measurement",
        "unit": "DKK",
        "icon": "mdi:water",
    },
}