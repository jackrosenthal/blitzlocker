# BlitzLocker

BlitzLocker is an application for Salesforce developers and project owners to
quickly access their development site logins.

## Installation Instructions

To install BlitzLocker, you will need a machine running Linux or Mac OS X.

### Mac OS X

If you are running an Intel Macintosh with Mac OS X 10.9 or above, we have
already packaged a [`.dmg` file for you with an application ready to
go](https://github.com/jackrosenthal/blitzlocker/releases/tag/v1.0.0). Just drag
the application to your `Applications` folder.

If you are running an earlier verision than 10.9 or a PowerPC Macintosh,
BlitzLocker should still be compatible, you will have to just build the `.app`
folder yourself (described below).

### Linux (Ubuntu 14.04 or 16.04)

Download the prebuilt binary from
[here](https://github.com/jackrosenthal/blitzlocker/releases/tag/v1.0.0).

Extract the tarball:

    $ tar xf BlitzLocker_ubuntu14.04_amd64.tar.bz2

And run the program using `./BlitzLocker_amd64.bin`.

### Linux (systems which have GTK+ 3.22 or later)

You will need:

 * Python 2.7 or greater (Python 3.6 is reccomended)
 * PyGObject3 ([installation instructions](https://pygobject.readthedocs.io/en/latest/getting_started.html))
 * SQLAlchemy (`pip3 install sqlalchemy`)
 * GTK+ 3.22

After you have those dependencies installed, clone the repo and type
`./lockerapp`.

## Running BlitzLocker at Login

### Mac OS X

Right click (or control-click) on the BlitzLocker dock icon and select "Open at
Login".

### Linux

Add it to your `.xprofile` or `.xinitrc`, like so:

    #!/bin/bash
    # ... some stuff
    ~/blitzlocker/lockerapp &
    # ... some more stuff

## Using the System Tray in Ubuntu's Unity environment

Ubuntu's default environment, Unity, does not provide a system tray. This is
part of Mark Shuttleworth's opinion against system tray icons. You can
workaround his opinion by installing
[this indicator](https://github.com/GGleb/indicator-systemtray-unity)
that provides a system tray in Unity.

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

