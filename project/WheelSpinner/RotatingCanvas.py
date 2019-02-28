import tkinter as tk


class RotatingCanvas(tk.Canvas):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.arc = RotatingArc(self, 100, 200, 200, -2, 2)
        self.bind("<Button-1>", lambda event, angle=1, *args: self.arc.rotate(event, angle, *args))

    def create_circle(self, x, y, r, **kwargs) -> classmethod:
        """
        Allows the user to draw a circle on the canvas.
        :param x: X position of the center of the circle
        :param y: Y position of the center of the circle
        :param r: Radius of the circle
        :param kwargs:
        :return: Modified create_oval method to draw the circle with the given parameters.
        """
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def create_circle_arc(self, x, y, r, **kwargs) -> classmethod:
        """
        This method draws a circle arc on the canvas
        :param x: X position of the center of the arc
        :param y: Y position of the center of the arc
        :param r: Radius of the arc
        :param kwargs: important parameter are 'start' and 'end' to setup the angle where the arc is positioned.
        :return: Returns the modified create_arc methods that will actually draw a circle_arc with the given parameters.
        """
        if "start" in kwargs and "end" in kwargs:
            kwargs["extent"] = kwargs["end"] - kwargs["start"]
            del kwargs["end"]
        return self.create_arc(x - r, y - r, x + r, y + r, **kwargs)


class RotatingArc:
    def __init__(self, canvas_parent, position_x, position_y, radius, start_angle, end_angle, *args, **kwargs):
        self.canvas_parent = canvas_parent
        self.radius = radius
        self.position_x = position_x
        self.position_y = position_y
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.item = None
        self.draw(*args, **kwargs)


    def draw(self, *args, **kwargs):
        self.item =self.canvas_parent.create_circle_arc(self.position_x, self.position_y, self.radius,
                                                        start=self.start_angle, end=self.end_angle, *args, **kwargs)

    def rotate(self,event, angle, *args):
        print("rotating")
        if self.start_angle<360:
            self.canvas_parent.itemconfigure(self.item, start=self.start_angle + angle)
            self.start_angle += angle

            self.canvas_parent.after(33, lambda event=event, a=0.5: self.rotate(event, a))

if __name__ == '__main__':
    root = tk.Tk()
    a = RotatingCanvas(root, width=500, height=500)
    a.pack()
    root.mainloop()
