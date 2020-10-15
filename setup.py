from distutils.core import setup
import py2exe

option = {
    'bundle_files':2,
    "optimize"      :2,
    'compressed': True
}
setup(
    options = {'py2exe': option},
    windows = [
        {"script"   :    "siimeter.py"}
    ],
    zipfile = 'siimeter.zip', 
    )