from blitzlocker import Gtk

class TrayIcon(Gtk.StatusIcon):
    def __init__(self, menu):
        Gtk.StatusIcon.__init__(self)
        self.menu = menu

        self.set_from_icon_name("applications-internet")
        self.set_tooltip_text("BlitzLocker")
        self.connect("button-press-event", self.click_event)

    def click_event(self, *args):
        self.menu.show_all()
        self.menu.popup_at_pointer(None)
