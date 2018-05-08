# import built-in modules
import sys

from maya.api import OpenMaya


def start():
    print('Starting')


# Register as a Maya Command Plugin
class PluginCommand(OpenMaya.MPxCommand):
    kPluginCmdName = 'tweenMachine'

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
    except Exception as exc:
        sys.stderr.write('Failed to register command: {}\n{}'.format(PluginCommand.kPluginCmdName, exc))


def uninitializePlugin(plugin):
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(PluginCommand.kPluginCmdName)
    except Exception as exc:
        sys.stderr.write('Failed to deregister command: {}\n{}'.format(PluginCommand.kPluginCmdName, exc))