from blitzlocker import Gtk, Gdk

class ManageOrgsDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Manage Orgs")
        self.resizable = False
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

manage_orgs_dialog = ManageOrgsDialog()
