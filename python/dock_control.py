"""Dockable control for Maya UI items."""

# import built-in modules
import weakref

# import 3rd party modules
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

from shiboken2 import wrapInstance
from PySide2 import QtWidgets, QtCore

# import local modules
import settings


def dock_window(dialog_class, widget):
    """Dock the UI to a workspace control."""
    try:
        cmds.deleteUI(dialog_class.CONTROL_NAME)
    except:
        pass

    # building the workspace control with maya.cmds
    main_control = cmds.workspaceControl(
        settings.APP_NAME,
        tabToControl=["RangeSlider", -1],
        initialWidth=300,
        minimumWidth=True,
        widthProperty='preferred',
        label=dialog_class.DOCK_LABEL_NAME)

    # now lets get a C++ pointer to it using OpenMaya
    control_widget = OpenMayaUI.MQtUtil.findControl(settings.APP_NAME)
    # convert the C++ pointer to Qt object we can use
    control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)

    # control_wrap is the widget of the docking window and now we can start working with it:
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win = dialog_class(control_wrap, widget)

    # after maya is ready we should restore the window since it may not be visible
    cmds.evalDeferred(lambda *args: cmds.workspaceControl(main_control, e=True, rs=True))

    # will return the class of the dock content.
    return win.run()


class MyDockingUI(QtWidgets.QWidget):
    """A dockable widget that is compatible with Maya's docking functionality."""

    instances = list()

    def __init__(self, parent=None, widget=None):
        """Initialization for the docking UI.

        Args:
            parent (QtWidgets.QWidget): The widget that is the parent of this dock
                (should be a main window).
            widget (QtWidgets.QWidget): The widget to dock.
        """
        super(MyDockingUI, self).__init__(parent)

        # Keep track of docks, only create one at a time
        MyDockingUI.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        self.window_name = settings.APP_NAME
        self.ui = parent
        self.main_layout = parent.layout()
        self.main_layout.setContentsMargins(2, 2, 2, 2)

        self.my_widget = widget
        self.main_layout.addWidget(self.my_widget)

    @staticmethod
    def delete_instances():
        """Delete all instances of the dock, only allow for one at a time."""
        for instance in MyDockingUI.instances:
            try:
                instance.setParent(None)
                instance.deleteLater()
            except:
                # ignore the case in which the actual parent has already been deleted by Maya...
                pass

            MyDockingUI.instances.remove(instance)
            del instance

    def run(self):
        return self
