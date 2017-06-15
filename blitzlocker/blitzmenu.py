from blitzlocker import Gtk
from blitzlocker.about_dialog import show_about_dialog
from blitzlocker.manage_orgs_dialog import manage_orgs_dialog
from blitzlocker.config_dialog import config_dialog
from blitzlocker.login_dialog import login_dialog

def show_all_func(window):
    return lambda widget: window.show_all()

default_menu_items = (
    ("About", show_about_dialog),
    ("Exit BlitzLocker", Gtk.main_quit),
    ("Configuration", show_all_func(config_dialog)),
    ("Manage Orgs", show_all_func(manage_orgs_dialog)),
#    ("Login using CL#...", Gtk.main_quit),
    ("Login...", show_all_func(login_dialog)),
)

class BlitzMenu(Gtk.Menu):
    def __init__(self, items):
        Gtk.Menu.__init__(self)
        for label, act in items:
            itm = Gtk.MenuItem()
            itm.set_label(label)
            itm.connect("activate", act)
            self.append(itm)

default_menu = BlitzMenu(default_menu_items)
