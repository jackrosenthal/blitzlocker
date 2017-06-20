# Enable the Adwaita theme at runtime
# Needed for Ubuntu 14.04, which has a default theme incompat. with GTK+ 3.22
import os
os.environ['GTK_THEME'] = 'Adwaita'
