from blitzlocker.db import db, Site, AppConfigItem
from blitzlocker import Gtk, Gdk

class ConfigDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Configure BlitzLocker")
        self.resizable = False
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.notebook.append_page(SitesPage(), Gtk.Label('Sites'))
        self.notebook.append_page(BrowserPage(), Gtk.Label('Web Browser'))

        self.notebook.show_all()

class SitesPage(Gtk.ListBox):
    def __init__(self):
        Gtk.Box.__init__(self)

        self.bbox = Gtk.ButtonBox()
        self.add_site_button = Gtk.Button(label='Add Site...')
        self.rm_site_button = Gtk.Button(label='Remove Site', sensitive=False)
        self.bbox.add(self.add_site_button)
        self.bbox.add(self.rm_site_button)

        self.add(self.bbox)

        self.liststore = Gtk.ListStore(str)
        for site in db.query(Site).all():
            self.liststore.append([site.base_url])

        self.treeview = Gtk.TreeView(self.liststore)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True)
        self.scroll.add(self.treeview)

        self.add(self.scroll)

class BrowserPage(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_border_width(10)
        self.add(Gtk.Label("Web Browser Configuration!"))

config_dialog = ConfigDialog()
