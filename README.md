# BlitzLocker

BlitzLocker is an application for Salesforce developers and project owners to
quickly access their development site logins.

## Installation Instructions

To install BlitzLocker, you will need a machine running Linux or Mac OS X.

### Mac OS X

If you are running an Intel Macintosh with Mac OS X 10.9 or above, we have
already packaged a [`.dmg` file for you with an application ready to
go](http://inside.mines.edu/~jrosenth/blitzlocker/BlitzLocker.dmg). Just drag
the application to your `Applications` folder.

If you are running an earlier verision than 10.9 or a PowerPC Macintosh,
BlitzLocker should still be compatible, you will have to just build the `.app`
folder yourself (described below).

### Linux

You will need:

 * Python 2.7 or greater (Python 3.6 is reccomended)
 * PyGObject3 ([installation instructions](https://pygobject.readthedocs.io/en/latest/getting_started.html))
 * SQLAlchemy (`pip3 install sqlalchemy`)

After you have those dependencies installed, clone the repo and type
`./lockerapp`. If you are using Unity, see [this SO
post](https://askubuntu.com/questions/30742/how-do-i-access-and-enable-more-icons-to-be-in-the-system-tray)
on how to get BlitzLocker in the system tray whitelist. If you want BlitzLocker
to run at login, add it to your `.xprofile` or `.xinitrc`, like so:

    #!/bin/bash
    # ... some stuff
    ~/blitzlocker/lockerapp &
    # ... some more stuff

## Advanced Stuff: Building the Mac OS X `.app` folder and `.dmg` file

You will need:

 * Homebrew
 * **Python 3.5.2**, installed via Homebrew (as of this time of writing, Python
   3.6 has an obsure bug with PyInstaller and the libraries in BlitzLocker)
 * PyGObject3 ([installation instructions](https://pygobject.readthedocs.io/en/latest/getting_started.html))
 * SQLAlchemy (`pip3 install sqlalchemy`)
 * PyInstaller (`pip3 install pyinstaller`)

Installing Python 3.5.2 via homebrew can be a bit tricky. The best way I've
found to do this is to make a backup of your current `/usr/local` (eg. move it
to `/usr/local_`) and reinstall Homebrew, then:

 1. `cd "$(brew --repo)"`
 2. `git fetch --unshallow`
 3. `git reset --hard ec545d45d4512ace3570782283df4ecda6bb0044`
 4. `git remote rm origin` (to prevent Homebrew from updating itself)
 5. Install `python3`, PyGObject3, etc.

Once you've done all of this, go to the location you cloned this repo, run
`./lockerapp` and make sure it works. If this is fine, proceed to the next
step.

Finally, use PyInstaller to bundle the application:

    $ pyinstaller --onefile -w -i BlitzLocker.icns --add-data res:res lockerapp

If all went well the `.app` folder will be left at `dist/lockerapp.app`. Rename
it as you like, and drop it in a `.dmg` disk.

