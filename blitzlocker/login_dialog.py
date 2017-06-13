from blitzlocker.db import Site, Org, db
from blitzlocker import Gtk, Gdk
from blitzlocker.browserutil import open_configured_browser

class LoginDialog(Gtk.Window):
    def __init__(self):
        self.site = None
        self.org = None
        self.ROWS = 1
        self.COLS = 5

        Gtk.Window.__init__(self, title="Login")
        self.set_resizable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_border_width(15)
        self.set_deletable(False)
        self.set_default_size(-1, 320)
        self.box = Gtk.Grid()
        self.add(self.box)

        #The Site list
        self.site_list = Gtk.ListStore(str)
        for self.site in db.query(Site).all():
            self.site_list.append((self.site.base_url,))
        self.site_combo = Gtk.ComboBox.new_with_model(self.site_list)
        self.site_combo.connect('changed', self.on_site_changed)
        self.site_combo_cr = Gtk.CellRendererText()
        self.site_combo.pack_start(self.site_combo_cr, True)
        self.site_combo.add_attribute(self.site_combo_cr, 'text', 0)
        self.box.attach(self.site_combo, 0, 0, self.COLS, self.ROWS)

        #The Org Tree
        self.org_list = Gtk.ListStore(str, str)
        self.org_scroll = Gtk.ScrolledWindow()
        logins_name = Gtk.TreeViewColumn("Logins")
        self.org_tree = Gtk.TreeView(self.org_list)
        self.org_tree_cr = Gtk.CellRendererText()
        for org in self.site.orgs:
            self.org_list.append([org.username, org.password])
        logins_name.pack_start(self.org_tree_cr, True)
        logins_name.add_attribute(self.org_tree_cr, 'text', 0)
        self.org_tree.append_column(logins_name)
        self.org_tree.get_selection().connect('changed', self.on_org_changed)
        self.org_scroll.set_vexpand(True)
        self.org_scroll.set_min_content_height(self.COLS)
        self.org_scroll.set_max_content_height(self.COLS)
        self.org_scroll.add(self.org_tree)
        self.box.attach_next_to(self.org_scroll,
                self.site_combo,
                Gtk.PositionType.BOTTOM,
                2*self.ROWS,
                self.COLS,
                )

        #The Cancel Button
        self.cancel_button = Gtk.Button.new_with_label('Cancel')
        self.cancel_button.connect('clicked', self.click_cancel)
        self.box.attach_next_to(self.cancel_button,
                self.org_scroll,
                Gtk.PositionType.BOTTOM,
                self.ROWS,
                self.ROWS,
                )

        #The Login button
        self.login_button = Gtk.Button.new_with_label('Login')
        self.login_button.connect('clicked', self.click_login)
        self.box.attach_next_to(self.login_button,
                self.cancel_button,
                Gtk.PositionType.RIGHT,
                self.ROWS,
                self.ROWS,
                )

    def on_org_changed(self, combo):
        tree, pathlist = combo.get_selected_rows()
        for path in pathlist:
            tree_iter = tree.get_iter(path)
            self.org = (tree.get_value(tree_iter, 0),
                    tree.get_value(tree_iter, 1)
                    )

    def repopulate_org(self):
        self.org_list.clear()
        for org in db.query(Site).filter(Site.base_url==self.site).one().orgs:
            self.org_list.append([org.username, org.password])
        self.org_tree.set_model(self.org_list)

    def on_site_changed(self, combo):
        self.site = combo.get_model()[combo.get_active()][0]
        self.repopulate_org()

    def click_cancel(self, button):
        self.hide()

    def click_login(self, button):
        open_configured_browser(self.site + 
                '?un=' +
                self.org[0] +
                '&pw=' + 
                self.org[1]
                )
        print('login clicked')

login_dialog = LoginDialog()
