# Application wrapper for Mac OS X
# (as an alternative to the systray icon typically used)
from blitzlocker import Gtk, Gio
from blitzlocker.blitzmenu import default_menu_items
from functools import wraps

class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="com.salesforce.blitzlocker",
            flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        menu = Gio.Menu()
        for label, func in default_menu_items:
            act = Gio.SimpleAction.new('a' + str(hash(label)), None)
            act.connect("activate", menu_wrapper_func(func))
            self.add_action(act)
            menu.append(label, "app.a" + str(hash(label)))
        self.set_app_menu(menu)

    def do_activate(self):
        Gtk.main()

def menu_wrapper_func(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        f(None)
    return wrapper

