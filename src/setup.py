from setuptools import setup, find_packages

install_requires=["PyQt5", "pyqtgraph", \
                  "QDarkStyle", \
                  "pytango", "taurus", "taurus-pyqtgraph", \
                  "IPython", "qtconsole", 'magicgui']

setup(
    name = 'psd',
    version= '0.1.0',
    description='client app for PSD pump control',
    author='Canrong Qiu (Jackey)',
    author_email='canrong.qiu@desy.de',
    url='https://github.com/jackey-qiu/psd-client',
    classifiers=['Topic :: pump control',
                 'Programming Language :: Python'],
    license='MIT',
    python_requires='>=3.7, <=3.10',
    install_requires = install_requires,
    packages=find_packages(),
    package_data={'':['*.ui','*.ini','*.qrc'],'smart.bin':['*.png'], 'psd.gui.ui':['icons/*/*.png'],\
                  'psd.resource':['config/appsettings.ini']},
    entry_points = {
        'console_scripts' : [
            'psd = psd.bin.launch_app:main'
        ],
    }
)