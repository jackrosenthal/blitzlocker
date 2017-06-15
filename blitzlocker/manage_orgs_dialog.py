from blitzlocker.db import db, Site, Org, AppConfigItem
from blitzlocker import Gtk, Gdk
import random

class ManageOrgsDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Manage Orgs")
        Gtk.Box.__init__(self)
        self.set_default_size(-1,320)
        self.set_resizable(False)
        self.set_deletable(False)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.combo = None
        self.site = None

        self.grid = Gtk.Grid()

        self.liststore = Gtk.ListStore(str)
        for site in db.query(Site).all():
            self.liststore.append([site.base_url])

        self.site_combo_box = Gtk.ComboBox.new_with_model(self.liststore)
        site_url_cr = Gtk.CellRendererText()
        self.site_combo_box.pack_start(site_url_cr,True)
        self.site_combo_box.add_attribute(site_url_cr,"text",0)
        self.site_combo_box.connect('changed', self.on_site_changed)

        self.grid.add(self.site_combo_box)

        self.bbox = Gtk.ButtonBox()
        self.add_org_button = Gtk.Button(label='Add Org...')
        self.rm_org_button = Gtk.Button(label='Remove Org', sensitive=False)
        self.bbox.add(self.add_org_button)
        self.bbox.add(self.rm_org_button)

        self.add_org_button.connect("clicked", self.open_add_org)
        self.rm_org_button.connect("clicked",self.rm_org)

        self.grid.attach_next_to(self.bbox,self.site_combo_box,
                Gtk.PositionType.BOTTOM,
                1,
                2
                )

        #Treeveiw display
        self.org_list = Gtk.ListStore(str, str, str)
        self.org_scroll = Gtk.ScrolledWindow()
        user_column = Gtk.TreeViewColumn('Username')
        pass_column = Gtk.TreeViewColumn('Password')
        desc_column = Gtk.TreeViewColumn('Description')
        self.org_tree = Gtk.TreeView(self.org_list)
        self.org_tree_cr = Gtk.CellRendererText()
        if db.query(Org).all() and self.site:
            for org in db.query(Site).filter(Site.base_url==self.site).one().orgs:
                self.org_list.append((org.username, org.password, org. description))
        user_column.pack_start(self.org_tree_cr, True)
        pass_column.pack_start(self.org_tree_cr, True)
        desc_column.pack_start(self.org_tree_cr, True)
        user_column.add_attribute(self.org_tree_cr, 'text', 0)
        pass_column.add_attribute(self.org_tree_cr, 'text', 1)
        desc_column.add_attribute(self.org_tree_cr, 'text', 2)
        self.org_tree.append_column(user_column)
        self.org_tree.append_column(pass_column)
        self.org_tree.append_column(desc_column)
        self.org_tree.get_selection().connect('changed', self.edit_description)
        self.org_scroll.set_vexpand(True)
        self.org_scroll.add(self.org_tree)
        self.grid.attach_next_to(self.org_scroll,
                self.bbox,
                Gtk.PositionType.BOTTOM,
                1,
                1,
                )

        #The button box!
        self.button_box = Gtk.ButtonBox()

        #Close Button
        self.close_button = Gtk.Button.new_with_label('Close')
        self.close_button.connect('clicked', self.click_close)
        self.button_box.add(self.close_button)

        #Edit Button
        self.edit_button = Gtk.Button.new_with_label('Edit Desc.')
        self.edit_button.connect('clicked', self.click_edit)
        self.button_box.add(self.edit_button)

        self.grid.attach_next_to(self.button_box,
                self.org_scroll,
                Gtk.PositionType.BOTTOM,
                1,
                1,
                )

        self.add(self.grid)

    def refresh_tree(self):
        self.org_list.clear()
        if db.query(Org).all() and self.site:
            for org in db.query(Site).filter(Site.base_url==self.site).one().orgs:
                self.org_list.append((org.username, org.password, org.description))
        self.org_tree.set_model(self.org_list)

    def click_close(self, button):
        self.hide()

    def click_edit(self, button):
        if self.combo:
            add = AddDescriptionDialog(self.combo)
            add.present()
    def edit_description(self, combo):
        self.combo = combo
        self.rm_org_button.set_sensitive(True)

    def rm_org(self,widget):
        tree,pathlist = self.org_tree.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = tree.get_iter(path)
            self.id = tree.get_value(tree_iter, 0)
            description = tree.get_value(tree_iter, 2)
        db.query(Org).filter(Org.username==self.id,Org.description==description)\
                .delete(synchronize_session=False)
        db.commit()
        self.refresh_tree()

    def on_site_changed(self, combo):
        self.site = combo.get_model()[combo.get_active()][0]
        self.refresh_tree()

    def open_add_org(self, widget):
        self.active_combo = self.site_combo_box.get_active_iter()
        aod = AddOrgDialog(liststore=self.liststore,
                active_combo = self.active_combo,
                transient_for=self,
                modal=True
                )
        aod.present()
        self.refresh_tree()

class AddDescriptionDialog(Gtk.Dialog):
    def __init__(self, combo):
        Gtk.Dialog.__init__(self, title="Edit Description")
        self.set_default_size(250, 100)
        self.set_resizable(False)
        self.set_deletable(False)
        self.description_label = Gtk.Label('Description: ')
        self.description_textbox = Gtk.Entry()
        self.grid = Gtk.Grid()

        description = 'Description'
        tree, pathlist = combo.get_selected_rows()
        for path in pathlist:
            tree_iter = tree.get_iter(path)
            self.id = tree.get_value(tree_iter, 0)
            description = tree.get_value(tree_iter, 2)

        #description field
        self.description_textbox.set_text(description)
        self.description_textbox.set_activates_default(True)
        self.grid.add(self.description_label)
        self.grid.attach_next_to(self.description_textbox,
                self.description_label,
                Gtk.PositionType.RIGHT,
                1,
                1,
                )

        #cancel button
        self.cancel = Gtk.Button.new_with_label('Cancel')
        self.cancel.connect('clicked', self.click_cancel)
        self.grid.attach_next_to(self.cancel,
                self.description_label,
                Gtk.PositionType.BOTTOM,
                1,
                1,
                )

        #Accept button
        self.accept = Gtk.Button.new_with_label('Accept')
        self.accept.connect('clicked', self.click_accept)
        self.grid.attach_next_to(self.accept,
                self.cancel,
                Gtk.PositionType.RIGHT,
                1,
                1,
                )

        self.get_content_area().add(self.grid)
        self.show_all()

    def click_cancel(self, button):
        self.destroy()

    def click_accept(self, button):
        if self.description_textbox.get_text():
            db.query(Org).filter(Org.username==self.id).first()\
                    .description = self.description_textbox.get_text()
            db.commit()
            self.destroy()


class AddOrgDialog(Gtk.Dialog):
    def __init__(self, liststore,active_combo, *args, **kwargs):
        self.site_url = None
        self.set_resizable(False)
        self.set_deletable(False)
        Gtk.Dialog.__init__(self, *args, title="Add Org", **kwargs)
        self.liststore = liststore
        self.set_default_size(250, 100)

        self.grid = Gtk.Grid()

        self.site_label = Gtk.Label("Site: ")
        self.treeview=Gtk.TreeView(self.liststore)
        self.site_combo_box = Gtk.ComboBox.new_with_model(self.liststore)
        site_url_cr = Gtk.CellRendererText()
        self.site_combo_box.pack_start(site_url_cr,True)
        self.site_combo_box.add_attribute(site_url_cr,"text",0)
        self.site_combo_box.set_active_iter(active_combo)
        self.site_combo_box.connect("changed", self.on_site_combo_changed)

        self.grid.attach(self.site_label,0,0,1,1)
        self.grid.attach_next_to(self.site_combo_box,self.site_label,Gtk.PositionType.RIGHT,2,1)

        self.user_textbox = Gtk.Entry()
        self.user_textbox.set_placeholder_text("Username ")
        self.user_textbox.set_activates_default(True)
        self.user_label = Gtk.Label("Username: ")

        self.grid.attach_next_to(self.user_label,self.site_label,Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.user_textbox,self.user_label,Gtk.PositionType.RIGHT,2,1)

        self.pw_textbox = Gtk.Entry()
        self.pw_textbox.set_placeholder_text("********")
        self.pw_label = Gtk.Label("Password: ")
        self.gen_pw_button = Gtk.Button(label = 'Generate')
        self.gen_pw_button.connect('clicked', self.on_generate_clicked)

        self.grid.attach_next_to(self.pw_label,self.user_label,Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.pw_textbox,self.pw_label,Gtk.PositionType.RIGHT,1,1)
        self.grid.attach_next_to(self.gen_pw_button,self.pw_textbox,Gtk.PositionType.RIGHT,1,1)

        self.desc_textbox = Gtk.Entry()
        self.desc_label = Gtk.Label("Description: ")

        self.grid.attach_next_to(self.desc_label,self.pw_label,Gtk.PositionType.BOTTOM,1,1)
        self.grid.attach_next_to(self.desc_textbox,self.desc_label,Gtk.PositionType.RIGHT,2,1)


        self.add_button("Cancel", 0)
        aob = self.add_button("Add Org", 1)
        aob.set_can_default(True)
        aob.grab_default()

        self.connect("response", self.response)
        self.get_content_area().add(self.grid)
        self.show_all()

    def on_generate_clicked(self, button):
        length = 15
        chars = (list(range(97, 123)) +
            list(range(65, 91)) +
            list(range(48, 57))
            )
        pw = chr(chars[random.randint(0, len(chars)-11)])
        while len(pw) < length:
            pw += chr(chars[random.randint(0, len(chars)-1)])
        self.pw_textbox.set_text(pw)

    def on_site_combo_changed(self, combo):
        self.site_url = combo.get_model()[combo.get_active()][0]

    def response(self, widget, response_id):
        if response_id == 0:
            self.destroy()
        elif (response_id == 1 and
            self.site_url and
            self.user_textbox.get_text()
            ):
            if not self.pw_textbox.get_text():
                self.on_generate_clicked(None)
            user = self.user_textbox.get_text()
            pw = self.pw_textbox.get_text()
            desc = self.desc_textbox.get_text()
            site = self.site_url
            self.site_id, = db.query(Site.id).filter(Site.base_url==site).one()
            db.add(Org(username = user,password = pw, description = desc, site_id = self.site_id))
            db.commit()
            self.destroy()

manage_orgs_dialog = ManageOrgsDialog()
