import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from psd.gui.main_gui import smartGui

def main():
    import qdarkstyle
    sys.path.append(str(Path(__file__).parent.parent))
    sys.path.append(str(Path(__file__).parent.parent / 'gui' / 'widgets'))

    QApplication.setStyle("windows")
    app = QApplication(sys.argv)
    myWin = smartGui()
    # myWin.init_taurus()
    myWin.setWindowIcon(QtGui.QIcon(str(Path(__file__).parent / 'smart_logo.png')))
    myWin.setWindowTitle("PSD")
    myWin.showMaximized() 
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()