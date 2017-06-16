import os
import subprocess
from blitzlocker.db import db, AppConfigItem

browsers = {
    'google-chrome-stable': {'private': '-incognito'},
    'chrome': {'private': '-incognito'},
    'chromium': {'private': '-incognito'},
    'chromium-browser': {'private': '-incognito'},
    'firefox': {'private': '--private-window'},
    'palemoon': {'private': '--private-window'},
    'iceweasel': {'private': '--private-window'},
    'icecat': {'private': '--private-window'},
    'epiphany': {'private': '-i'},
    'midori': {'private': '--private'},
    'xdg-open': {},
    'Safari': {},
}

# For Mac OS X
if os.path.isdir("/Applications"):
    bpaths = ["/Applications/Google Chrome.app/Contents/MacOS",
              "/Applications/Safari.app/Contents/MacOS",
              "/Applications/Firefox.app/Contents/MacOS"]
    os.putenv("PATH", os.getenv("PATH") + ':' + ':'.join(bpaths))

system_browsers = set()
for d in os.getenv("PATH").split(":"):
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if fn in browsers.keys():
                system_browsers.add(fn)

def open_browser(browser, url, private=False):
    return subprocess.Popen(
        [browser] + ([browsers[browser].get('private', '')] if private else []) + [url]
    )

def open_configured_browser(url):
    default_browser = db.query(AppConfigItem)\
            .filter(AppConfigItem.key == 'browser.choice')\
            .one_or_none()
    if not default_browser:
        for b in ('xdg-open', 'chrome', 'firefox', 'Safari'):
            if b in system_browsers:
                default_browser = b
                break
        else:
            return
    else:
        default_browser = default_browser.value
    private = db.query(AppConfigItem)\
            .filter(AppConfigItem.key == 'browser.private')\
            .one_or_none()
    if private:
        private = private.value
    return open_browser(default_browser, url, private)
