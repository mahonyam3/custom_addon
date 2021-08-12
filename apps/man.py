import appdaemon.plugins.hass.hassapi as hass
import socket

class ManualControl(hass.Hass):

    def initialize(self):

        speed = self.get_state("input_text.speedcount", attribute="state")

        self.log(speed)

        self.status = False

        self.cams = {
            1:{
                'status':False,
                'socket':socket.socket(),
                'host':"10.110.15.25",
                'port':5678
            },
            2:{
                'status':False,
                'socket':socket.socket(),
                'host':"10.110.15.49",
                'port':5679
            },
            3:{
                'status':False,
                'socket':socket.socket(),
                'host':"10.110.15.54",
                'port':5680
            }
        }

        self.coms = {
            "up":bytes.fromhex("81 01 06 01 " + speed + " 03 01 FF"),
            "stop":bytes.fromhex("81 01 06 01 10 10 03 03 FF"),
            "down":bytes.fromhex("81 01 06 01 " + speed + " 03 02 FF"),
            "right":bytes.fromhex("81 01 06 01 " + speed + " 02 03 FF"),
            "left":bytes.fromhex("81 01 06 01 " + speed + " 01 03 FF"),
            "zoom+":bytes.fromhex("81 01 04 07 27 FF"),
            "zoom-":bytes.fromhex("81 01 04 07 37 FF"),
            "stopzoom":bytes.fromhex("81 01 04 07 00 FF"),
            "1":bytes.fromhex("81 01 04 3F 01 01 FF"), 
            "2":bytes.fromhex("81 01 04 3F 01 02 FF"), 
            "3":bytes.fromhex("81 01 04 3F 01 03 FF"), 
            "4":bytes.fromhex("81 01 04 3F 01 04 FF"),
            "5":bytes.fromhex("81 01 04 3F 01 05 FF"),
            "6":bytes.fromhex("81 01 04 3F 01 06 FF"),
            "7":bytes.fromhex("81 01 04 3F 01 07 FF"),
            "8":bytes.fromhex("81 01 04 3F 01 08 FF"),
            "9":bytes.fromhex("81 01 04 3F 01 09 FF"),
            "10":bytes.fromhex("81 01 04 3F 01 10 FF"),
            "99":bytes.fromhex("81 01 04 3F 01 63 FF"),
            "on":bytes.fromhex("81 01 04 00 02 FF"),
            "off":bytes.fromhex("81 01 04 00 03 FF")
        }

        self.log("ManualControl Active")
        self.listen_state(self.up, "input_boolean.up", attribute = 'state')
        self.listen_state(self.down, "input_boolean.down", attribute = 'state')
        self.listen_state(self.right, "input_boolean.right", attribute = 'state')
        self.listen_state(self.left, "input_boolean.left", attribute = 'state')
        self.listen_state(self.stop, "input_boolean.stop", attribute = 'state')
        self.listen_state(self.zoomin, "input_boolean.zoom_in", attribute = 'state')
        self.listen_state(self.zoomout, "input_boolean.zoom_out", attribute = 'state')
        self.listen_state(self.setpreset, "input_boolean.set_preset", attribute = 'state')
#        self.listen_state(self.gotopreset, "input_number.comtocam", attribute = 'state')
        self.listen_state(self.on, "input_boolean.camson", attribute = 'state')
        self.listen_state(self.off, "input_boolean.camsoff", attribute = 'state')

    def send(self, cam, cmd):

        try:
            cam["socket"].send(cmd)
            self.log(str(cmd) + " success")
        except socket.error as msg:
            while not cam["status"]:
                # attempt to reconnect, otherwise sleep for 2 seconds
                    try:
                        cam["socket"].connect( (cam["host"], cam["port"]) )
                        cam["status"] = True
                        self.log( "re-connection successful" )
                    except socket.error:
                        cam["status"] = False
                        self.log( "re-connection failure" )
                        sleep( 2 )

        cam["socket"].send(cmd)
        self.log(str(cmd) + " success")

    def up(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.down', state='off')
        self.set_state('input_boolean.right', state='off')
        self.set_state('input_boolean.left', state='off')
        self.set_state('input_boolean.stop', state='off')
        self.set_state('input_boolean.zoom_in', state='off')
        self.set_state('input_boolean.zoom_out', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        if new == "on":

            self.log("UP")

            camlist = self.get_state("input_select.camera_list", attribute="state")

            x = int(float(camlist))

            self.send(self.cams[x], self.coms["up"])

            self.log("send UP")

            self.set_state('input_boolean.up', state='off')

    def down(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.up', state='off')
        self.set_state('input_boolean.right', state='off')
        self.set_state('input_boolean.left', state='off')
        self.set_state('input_boolean.stop', state='off')
        self.set_state('input_boolean.zoom_in', state='off')
        self.set_state('input_boolean.zoom_out', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        if new == "on":

            self.log("DOWN")

            camlist = self.get_state("input_select.camera_list", attribute="state")

            x = int(float(camlist))

            self.send(self.cams[x], self.coms["down"])

            self.log("send DOWN")

            self.set_state('input_boolean.down', state='off')

    def right(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.up', state='off')
        self.set_state('input_boolean.down', state='off')
        self.set_state('input_boolean.left', state='off')
        self.set_state('input_boolean.stop', state='off')
        self.set_state('input_boolean.zoom_in', state='off')
        self.set_state('input_boolean.zoom_out', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        if new == "on":

            self.log("RIGHT")

            camlist = self.get_state("input_select.camera_list", attribute="state")

            x = int(float(camlist))

            self.send(self.cams[x], self.coms["right"])

            self.log("send RIGHT")

            self.set_state('input_boolean.right', state='off')

    def left(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.up', state='off')
        self.set_state('input_boolean.down', state='off')
        self.set_state('input_boolean.right', state='off')
        self.set_state('input_boolean.stop', state='off')
        self.set_state('input_boolean.zoom_in', state='off')
        self.set_state('input_boolean.zoom_out', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        if new == "on":

            self.log("LEFT")

            camlist = self.get_state("input_select.camera_list", attribute="state")

            x = int(float(camlist))

            self.send(self.cams[x], self.coms["left"])

            self.log("send LEFT")

            self.set_state('input_boolean.left', state='off')

    def stop(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.up', state='off')
        self.set_state('input_boolean.down', state='off')
        self.set_state('input_boolean.right', state='off')
        self.set_state('input_boolean.left', state='off')
        self.set_state('input_boolean.zoom_in', state='off')
        self.set_state('input_boolean.zoom_out', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        self.log("STOP")

        camlist = self.get_state("input_select.camera_list", attribute="state")

        x = int(float(camlist))

        self.send(self.cams[x], self.coms["stop"])
        self.send(self.cams[x], self.coms["stopzoom"])

        self.log("send STOP")

        self.set_state('input_boolean.stop', state='off')

    def zoomin(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.up', state='off')
        self.set_state('input_boolean.down', state='off')
        self.set_state('input_boolean.right', state='off')
        self.set_state('input_boolean.left', state='off')
        self.set_state('input_boolean.stop', state='off')
        self.set_state('input_boolean.zoom_out', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        if new == "on":

            self.log("ZOOMIN")

            camlist = self.get_state("input_select.camera_list", attribute="state")

            x = int(float(camlist))

            self.send(self.cams[x], self.coms["zoom+"])

            self.log("send ZOOMIN")

            self.set_state('input_boolean.zoom_in', state='off')

    def zoomout(self, entity, attribute, old, new, kwargs):

        self.set_state('input_boolean.up', state='off')
        self.set_state('input_boolean.down', state='off')
        self.set_state('input_boolean.right', state='off')
        self.set_state('input_boolean.left', state='off')
        self.set_state('input_boolean.stop', state='off')
        self.set_state('input_boolean.zoom_in', state='off')
        self.set_state('input_boolean.set_preset', state='off')

        if new == "on":

            self.log("ZOOMOUT")

            camlist = self.get_state("input_select.camera_list", attribute="state")

            x = int(float(camlist))

            self.send(self.cams[x], self.coms["zoom-"])

            self.log("send ZOOMOUT")

            self.set_state('input_boolean.zoom_out', state='off')

    def setpreset(self, entity, attribute, old, new, kwargs):

        if new == "on":

            self.log("Set preset...")

            camlist = self.get_state("input_select.camera_list", attribute="state")
            preset = self.get_state("input_select.preset_list", attribute="state")

            x = int(float(camlist))
            y = str(int(float(preset)))

            if y in self.coms.keys():

                self.send(self.cams[x], self.coms[y])

            self.set_state('input_boolean.set_preset', state='off')

            self.log("Set preset")

    def gotopreset(self, entity, attribute, old, new, kwargs):


        self.log("Go to preset...")

        cam = self.get_state("input_select.camera_list", attribute="state")
        dist = new

        x = int(float(cam))
        y = str(int(float(dist)))

        if y in self.coms.keys():

            self.send(self.cams[x], self.coms[y])

            self.log("Success")

    def on(self, entity, attribute, old, new, kwargs):

        try:
            self.send(self.cams[1], self.coms["on"])
        except:
            pass
        try:
            self.send(self.cams[2], self.coms["on"])
        except:
            pass
        try:
            self.send(self.cams[3], self.coms["on"])
        except:
            pass

        self.log("Success")

    def off(self, entity, attribute, old, new, kwargs):

        try:
            self.send(self.cams[1], self.coms["off"])
        except:
            pass
        try:
            self.send(self.cams[2], self.coms["off"])
        except:
            pass
        try:
            self.send(self.cams[3], self.coms["off"])
        except:
            pass

        self.log("Success")