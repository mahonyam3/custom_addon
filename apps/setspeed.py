import appdaemon.plugins.hass.hassapi as hass

class SetSpeed(hass.Hass):

    def initialize(self):

        self.listen_state(self.set, "input_number.camspeed", attribute = 'state')

    def set(self, entity, attribute, old, new, kwargs):

        y = int(self.get_state("input_select.camera_list", attribute="state"))

        x = int(float(new))

        self.log(x)

        setlist = [1, 10]

        minpan = {
            1:1,
            2:1,
            3:1
        }

        mintilt = {
            1:1,
            2:1,
            3:1
        }

        maxpan = {
            1:18,
            2:18,
            3:18
        }

        maxtilt = {
            1:14,
            2:14,
            3:14
        }

        settilt = round(1 + ((maxtilt[y]-mintilt[y])/(setlist[1]-setlist[0]))*(x-1))
        if settilt < 10:
            strsettilt = "0"+str(settilt)
        else:
            strsettilt = str(settilt)

        setpan = round(1 + ((maxpan[y]-minpan[y])/(setlist[1]-setlist[0]))*(x-1))
        if setpan < 10:
            strsetpan = "0"+str(setpan)
        else:
            strsetpan = str(setpan)

        speed = strsetpan + " " + strsettilt

        self.set_state('input_text.speedcount', state=speed)

        self.restart_app("man")