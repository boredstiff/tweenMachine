"""
tween_machine.py
"""

# Built-in
import contextlib
import json
import logging
import logging.config
import os
import sys
import tempfile
import urllib2
import webbrowser


# Third-party
from maya import cmds
from maya.api import _OpenMaya_py2 as OpenMaya
from maya.api import _OpenMayaAnim_py2 as OpenMayaAnim
# from maya.api import OpenMaya, OpenMayaAnim
from PySide2 import QtWidgets, QtCore

# import local modules
import dock_control
import settings
import util

__version__ = "3.1.0-alpha-1"

LOG = None

KEY_COLORS = [
    ('red', 'rgb(255, 0, 0)'),
    ('blue', 'rgb(0, 0, 255)'),
    ('green', 'rgb(0, 255, 0)')
]


def tween(bias, nodes=None):
    """

    Args:
        bias (float):
        nodes (list):  The specified nodes

    Returns:

    """
    if isinstance(nodes, list) and len(nodes) == 0:
        nodes = None

    if nodes is None:
        nodes = OpenMaya.MGlobal.getActiveSelectionList()

    if not nodes.length():
        return

    current_time = OpenMayaAnim.MAnimControl.currentTime()
    # I know I can query locked via OM, not sure about selected?
    attributes = cmds.channelBox(
        'mainChannelBox',
        query=True,
        selectedMainAttributes=True)

    selection_iterator = OpenMaya.MItSelectionList(nodes)
    dependency_fn = OpenMaya.MFnDependencyNode()

    # Loop through selected attributes, need to finish.
    # while not node_iterator.isDone():
    #     node = node_iterator.getDependNode()
    #     dependency_fn.setObject(node)
    #     for attribute in attributes:
    #         if dependency_fn.hasAttribute(attribute):
    #
    #     node_iterator.next()

    # I can use the thing I made at work to just get everything from the selection
    # curves =




def update_check():
    """Check for available updates.

    Returns:
        str: The new tag number, otherwise returns None.
    """
    url = 'https://api.github.com/repos/alexwidener/tweenMachine/releases/latest'
    with contextlib.closing(urllib2.urlopen(url)) as response:
        data = json.loads(response.read())
        # TODO: When doing the Qt rework, add a QMessageBox
        if data['tag_name'] > __version__:
            LOG.info('A new version of Tween Machine is available')
            return data['tag_name']
    return None


def get_logger():
    """Create a stream handler and a file handler. The file handler will only log warning and above.

    Returns:
        logging.Logger: The global instance of the logger.
    """
    global LOG

    configuration = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s'
            },
            'file_format': {
                'format': '%(asctime)s [%(levelname)-8s] %(message)s'
            }
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            },
            'file_handler': {
                'level': 'WARNING',
                'formatter': 'file_format',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'tween_machine.log'
            }
        },
        'loggers': {
            '': {
                'handlers': ['default', 'file_handler'],
                'level': 'INFO',
                'propagate': True,
                'maxBytes': 2048,
                'backupCount': 5
            }
        }
    }

    temp_dir = tempfile.gettempdir()
    tween_machine_dir = os.path.join(temp_dir, settings.APP_NAME)
    if not os.path.exists(tween_machine_dir):
        os.makedirs(tween_machine_dir)

    configuration['handlers']['file_handler']['filename'] = os.path.join(
        tween_machine_dir, configuration['handlers']['file_handler']['filename'])

    if not LOG:
        LOG = logging.getLogger(__name__)
        logging.config.dictConfig(configuration)

    return LOG


get_logger()
LOG.setLevel(logging.INFO)


class RetimeButton(QtWidgets.QPushButton):
    value_changed = QtCore.Signal(int)

    def __init__(self, parent=None, value=0, width=15, height=15):
        super(RetimeButton, self).__init__(parent)
        self.value = value
        self.clicked.connect(self.emit_value)
        self.setFixedWidth(width)
        self.setFixedHeight(height)
        self.setToolTip(str(self.value))
        self.setText(str(self.value))

    def emit_value(self, value):
        self.value_changed.emit(value)


class RetimingWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(RetimingWidget, self).__init__(parent)
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.setFixedWidth(200)
        top_button_layout = QtWidgets.QHBoxLayout()
        top_button_layout.setContentsMargins(0, 0, 0, 0)
        top_button_layout.setSpacing(2)

        bottom_button_layout = QtWidgets.QHBoxLayout()
        bottom_button_layout.setContentsMargins(0, 0, 0, 0)
        bottom_button_layout.setSpacing(5)

        bottom_left_layout = QtWidgets.QHBoxLayout()
        bottom_left_layout.setContentsMargins(0, 0, 0, 0)
        bottom_left_layout.setAlignment(QtCore.Qt.AlignLeft)
        bottom_left_layout.setSpacing(2)

        bottom_right_layout = QtWidgets.QHBoxLayout()
        bottom_right_layout.setContentsMargins(0, 0, 0, 0)
        bottom_right_layout.setAlignment(QtCore.Qt.AlignRight)
        bottom_right_layout.setSpacing(2)

        bottom_button_layout.addLayout(bottom_left_layout)
        bottom_button_layout.addLayout(bottom_right_layout)

        main_layout.addLayout(top_button_layout)
        main_layout.addLayout(bottom_button_layout)

        for i in range(1, 7):
            button = RetimeButton(self, i, 30, 15)
            top_button_layout.addWidget(button)

        for i in [-2, -1]:
            button = RetimeButton(self, i, 40, 15)
            bottom_left_layout.addWidget(button)

        for i in [1, 2]:
            button = RetimeButton(self, i, 40, 15)
            bottom_right_layout.addWidget(button)


class KeysBreakdownWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(KeysBreakdownWidget, self).__init__(parent)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        top_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.key_button = QtWidgets.QPushButton('K/R')
        self.breakdown_button = QtWidgets.QPushButton('B/G')

        top_layout.addWidget(self.key_button)
        top_layout.addWidget(self.breakdown_button)

        bottom_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        self.key_selected_attrs_combo = QtWidgets.QCheckBox()
        self.key_selected_attrs_combo.setText('Key All')
        bottom_layout.addWidget(self.key_selected_attrs_combo)


class TweenButton(QtWidgets.QPushButton):

    value_changed = QtCore.Signal(int)

    def __init__(self, parent=None, value=0):
        super(TweenButton, self).__init__(parent)
        self.value = value
        self.clicked.connect(self.emit_value)
        self.setFixedWidth(30)
        self.setFixedHeight(30)
        self.setToolTip(str(self.value))

    def emit_value(self):
        self.value_changed.emit(self.value)


class TweenSlider(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TweenSlider, self).__init__(parent)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        slider_layout = QtWidgets.QVBoxLayout()

        self.slider_value_line = QtWidgets.QLineEdit('0')
        main_layout.addWidget(self.slider_value_line)
        main_layout.addLayout(slider_layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(400)
        self.setMaximumHeight(75)
        slider_layout.setSpacing(2)

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(-100, 100)
        slider_layout.addWidget(self.slider)

        button_layout = QtWidgets.QHBoxLayout()
        slider_layout.addLayout(button_layout)
        button_layout.setAlignment(QtCore.Qt.AlignCenter)
        button_layout.setSpacing(5)

        self._create_array(button_layout)

        self.make_connections()
        self.show()

    def _create_array(self, parent_layout):
        distances = [-100, -75, -50, -25, 0, 25, 50, 75, 100]

        for value in distances:
            button = TweenButton(self, value)
            parent_layout.addWidget(button)
            button.value_changed.connect(self.button_was_changed)

    def button_was_changed(self, value):
        self.slider.setValue(value)

    def make_connections(self):
        self.slider.valueChanged.connect(self.value_changed)

    def value_changed(self, value):
        self.slider_value_line.setText(str(value))
        tween((value + 100) / 200.0)


class TweenMachineUI(QtWidgets.QWidget):

    MODE = {
        'keys': 0,
        'breakdowns': 1,
    }

    def __init__(self, parent=None):
        super(TweenMachineUI, self).__init__(parent)

        self.active_mode = self.MODE.get('keys')

        self.keys_button = None
        self.breakdowns_button = None
        self.tween_slider = None
        self.retiming_widget = None
        self.keys_breakdowns_widget = None
        self.key_color_widget = None
        self.help_widget = None

        self.build_ui()
        self.make_connections()

    def build_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(main_layout)
        main_layout.setAlignment(QtCore.Qt.AlignLeft)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        main_horizontal_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(main_horizontal_layout)

        mode_label = QtWidgets.QLabel('Mode: ')
        main_horizontal_layout.setAlignment(QtCore.Qt.AlignLeft)
        main_horizontal_layout.addWidget(mode_label)

        radio_layout = QtWidgets.QVBoxLayout()
        main_horizontal_layout.addLayout(radio_layout)

        radio_top_layout = QtWidgets.QHBoxLayout()
        radio_layout.addLayout(radio_top_layout)

        radio_bottom_layout = QtWidgets.QHBoxLayout()
        radio_layout.addLayout(radio_bottom_layout)
        self._create_keys_array(radio_top_layout)
        self._create_override_ripple_array(radio_bottom_layout)

        self.tween_slider = TweenSlider(self)
        main_horizontal_layout.addWidget(self.tween_slider)

        self.retiming_widget = RetimingWidget(self)
        main_horizontal_layout.addWidget(self.retiming_widget)

        self.keys_breakdowns_widget = KeysBreakdownWidget(self)
        main_horizontal_layout.addWidget(self.keys_breakdowns_widget)

        self.key_color_widget = KeyColorWidget(self)
        main_horizontal_layout.addWidget(self.key_color_widget)

        self.help_widget = HelpWidget(self)
        main_horizontal_layout.addWidget(self.help_widget)

    def _create_override_ripple_array(self, parent_layout):
        button_group = util.create_radio_button_group(parent_layout, 140)
        self.override_button = QtWidgets.QRadioButton('Overwrite')
        self.ripple_button = QtWidgets.QRadioButton('Ripple')
        for button in [self.override_button, self.ripple_button]:
            button_group.addWidget(button)
        self.override_button.setChecked(True)

    def _create_keys_array(self, parent_layout):
        """Create a radio button array parented to the given parent_layout.

        Args:
            parent_layout (QtWidgets.QHboxLayout): The parent layout to which we parent the buttons.
        """
        button_group = util.create_radio_button_group(parent_layout, 140)
        self.keys_button = QtWidgets.QRadioButton('Keys')
        self.breakdowns_button = QtWidgets.QRadioButton('Breakdowns')
        for button in [self.keys_button, self.breakdowns_button]:
            button_group.addWidget(button)
        self.keys_button.setChecked(True)

    def make_connections(self):
        self.keys_button.clicked.connect(lambda: self.set_active_mode(self.MODE.get('keys')))
        self.breakdowns_button.clicked.connect(lambda: self.set_active_mode(self.MODE.get('breakdowns')))

    def set_active_mode(self, value):
        """Set the currently active keying mode to the given value (passed in through a signal connection).

        Args:
            value (int): 0 represents key mode, 1 represents breakdown mode
        """
        print('Setting: {}'.format(value))
        self.active_mode = value


class KeyColorButton(QtWidgets.QPushButton):

    def __init__(self, parent=None, color=None, value=None):
        super(KeyColorButton, self).__init__(parent)
        self.color = color
        self.value = value
        self.setStyleSheet('background-color: %s;' % self.value)

    def keyPressEvent(self, *args, **kwargs):
        super(KeyColorButton, self).keyPressEvent(*args, **kwargs)
        self.emit(self.value)


class KeyColorWidget(QtWidgets.QWidget):
    # Whenever a user changes the key color, we'll want to update the drawing on the button
    # and also update the state on the main Widget so that any new keys are keyed with that color
    key_color_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(KeyColorWidget, self).__init__(parent)
        colors = KEY_COLORS
        color_group_layout = QtWidgets.QVBoxLayout()

        color_group_top_layout = QtWidgets.QHBoxLayout()
        color_group_bottom_layout = QtWidgets.QHBoxLayout()
        color_group_layout.addLayout(color_group_top_layout)
        color_group_layout.addLayout(color_group_bottom_layout)

        top_group = colors[:(len(colors) / 2)]
        bottom_group = colors[(len(colors) / 2):]

        self._set_group(top_group, color_group_top_layout)
        self._set_group(bottom_group, color_group_bottom_layout)

    def _set_group(self, group, layout):
        for color in group:
            button = KeyColorButton(self, color[0], color[1])
            layout.addWidget(button)


class HelpWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HelpWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.about_button = QtWidgets.QPushButton('Help')

        self.support_button = QtWidgets.QPushButton('Support')
        self.documentation_button = QtWidgets.QPushButton('Docs')

        layout.addWidget(self.about_button)
        self.make_connections()

    def make_connections(self):
        self.support_button.clicked.connect(self.open_support)
        self.documentation_button.clicked.connect(self.open_docs)
        self.about_button.clicked.connect(self.show_about_dialog)

    def show_about_dialog(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Tween Machine Help')
        layout = QtWidgets.QVBoxLayout()

        version_label = QtWidgets.QLabel('Version: {}'.format('version_number_here'))
        author_label = QtWidgets.QLabel('Authors: {}'.format('Alex Widener, Justin Barrett'))
        contact_label = QtWidgets.QLabel('github@alexwidener.com')
        note_label = QtWidgets.QLabel('Please file an issue by clicking "Support" before sending an e-mail')

        layout.addWidget(version_label)
        layout.addWidget(author_label)
        layout.addWidget(contact_label)
        layout.addWidget(note_label)

        layout.addWidget(self.support_button)
        layout.addWidget(self.documentation_button)

        dialog.setLayout(layout)
        dialog.show()

    @staticmethod
    def open_support():
        webbrowser.open(settings.GITHUB_ISSUES_URL)

    @staticmethod
    def open_docs():
        webbrowser.open(settings.GITHUB_URL)


def start():
    """
    Convenience function to open the main tweenMachine instance
    """
    ui = TweenMachineUI()
    dock_control.dock_window(dock_control.MyDockingUI, ui)
    # TMWindowUI()


def maya_useNewAPI():
    pass


class PluginCommand(OpenMaya.MPxCommand):
    kPluginCmdName = 'tween'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)

    def doIt(self, *args):
        start()


def cmdCreator():
    return PluginCommand()


def initializePlugin(plugin):
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        plugin_fn.registerCommand(PluginCommand.kPluginCmdName, cmdCreator)
    except Exception as exc:
        sys.stderr.write('Failed to register command: {}\n{}'.format(PluginCommand.kPluginCmdName, exc))


def uninitializePlugin(plugin):
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(PluginCommand.kPluginCmdName)
    except Exception as exc:
        sys.stderr.write('Failed to deregister command: {}\n{}'.format(PluginCommand.kPluginCmdName, exc))
