import logging
import requests
from typing import Any
import voluptuous as vol
from homeassistant.const import (
    CONF_URL,
    CONF_TOKEN,
    CONF_VERIFY_SSL,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.notify import (
    ATTR_TITLE_DEFAULT,
    ATTR_TITLE,
    ATTR_DATA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

PRIORITIES = {
    "high": 10,
    "normal": 5,
    "default": 5,
    "low": 2,
    "min": 0,
    "none": 0
}
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_URL): cv.url, vol.Required(CONF_TOKEN): cv.string})
_LOGGER = logging.getLogger(__name__)

def get_service(hass, config, discovery_info=None):
    url = config.get(CONF_URL)
    token = config.get(CONF_TOKEN)
    verify_ssl = config.get(CONF_VERIFY_SSL, True)
    msg_blacklist = config.get('msg_blacklist', [])

    _LOGGER.info('Service created')

    return HassAgentNotificationService(hass, url, token, verify_ssl, msg_blacklist)


class HassAgentNotificationService(BaseNotificationService):
    def __init__(self, hass, url, token, verify_ssl, msg_blacklist):
        self._url = url
        self._token = token
        self._hass = hass
        self._verify_ssl = verify_ssl
        self._msg_blacklist = msg_blacklist

        if not self._url.endswith('/'):
            self._url += '/'
        self._url += 'message'

    def send_request(self, data):
        return requests.post(self._url, headers={'X-Gotify-Key': self._token}, json=data, verify=self._verify_ssl, timeout=10)

    async def async_send_message(self, message: str, **kwargs: Any):
        if message.strip() in self._msg_blacklist:
            return

        title = kwargs.get(ATTR_TITLE, ATTR_TITLE_DEFAULT)
        data = kwargs.get(ATTR_DATA, None)
        if data is None:
            data = dict()

        priority = data.get('priority', 5)
        if type(priority) is str:
            priority = PRIORITIES.get(priority, 5)

        payload = {
            'title': title,
            'message': message,
            'priority': priority
        }
        if 'extras' in data:
            payload['extras'] = data.get('extras')
        
        _LOGGER.debug('Sending message to gotify: %s', payload)

        try:
            response = await self.hass.async_add_executor_job(self.send_request, payload)
            response.raise_for_status()
        except Exception as ex:
            _LOGGER.error('Error while sending gotify message: %s', ex)
