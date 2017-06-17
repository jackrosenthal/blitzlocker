from blitzlocker import Gtk, GdkPixbuf, basepath
from gi.repository import GLib

with open(basepath + "/res/raw_logo", "rb") as f:
    logo = GdkPixbuf.Pixbuf.new_from_bytes(
            GLib.Bytes(f.read()),
            GdkPixbuf.Colorspace(0),
            True, 8, 90, 128, 360)

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
