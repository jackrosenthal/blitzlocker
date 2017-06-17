from blitzlocker import Gtk, basepath

class TrayIcon(Gtk.StatusIcon):
    def __init__(self, menu):
        Gtk.StatusIcon.__init__(self)
        self.menu = menu

        self.set_from_file(basepath + "/res/icon64.png")
        self.set_tooltip_text("BlitzLocker")
        self.connect("button-press-event", self.click_event)

    def click_event(self, *args):
        self.menu.show_all()
        self.menu.popup_at_pointer(None)
