import logging
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from datetime import timedelta

import voluptuous as vol
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3600)

CONF_LIST_GAS_STATIONS = 'list_gas_stations'
ICON = 'mdi:gas-station'
SENSOR_PREFIX = 'Essence '

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LIST_GAS_STATIONS):
        vol.All(cv.ensure_list, [cv.string]),
})
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the file size sensor."""
    sensors = []
    for id in config.get(CONF_LIST_GAS_STATIONS):
        ville = get_ville(id)
        sensors.append(gas_station(id,ville,"Gazole"))
        sensors.append(gas_station(id, ville,"SP95"))

    if sensors:
        add_devices(sensors, True)
def get_ville(idstation):
    try:
        resp = urlopen("https://donnees.roulez-eco.fr/opendata/instantane")
        zipfile = ZipFile(BytesIO(resp.read()))
        tree = ET.parse(zipfile.open(zipfile.namelist()[0]))
        root = tree.getroot()
        for pdv in root.findall('pdv'):
            id=pdv.get('id')
            if (id == idstation):
                return(pdv.find("ville").text.replace("'"," ").replace("-"," "))
    except Exception:
        _LOGGER.error("Failed to retrieve the city for the carburant sensor")

class gas_station(Entity):
    def __init__(self, id, ville, essence):
        """Initialize the data object."""
        self._id = id
        self._last_updated = None
        self._name = SENSOR_PREFIX + ville + " " + essence
        self._unit_of_measurement = '€'
        self._icon = ICON
        self._type = essence

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update the sensor."""
        _LOGGER.info("Mise à jour pour l'id= %s", self._id)
        try:
            resp = urlopen("https://donnees.roulez-eco.fr/opendata/instantane")
            zipfile = ZipFile(BytesIO(resp.read()))
            tree = ET.parse(zipfile.open(zipfile.namelist()[0]))
            root = tree.getroot()
            _LOGGER.debug("Cherche carburant  id= %s", self._id)
            for pdv in root.findall('pdv'):
                id=pdv.get('id')
                if (id == self._id):
                    modif=0
                    for essence in pdv.iter('prix'):
                        if (essence.get("nom") == self._type):
                            self._state = essence.get("valeur")
                            self._last_updated = essence.get("maj")
                            modif=1
                    if (modif == 0):
                        self._state = None
                        self._last_updated = None
        except Exception:
            _LOGGER.error("Failed to retreive the webpage https://donnees.roulez-eco.fr/opendata/instantane ")
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """Return the state attributes of this device."""
        attr = {}
        if self._last_updated is not None:
            attr['Last Updated'] = self._last_updated
        return attr


