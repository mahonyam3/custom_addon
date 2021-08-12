import appdaemon.plugins.hass.hassapi as hass

class Restart(hass.Hass):

    def initialize(self):

        self.listen_state(self.rest, "input_boolean.restartapp", attribute = 'state')

    def rest(self, entity, attribute, old, new, kwargs):

        self.restart_app("man")