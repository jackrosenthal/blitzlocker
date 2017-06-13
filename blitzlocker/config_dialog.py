from blitzlocker.db import db, Site, AppConfigItem
from blitzlocker import Gtk, Gdk
from blitzlocker import browserutil
import re

valid_url_p = re.compile(r'^https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')

class ConfigDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Configure BlitzLocker")
        self.set_default_size(640, 480)
        self.set_resizable(False)
        self.set_deletable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.vbox = Gtk.Box()
        self.vbox.set_orientation(Gtk.Orientation.VERTICAL)
        self.vbox.set_spacing(6)
        self.add(self.vbox)

        self.notebook = Gtk.Notebook()
        self.vbox.add(self.notebook)

        self.actions = Gtk.ButtonBox()
        self.actions.set_layout(Gtk.ButtonBoxStyle(4))
        self.actions.set_spacing(6)
        self.actions.add(Gtk.Box())
        self.ok_button = Gtk.Button(label="OK")
        self.ok_button.connect("clicked", self.ok_clicked)
        self.actions.add(self.ok_button)
        self.vbox.add(self.actions)
        self.vbox.add(Gtk.Box())

        self.notebook.append_page(SitesPage(window=self), Gtk.Label('Sites'))
        self.notebook.append_page(BrowserPage(window=self), Gtk.Label('Web Browser'))

        self.notebook.show_all()

    def ok_clicked(self, *args, **kwargs):
        self.hide()

class SitesPage(Gtk.Box):
    def __init__(self, window):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        self.set_spacing(6)

        self.window = window

        self.bbox = Gtk.ButtonBox()
        self.add_site_button = Gtk.Button(label='Add Site...')
        self.rm_site_button = Gtk.Button(label='Remove Site', sensitive=False)
        self.bbox.add(self.add_site_button)
        self.bbox.add(self.rm_site_button)

        self.add_site_button.connect("clicked", self.open_add_site)
        self.rm_site_button.connect("clicked", self.rm_site)

        self.add(self.bbox)

        self.liststore = Gtk.ListStore(str)
        for site in db.query(Site).all():
            self.liststore.append([site.base_url])

        self.column = Gtk.TreeViewColumn("Base URL")
        base_url_cr = Gtk.CellRendererText()
        self.column.pack_start(base_url_cr, True)
        self.column.add_attribute(base_url_cr, "text", 0)

        self.treeview = Gtk.TreeView(self.liststore)
        self.treeview.append_column(self.column)
        self.select = self.treeview.get_selection()
        self.select.connect("changed", self.selection_changed)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True)
        self.scroll.add(self.treeview)

        self.add(self.scroll)
        self.show_all()

    def open_add_site(self, widget):
        asd = AddSiteDialog(liststore=self.liststore, transient_for=self.window, modal=True)
        asd.present()

    def rm_site(self, widget):
        url = self.liststore[self.selected_treeiter][0]
        del self.liststore[self.selected_treeiter]
        db.commit()
        db.query(Site).filter(Site.base_url == url).delete(synchronize_session=False)
        db.commit()

    def selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter:
            self.rm_site_button.set_sensitive(True)
            self.selected_treeiter = treeiter
        else:
            self.rm_site_button.set_sensitive(False)

class BrowserPage(Gtk.Box):
    def __init__(self, window):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.set_homogeneous(False)
        self.set_spacing(6)

        self.window = window

        private = db.query(AppConfigItem)\
                .filter(AppConfigItem.key == 'browser.private')\
                .one_or_none()
        if private:
            private = private.value

        choice = db.query(AppConfigItem)\
                .filter(AppConfigItem.key == 'browser.choice')\
                .one_or_none()
        if choice:
            choice = choice.value

        self.hbox = Gtk.Box(spacing=6)
        self.hbox.add(Gtk.Label("Default Browser"))

        self.browser_store = Gtk.ListStore(str)
        active_choice = None
        for b in browserutil.system_browsers:
            treeiter = self.browser_store.append([b])
            if b == choice:
                active_choice = treeiter

        self.check_private = Gtk.CheckButton("Use Private Browser Window")
        self.check_private.set_active(bool(private))
        self.check_private.connect("toggled", self.private_checkbox_toggled)

        self.browser_combo = Gtk.ComboBox.new_with_model(self.browser_store)
        renderer_text = Gtk.CellRendererText()
        self.browser_combo.pack_start(renderer_text, True)
        self.browser_combo.add_attribute(renderer_text, "text", 0)
        self.browser_combo.connect("changed", self.browser_combo_changed)
        if active_choice:
            self.browser_combo.set_active_iter(active_choice)
        self.hbox.add(self.browser_combo)

        self.add(self.hbox)
        self.add(self.check_private)

    def private_checkbox_toggled(self, widget):
        value = self.check_private.get_active()

        # clear any existing value in the db
        db.commit()
        db.query(AppConfigItem)\
            .filter(AppConfigItem.key == 'browser.private')\
            .delete(synchronize_session=False)
        db.commit()
        db.add(AppConfigItem(key='browser.private', value=value))
        db.commit()

    def browser_combo_changed(self, widget):
        tree_iter = self.browser_combo.get_active_iter()
        if tree_iter != None:
            model = self.browser_combo.get_model()
            name = model[tree_iter][0]
            if 'private' in browserutil.browsers[name].keys():
                self.check_private.set_sensitive(True)
            else:
                self.check_private.set_active(False)
                self.private_checkbox_toggled(None)
                self.check_private.set_sensitive(False)

            # clear any existing value in the db
            db.commit()
            db.query(AppConfigItem)\
                .filter(AppConfigItem.key == 'browser.choice')\
                .delete(synchronize_session=False)
            db.commit()
            db.add(AppConfigItem(key='browser.choice', value=name))
            db.commit()

class AddSiteDialog(Gtk.Dialog):
    def __init__(self, liststore, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, title="Add Site", **kwargs)
        self.liststore = liststore
        self.set_default_size(250, 100)

        self.base_textbox = Gtk.Entry()
        self.base_textbox.set_placeholder_text("https://foo.bar.baz.salesforce.com")
        self.base_textbox.set_activates_default(True)
        base_url_box = Gtk.Box(spacing=6)
        base_url_box.add(Gtk.Label("Base URL"))
        base_url_box.add(self.base_textbox)
        self.get_content_area().add(base_url_box)

        self.add_button("Cancel", 0)
        asb = self.add_button("Add Site", 1)
        asb.set_can_default(True)
        asb.grab_default()

        self.connect("response", self.response)
        self.show_all()

    def response(self, widget, response_id):
        if response_id == 0:
            self.destroy()
        elif response_id == 1:
            text = self.base_textbox.get_text()
            if not valid_url_p.match(text):
                msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, "You must enter a valid URL")
                msg.run()
                msg.destroy()
                return
            if text.endswith('/'):
                text = text[:-1]
            db.add(Site(base_url=text))
            db.commit()
            self.liststore.append([text])
            self.destroy()

config_dialog = ConfigDialog()
