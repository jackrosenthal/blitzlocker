from blitzlocker.db import Site, Org, db
from blitzlocker import Gtk, Gdk

ROWS = 1
COLS = 3

class LoginDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Login")
        self.set_resizable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_border_width(15)
        box = Gtk.Grid()
        self.add(box)

        #The Org list
        org_list = Gtk.ListStore(str, str)
        for org in db.query(Org).all():
            org_list.append((org.username, org.password))
        org_list.append(('DEFAULT','PW'))
        org_combo = Gtk.ComboBox.new_with_model(org_list)
        org_combo.connect('changed', self.on_org_changed)
        org_combo_cr = Gtk.CellRendererText()
        org_combo.pack_start(org_combo_cr, True)
        org_combo.add_attribute(org_combo_cr, 'text', 0)
        org_combo.set_wrap_width(COLS)
        box.add(org_combo)

        #The Site list
        site_list = Gtk.ListStore(str)
        for site in db.query(Site).all():
            site_list.append((site.base_url),)
        site_list.append(('Site',))
        site_combo = Gtk.ComboBox.new_with_model(site_list)
        site_combo.connect('changed', self.on_site_changed)
        site_combo_cr = Gtk.CellRendererText()
        site_combo.pack_start(site_combo_cr, True)
        site_combo.add_attribute(site_combo_cr, 'text', 0)
        site_combo.set_wrap_width(COLS)
        box.attach_next_to(site_combo,
                org_combo,
                Gtk.PositionType.RIGHT,
                1,
                1,
                )

        #The Cancel Button
        self.cancel_button = Gtk.Button.new_with_label('Cancel')
        self.cancel_button.connect('clicked', self.click_cancel)
        box.attach_next_to(self.cancel_button,
                org_combo,
                Gtk.PositionType.BOTTOM,
                1,
                1,
                )

        #The Login button
        self.login_button = Gtk.Button.new_with_label('Login')
        self.login_button.connect('clicked', self.click_login)
        box.attach_next_to(self.login_button,
                site_combo,
                Gtk.PositionType.BOTTOM,
                1,
                1,
                )

    def on_org_changed(self, combo):
            print('List Changed')

    def on_site_changed(self, combo):
        print('Site Changed')

    def click_cancel(self, button):
        self.hide()

    def click_login(self, button):
        print('login clicked')

login_dialog = LoginDialog()
