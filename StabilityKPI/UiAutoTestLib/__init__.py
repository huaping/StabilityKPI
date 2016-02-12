from UiTestLib import UiTestLib

class UiAutoTestLib(UiTestLib):
    """
    """

    __version__ = '0.1'
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_EXIT_ON_FAILURE = True

    def __init__(self, serial = None):
        """
        """
        UiTestLib.__init__(self, serial)
