from distutils.core import setup
setup(
    name = 'xrfgui',
    packages = ['xrfgui','xrfgui.core', 'xrfgui.core.data_functions',
               'xrfgui.core.gui_functions', 'xrfgui.core.roi', 'xrfgui.core.tabs'],
    version = '0.0.10',
    entry_points={'console_scripts': ['xrfgui = xrfgui.program:main']},
    description = 'Vizualization and data manipulation tool for HXN Beamline',
    author='Derek Tropf',
    author_email='dt2516@columbia.edu',
    url='https://github.com/tropfcode/xrf-gui'
)