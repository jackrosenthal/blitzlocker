from blitzlocker.db import Site, Org, db
from blitzlocker import Gtk, Gdk

class LoginDialog(Gtk.Window):
    def __init__(self):
        __site = None
        __org = None
        __ROWS = 1
        __COLS = 4

        Gtk.Window.__init__(self, title="Login")
        self.set_resizable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_border_width(15)
        self.set_deletable(False)
        box = Gtk.Grid()
        self.add(box)

        #The Site list
        site_list = Gtk.ListStore(str)
        for site in db.query(Site).all():
            site_list.append((site.base_url,))
        site_list.append(('Default Site',))
        site_combo = Gtk.ComboBox.new_with_model(site_list)
        site_combo.connect('changed', self.on_site_changed)
        site_combo_cr = Gtk.CellRendererText()
        site_combo.pack_start(site_combo_cr, True)
        site_combo.add_attribute(site_combo_cr, 'text', 0)
        site_combo.set_wrap_width(__COLS)
        box.attach(site_combo, 0, 0, __COLS, __ROWS)

        #The Org Tree
        org_list = Gtk.ListStore(str, str)
        for org in db.query(Org).all():
            if(org.site == __site):
                self.org_list.append((org.username, org.password))
        org_list.append(('DEFAULT','PW'))
        org_list.append(('DEFAULT2','PWw'))
        logins_name = Gtk.TreeViewColumn("Logins")
        org_tree = Gtk.TreeView(org_list)
        org_tree_cr = Gtk.CellRendererText()
        logins_name.pack_start(org_tree_cr, True)
        logins_name.add_attribute(org_tree_cr, 'text', 0)
        org_tree.append_column(logins_name)
        org_tree.get_selection().connect('changed', self.on_org_changed)
        org_scroll = Gtk.ScrolledWindow()
        org_scroll.set_vexpand(True)
        org_scroll.add(org_tree)
        box.attach_next_to(org_scroll,
                site_combo,
                Gtk.PositionType.BOTTOM,
                2*__ROWS,
                2*__ROWS,
                )

        #The Cancel Button
        self.cancel_button = Gtk.Button.new_with_label('Cancel')
        self.cancel_button.connect('clicked', self.click_cancel)
        box.attach_next_to(self.cancel_button,
                org_scroll,
                Gtk.PositionType.BOTTOM,
                __ROWS,
                __ROWS,
                )

        #The Login button
        self.login_button = Gtk.Button.new_with_label('Login')
        self.login_button.connect('clicked', self.click_login)
        box.attach_next_to(self.login_button,
                self.cancel_button,
                Gtk.PositionType.RIGHT,
                __ROWS,
                __ROWS,
                )

    def on_org_changed(self, combo):
            __org = combo

    def on_site_changed(self, combo):
        __site = combo[0]

    def click_cancel(self, button):
        self.hide()

    def click_login(self, button):
        print('login clicked')

login_dialog = LoginDialog()
