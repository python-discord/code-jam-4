class MouseController:
    def __init__(self, root):
        self.root = root

    def get_absolute_position(self):
        x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        y = self.root.winfo_pointery() - self.root.winfo_rooty()
        return x, y
