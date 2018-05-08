from maya.api import OpenMaya
# import maya.OpenMayaUI as old_omui
import sys
from PySide2 import QtWidgets, QtCore
# from shiboken2 import wrapInstance
from .app.maya import dock_control

PACKAGE_NAME = 'Tween Machine'


def maya_useNewAPI():
    pass


class TweenSlider(QtWidgets.QStackedWidget):
    def __init__(self, parent=None):
        super(TweenSlider, self).__init__(parent)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.addWidget(self.slider)
        self.button = QtWidgets.QPushButton('hi')
        self.addWidget(self.button)


class TweenMachineUI(QtWidgets.QWidget):

    keys_mode = 0
    breakdown_mode = 1

    something = '{key} is something'

    def __init__(self, parent=None):
        super(TweenMachineUI, self).__init__(parent)
        # Become adopted

        # self.parent().layout().addWidget(self)
        self.main_layout = None
        self.menu_bar = None
        self.mode_label = None

        self.active_mode = self.keys_mode
        # self.show()

        # UI Elements
        self.keys_button = None
        self.breakdowns_button = None
        self.tween_slider = None

        self.build_ui()
        self.make_connections()

    def build_ui(self):
        # TODO(Alex) Check for updates
        # Build Menu
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        # self.menu_bar = QtWidgets.QMenuBar(self)
        # self.menu_bar.setContentsMargins(0, 0, 0, 0)
        # self.main_layout.addWidget(self.menu_bar)

        # Whatever, figure this shit out later.
        # options_item = self.menu_bar.addMenu('Options')
        # show_menu = options_item.addMenu('&Show...')
        # menu_bar_option = show_menu.addAction('&Menu Bar')
        # label_option = show_menu.addAction('&Label')
        # show_menu.addSeparator()
        # slider_action_group = QtWidgets.QActionGroup(show_menu)
        #
        # show_menu.addAction('Slider and &Buttons')
        # show_menu.addAction('Slider Only')

        self.main_horizontal_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.main_horizontal_layout)

        self.mode_label = QtWidgets.QLabel('Mode: ')
        self.main_horizontal_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.main_horizontal_layout.addWidget(self.mode_label)
        self._create_array(self.main_horizontal_layout)

        self.tween_slider = TweenSlider(self)
        print('should have added it')
        self.main_horizontal_layout.addWidget(self.tween_slider)
        # self.tween_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # self.tween_slider.setFixedWidth(200)
        # self.main_horizontal_layout.addWidget(self.tween_slider)

    def _create_radio_button_group(self, parent_row_layout):
        widget = QtWidgets.QWidget()
        widget_group = QtWidgets.QHBoxLayout()
        widget_group.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(widget_group)
        parent_row_layout.layout().addWidget(widget)
        return widget_group

    def _create_array(self, parent_layout):
        button_group = self._create_radio_button_group(parent_layout)
        # TODO (Alex): Clean this up, this is a fucking mess.
        self.keys_button = QtWidgets.QRadioButton('Keys')
        self.breakdowns_button = QtWidgets.QRadioButton('Breakdowns')
        buttons = [self.keys_button, self.breakdowns_button]
        for button in buttons:
            button_group.addWidget(button)
        buttons[0].setChecked(True)
        return buttons

    def make_connections(self):
        self.keys_button.clicked.connect(lambda: self.set_active_mode(self.keys_mode))
        self.breakdowns_button.clicked.connect(lambda: self.set_active_mode(self.breakdown_mode))

    def set_active_mode(self, value):
        print('Setting: {}'.format(value))
        self.active_mode = value

    def contextMenuEvent(self, event):
        options_menu = QtWidgets.QMenu()
        show_menu = options_menu.addMenu('&Show...')
        menu_bar_option = show_menu.addMenu('&Menu Bar')
        label_option = show_menu.addAction('&Label')

        action = options_menu.exec_(self.mapToGlobal(event.pos()))
        if action == menu_bar_option:
            print 'uh oh'


def get_maya_main_window():
    """

    Returns:

    """
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj

    # window = old_omui.MQtUtil_mainWindow()
    # pointer = wrapInstance(long(window), QtWidgets.QMainWindow)
    # return pointer


def get_dialog():
    """Get a dialog window to parent the Tween Machine UI to.

    Returns:
        QtWidgets.QDialog: The dialog to parent the Tween Machine UI to.
    """
    dialog = QtWidgets.QDialog(parent=get_maya_main_window())
    dialog.setObjectName('tweenMachine')
    dialog.setWindowTitle(PACKAGE_NAME)
    dialog.main_layout = QtWidgets.QVBoxLayout(dialog)
    dialog.setLayout(dialog.main_layout)
    dialog.setFixedWidth(400)
    dialog.setFixedHeight(400)
    dialog.setContentsMargins(0, 0, 0, 0)
    return dialog


def start():
    # dialog = get_dialog()
    ui = TweenMachineUI()
    dock = dock_control.dock_window(dock_control.MyDockingUI, ui)
    # TweenMachineUI(dialog)
    # dialog.show()
    print('ran it')


class PluginCommand(OpenMaya.MPxCommand):
    kPluginCmdName = 'tween'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    def doIt(self, *args):
        OpenMaya.MGlobal.displayInfo('Hello again')
        start()


def cmdCreator():
    return PluginCommand()


def initializePlugin(plugin):
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        plugin_fn.registerCommand(PluginCommand.kPluginCmdName, cmdCreator)
    except:
        sys.stderr.write('Failed to register command: ' + PluginCommand.kPluginCmdName)


def uninitializePlugin(plugin):
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(PluginCommand.kPluginCmdName)
    except:
        sys.stderr.write('Failed to deregister command: ' + PluginCommand.kPluginCmdName)


