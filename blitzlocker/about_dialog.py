from blitzlocker import Gtk

class AboutBlitzLocker(Gtk.AboutDialog):
    def __init__(self):
        self.program_name = "BlitzLocker"
        self.version = "0.0.1"
        self.comments = "A password manager for SalesForce"
        self.authors = ["Jack Rosenthal", "Charlie McConnell", "Jacob Thompson"]

about = Gtk.Dialog(AboutBlitzLocker())

def show_about_dialog(item):
    about.run()
