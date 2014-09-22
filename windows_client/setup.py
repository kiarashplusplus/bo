from setuptools import setup

import py2exe
setup(
    windows=[{"script":"desktop.py", "icon_resources": [(1, "eye.ico")]}],
    options={"py2exe" : { 'bundle_files': 1, 'compressed': True,  "includes" : ["sip","PyQt4"] }},zipfile = None)