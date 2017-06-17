import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

if getattr(sys, 'frozen', False):
    basepath = sys._MEIPASS
else:
    basepath = '.'
