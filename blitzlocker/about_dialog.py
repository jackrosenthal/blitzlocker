from blitzlocker import Gtk, GdkPixbuf

logo = GdkPixbuf.Pixbuf.new_from_file_at_scale("res/blitz.png", 128, 128, True)

def show_about_dialog(item):
    about = Gtk.AboutDialog()
    about.set_transient_for(None)
    about.set_program_name('BlitzLocker')
    about.set_version('Version 1.0.0 (Golden Master Release)')
    about.set_comments("A password manager for SalesForce")
    about.set_authors(["Jack Rosenthal", "Charlie McConnell", "Jacob Thompson"])
    about.set_logo(logo)
    about.run()
    about.destroy()
