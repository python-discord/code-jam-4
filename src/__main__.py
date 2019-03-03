from .main import App

if __name__ == "__main__":
    root = App()
    root.protocol('WM_DELETE_WINDOW', root.cleanup)
    root.mainloop()
