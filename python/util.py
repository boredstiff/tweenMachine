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
