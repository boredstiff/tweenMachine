"""Utilities for TweenMachine"""

# import 3rd party modules
from PySide2 import QtWidgets

# import local modules
import settings


def get_maya_main_window():
    """Get the main Maya window.

    Returns:
        QtWidgets.QWidget: The Maya Main Window
    """
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj


def get_dialog():
    """Get a dialog window to parent the Tween Machine UI to.

    Returns:
        QtWidgets.QDialog: The dialog to parent the Tween Machine UI to.
    """
    dialog = QtWidgets.QDialog(parent=get_maya_main_window())
    dialog.setObjectName(settings.APP_NAME)
    dialog.setWindowTitle(settings.APP_TITLE)
    dialog.main_layout = QtWidgets.QVBoxLayout(dialog)
    dialog.setLayout(dialog.main_layout)
    dialog.setFixedWidth(400)
    dialog.setFixedHeight(400)
    dialog.setContentsMargins(0, 0, 0, 0)
    return dialog


def create_radio_button_group(parent_layout):
    """Create a radio button group and parent it to the given parent_layout.

    Args:
        parent_layout (QtWidgets.QHboxLayout): The parent layout for this widget.

    Returns:
        QtWidgets.QHBoxLayout: The layout containing the button group.
    """
    widget = QtWidgets.QWidget()
    widget_group = QtWidgets.QHBoxLayout()
    widget_group.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(widget_group)
    parent_layout.layout().addWidget(widget)
    return widget_group
