from blitzlocker import Gtk

def show_about_dialog(item):
    about = Gtk.AboutDialog()
    about.set_transient_for(None)
    about.set_program_name('BlitzLocker')
    about.set_version('0.1.0')
    about.set_comments("A password manager for SalesForce")
    about.set_authors(["Jack Rosenthal", "Charlie McConnell", "Jacob Thompson"])
    about.run()
    about.destroy()
