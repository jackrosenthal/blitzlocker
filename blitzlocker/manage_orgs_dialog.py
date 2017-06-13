from blitzlocker.db import db, Site, AppConfigItem
from blitzlocker import Gtk, Gdk

class ManageOrgsDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Manage Orgs")    
        Gtk.Box.__init__(self)
        self.set_default_size(230,320)
        self.resizable = False
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        
        self.grid = Gtk.Grid()

        self.liststore = Gtk.ListStore(str)
        for site in db.query(Site).all():
            self.liststore.append([site.base_url])
        
        self.treeview=Gtk.TreeView(self.liststore)
        self.site_combo_box = Gtk.ComboBox.new_with_model(self.liststore)
        site_url_cr = Gtk.CellRendererText()
        self.site_combo_box.pack_start(site_url_cr,True)
        self.site_combo_box.add_attribute(site_url_cr,"text",0)
        self.grid.add(self.site_combo_box)
       
        
        self.bbox = Gtk.ButtonBox()
        self.add_org_button = Gtk.Button(label='Add Org...')
        self.rm_org_button = Gtk.Button(label='Remove Org', sensitive=False)
        self.bbox.add(self.add_org_button)
        self.bbox.add(self.rm_org_button)
        
        self.add_org_button.connect("clicked", self.open_add_org)

        self.grid.attach_next_to(self.bbox,self.site_combo_box,Gtk.PositionType.BOTTOM,1,2)
        self.add(self.grid)

    def open_add_org(self, widget):
        asd = AddSiteDialog(liststore=self.liststore, transient_for=self, modal=True)
        asd.present()


class AddSiteDialog(Gtk.Dialog):
    def __init__(self, liststore, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, title="Add Org", **kwargs)
        self.liststore = liststore
        self.set_default_size(250, 100)

        self.grid = Gtk.Grid()

        self.user_textbox = Gtk.Entry()
        self.user_textbox.set_placeholder_text("Username ")
        self.user_textbox.set_activates_default(True)
        self.user_label = (Gtk.Label("Username"))

        self.grid.attach(self.user_label,0,0,1,1)
        self.grid.attach_next_to(self.user_textbox,self.user_label,Gtk.PositionType.RIGHT,2,1)

        self.pw_textbox = Gtk.Entry()
        self.pw_textbox.set_placeholder_text("********")
        self.pw_label = Gtk.Label("Password ")
        self.gen_pw_button = Gtk.Button(label = 'Generate')
        
        self.grid.attach_next_to(self.pw_label,self.user_label,Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.pw_textbox,self.pw_label,Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.gen_pw_button,self.pw_textbox,Gtk.PositionType.RIGHT,1,1)

        self.desc_textbox = Gtk.Entry()
        self.desc_label = Gtk.Label("Description")
        
        self.grid.attach_next_to(self.desc_label,self.pw_label,Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.desc_textbox,self.desc_label,Gtk.PositionType.RIGHT,2,1)

        self.add_button("Cancel", 0)
        asb = self.add_button("Add Org", 1)
        asb.set_can_default(True)
        asb.grab_default()

        self.connect("response", self.response)
        self.get_content_area().add(self.grid)
        self.show_all()


    def response(self, widget, response_id):
        if response_id == 0:
            self.destroy()
        elif response_id == 1:
            self.destroy()


manage_orgs_dialog = ManageOrgsDialog()
