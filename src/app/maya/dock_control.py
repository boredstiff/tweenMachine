"""Original author: Lior ben horin

Docking a UI

"""
import weakref

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
from shiboken2 import wrapInstance

from PySide2 import QtWidgets, QtCore


def dock_window(dialog_class, widget):
    try:
        cmds.deleteUI(dialog_class.CONTROL_NAME)
    except:
        pass

    # building the workspace control with maya.cmds
    main_control = cmds.workspaceControl(dialog_class.CONTROL_NAME, ttc=["RangeSlider", -1], iw=300, mw=True,
                                         wp='preferred', label=dialog_class.DOCK_LABEL_NAME)

    # now lets get a C++ pointer to it using OpenMaya
    control_widget = OpenMayaUI.MQtUtil.findControl(dialog_class.CONTROL_NAME)
    # conver the C++ pointer to Qt object we can use
    control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)

    # control_wrap is the widget of the docking window and now we can start working with it:
    control_wrap.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    win = dialog_class(control_wrap, widget)

    # after maya is ready we should restore the window since it may not be visible
    cmds.evalDeferred(lambda *args: cmds.workspaceControl(main_control, e=True, rs=True))

    # will return the class of the dock content.
    return win.run()


class MyDockingUI(QtWidgets.QWidget):
    instances = list()
    CONTROL_NAME = 'tween_machine'
    DOCK_LABEL_NAME = 'Tween Machine'

    def __init__(self, parent=None, widget=None):
        super(MyDockingUI, self).__init__(parent)

        # let's keep track of our docks so we only have one at a time.
        MyDockingUI.delete_instances()
        self.__class__.instances.append(weakref.proxy(self))

        self.window_name = self.CONTROL_NAME
        self.ui = parent
        self.main_layout = parent.layout()
        self.main_layout.setContentsMargins(2, 2, 2, 2)

        # here we can start coding our UI
        self.my_widget = widget
        self.main_layout.addWidget(self.my_widget)

    @staticmethod
    def delete_instances():
        for ins in MyDockingUI.instances:
            try:
                ins.setParent(None)
                ins.deleteLater()
            except:
                # ignore the fact that the actual parent has already been deleted by Maya...
                pass

            MyDockingUI.instances.remove(ins)
            del ins

    def run(self):
        return self
