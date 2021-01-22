"""Platform for sensor integration."""
import logging
from datetime import datetime, timedelta

import requests
import json
import re
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import PLATFORM_SCHEMA
from homeassistant.const import *

_LOGGER = logging.getLogger(__name__)
DEFAULT_URL = "https://stadtplan.dresden.de/project/cardo3Apps/IDU_DDStadtplan/abfall/ical.ashx"
DEFAULT_DATE_FROM = datetime.now().strftime("%d.%m.%Y")
DEFAULT_DATE_UNTIL = (datetime.now() + timedelta(days=10)).strftime("%d.%m.%Y")
DEFAULT_GARBAGES = ["Bio", "Restabfall", "Blaue", "Gelbe"]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LOCATION): cv.string,
    vol.Optional(CONF_URL, default=DEFAULT_URL): cv.string,
    vol.Optional(CONF_DATE_FROM, default=DEFAULT_DATE_FROM): cv.string,
    vol.Optional(CONF_DATE_UNTIL, default=DEFAULT_DATE_UNTIL): cv.string,
    vol.Optional(CONF_GARBAGES, default=DEFAULT_GARBAGES): cv.ensure_list
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([SrdSensor(config)])


class SrdSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, config):
        self._state = None
        self._name = config.get(CONF_NAME)
        self.location = config.get(CONF_LOCATION)
        self.url = config.get(CONF_URL)
        self.date_from = config.get(CONF_DATE_FROM)
        self.date_until = config.get(CONF_DATE_UNTIL)
        self.data = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.data

    def update(self):
        attributes = {}
        srd_json = []
        srd_tab = []
        init = {}
        """Initialized JSON Object"""
        init['title_default'] = '$title'
        init['line1_default'] = '$days'
        init['icon'] = 'mdi:trash-can'
        srd_json.append(init)

        ical = self.get_ical(self.url, self.location, self.date_from, self.date_until)

        for garbage in self.garbages:
            srd_items = {}
            srd_items['title'] = garbage
            srd_items['days'] = self.parse_ical(ical['text'], garbage)

            srd_tab.append(srd_items)

        srd_json = srd_json + srd_tab
        attributes['data'] = json.dumps(srd_json)
        if ifs_movies["success"].__eq__("True"):
            self._state = "Success"
        else:
            self._state = "Failure"
        self.data = attributes

    def get_ical(self, url, location, date_from, date_until):
        req = "{0}?STANDORT={1}&DATUM_VON={2}&DATUM_BIS={3}".format(
            url,
            loction, date_from, date_until)

        res = requests.get(req)

        ical = {}
        ical['text'] = res.text()
        ical['status_code'] = res.status_code()

        return ical

    def parse_ical(self, ical):
        days = '42'

        return days

    def parse_date(self, airdate):
        """
        matcher = re.match(PATTERN_DATE, airdate)
        try:
            if matcher:
                airdate = datetime.strptime(airdate, "%Y-%m-%d").isoformat() + "Z"
            else:
                airdate = datetime.strptime(datetime.strptime(airdate, '%d %b %Y').strftime("%Y-%m-%d"),
                                        "%Y-%m-%d").isoformat() + "Z"
        except:
            _LOGGER.error("Unknow date format")
        """
        return ''
