# -*- coding: utf-8 -*-


# // module to manage the field view
# from ui.workspace_widget import Ui_workspace_widget
from pathlib import Path
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow

from psd import rs_path
from os import listdir
import yaml
from PyQt5.QtCore import pyqtSlot as Slot, QTimer
import threading

setting_file = str(Path(__file__).parent.parent / 'resource' / 'config' / 'appsettings.ini')
ui_file_folder = Path(__file__).parent / 'ui'

class smartGui(QMainWindow):

    _instance_lock = threading.Lock()

    def __init__(self, parent = None):
        """
        Initialize the class
        :param parent: parent widget
        :param settings_object: settings object
        """
        super(smartGui, self).__init__(parent)
        print(str(ui_file_folder / 'img_reg_main_window.ui'))
        uic.loadUi(str(ui_file_folder / 'img_reg_main_window.ui'), self)
        self.setMinimumSize(800, 600)
        self.widget_terminal.update_name_space('gui', self)
        self._parent = self
        self.populate_synoptic_viewer_config_files()
        self.connect_slots()
        self.init_attribute_values()

    '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(smartGui, "_instance"):
            with smartGui._instance_lock:
                if not hasattr(smartGui, "_instance"):
                    smartGui._instance = QMainWindow.__new__(cls)
        return smartGui._instance
    '''
        
    def init_attribute_values(self):
        self.first_client = True
        self.leftover_vol = 1000
        self.volume_change_on_the_fly = 50
        self.volume_syringe_1 = 0
        self.volume_syringe_2 = 0
        self.volume_syringe_3 = 0
        self.volume_syringe_4 = 0
        self.volume_reservoir = 0
        self.volume_cell = 0
        self.volume_waste = 0
        self.exchange_timer = QTimer()
        self.check_vol_timer = QTimer()

    def connect_slots(self):
        """
        :return:
        """
        #synoptic viewer control slots
        self.connect_slots_synoptic_viewer_control()

    def populate_synoptic_viewer_config_files(self):
        files = [each.rsplit('.')[0] for each in listdir(str(rs_path / 'config')) if each.endswith('yaml')]
        self.comboBox_viewer_filename.clear()
        self.comboBox_viewer_filename.addItems(files)

    @Slot(str)
    def populate_synoptic_objs(self, config_file_name):
        with open(str(rs_path / 'config' / (config_file_name+'.yaml')), 'r', encoding='utf8') as f:
           viewers = list(yaml.safe_load(f.read())['viewers'].keys())
        self.comboBox_viewer_obj_name.clear()
        self.comboBox_viewer_obj_name.addItems(viewers)

    def connect_slots_synoptic_viewer_control(self):
        self.horizontalSlider_sf.valueChanged.connect(self.set_scaling_factor)
        self.pushButton_render.clicked.connect(self.widget_synoptic.init_viewer)
        self.comboBox_viewer_filename.textActivated.connect(self.populate_synoptic_objs)

    def set_models(self):
        allkeys = self.settings_object.allKeys()
        selected_keys = [key for key in allkeys if key.rsplit('/')[0] in self.group_names]
        for each in selected_keys:
            model = self.settings_object.value(each)
            getattr(self, each.rsplit('/')[1]).model = model

    def set_scaling_factor(self):
        self.widget_synoptic.scale_composite_shapes(self.horizontalSlider_sf.value()/2)
        self.widget_synoptic.update()

    def statusUpdate(self, m):
        # slot for showing a message in the statusbar.
        self.statusbar.showMessage(m)

    def closeEvent(self, event):
        quit_msg = "About to Exit the program, are you sure? "
        reply = QMessageBox.question(self, 'Message', 
                        quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:        
            reply2 = QMessageBox.question(self, 'Message', 
                        "Do you want to save the image setting to db before exit?", QMessageBox.Yes, QMessageBox.No)
            if reply2 == QMessageBox.Yes:
                event.accept()
            else:
                event.accept()
        elif reply == QMessageBox.No:
            event.ignore()