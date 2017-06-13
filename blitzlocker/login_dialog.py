from blitzlocker.db import Site, Org, db
from blitzlocker import gtk, gdk

class LoginDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Login")
        self.set_default_size(640, 480)
        self.set_resizable(False)
        self.set_type_hint()
