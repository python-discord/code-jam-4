from infi.systray import SysTrayIcon

class systray:
    """ Class which contains logic for a system tray interactive icon"""

    # temp icon & name
    icon = "project\\tempicon.ico"
    name = "Example tray icon"
    
    def __init__(self, closecallback):
        # in future will have an function as a argument to work with rest of app

        # temp options for right click 
        menu_options = (("Say Hello", None, self.say_hello),)
        self.systray = SysTrayIcon(self.icon, self.name, menu_options, on_quit=closecallback)

    def say_hello(self, systray):
        print("Hello, World!")

    def start(self):
        """ Starts systray icon"""
        self.systray.start()

    def close(self):
        """ Closes systray icon"""
        self.systray.shutdown()
        # this function also runs the callback:(
        