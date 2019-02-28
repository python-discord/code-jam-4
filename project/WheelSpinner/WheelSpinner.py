import tkinter as tk
from random import randint
import time

class WheelSpinner(tk.Frame):

    def __init__(self, master, wheel_options, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.wheel_options = wheel_options
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.drawn_arc = []
        self.count = None
        self.angle_increment = None
        self.current_time = None
        self.delta_time = None
        self.is_rotating = False

        self.frame = 0
        self.speed = 400
        self.draw()
        self.canvas.pack()
        self.canvas.bind("<Button-1>", lambda event: self.r(event))
        self.update()
        self.pack()

    def draw(self):
        self.count = len(self.wheel_options)
        angle = 0
        self.angle_increment = 360/self.count
        for option in self.wheel_options:
            if self.wheel_options[self.count-1] == option:
                self.drawn_arc.append(RotatingArc(self, 150, 150, 100, angle, 360, option,
                                                  fill=self.generate_random_color(), width=3))
            else:
                self.drawn_arc.append(RotatingArc(self, 150, 150, 100, angle, angle + self.angle_increment, option,
                                              fill=self.generate_random_color(), width=3))
            angle = angle + self.angle_increment

    def find_current_winner(self):
        for arc in self.drawn_arc:
            if 90+self.angle_increment >= arc.start_angle >= 90:

                winner = arc.text
        print(winner)
        self.after(500, self.find_current_winner)

    def update(self):
        if self.current_time is None:
            self.delta_time = 1/30
        else:
            self.delta_time = time.time() - self.current_time

        if self.is_rotating:
            self.rotate_all()
            self.calculate_new_speed()

        self.after(33, self.update)

    def r(self, event):
        self.is_rotating = True

    def rotate_all(self):
        for arc in self.drawn_arc:
            arc.rotate(int(self.speed*self.delta_time))
        #self.find_current_winner()
        self.frame += 1

    def calculate_new_speed(self):
        if self.speed >= 200:
            acceleration = -30
        elif self.speed >= 100:
            acceleration = -20
        else:
            acceleration = -10
        self.speed = self.speed + acceleration*self.delta_time
        if self.speed <= 0:
            self.speed = 0
            self.is_rotating = False

    def __get_elapsed_time(self):
        """
        This function returns the elapsed time since the last time we updated the rotating animation. If it's the first
        frame of the animation, we assume the elapsed_time is 0.033s which correspond to 30 fps.
        :return:
        """
        if self.is_animation_on is None:
            elapsed_time = 0.0333
        else:
            elapsed_time = time.time() - self.is_animation_on
        return elapsed_time

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
        return self.canvas.create_arc(x - r, y - r, x + r, y + r, **kwargs)

    def generate_random_color(self):
        R = randint(0, 255)
        G = randint(0, 255)
        B = randint(0, 255)

        return "#%02x%02x%02x" % (R, G, B)

class RotatingArc:
    def __init__(self, frame, position_x, position_y, radius, start_angle, end_angle, text, *args, **kwargs):
        self.frame_parent = frame
        self.canvas_parent = frame.canvas
        self.radius = radius
        self.position_x = position_x
        self.position_y = position_y
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.item = None
        self.text = text
        self.draw(*args, **kwargs)

    def draw(self, *args, **kwargs):
        self.item =self.frame_parent.create_circle_arc(self.position_x, self.position_y, self.radius,
                                                       start=self.start_angle, end=self.end_angle, *args, **kwargs)

    def rotate(self, angle, *args):
        self.canvas_parent.itemconfigure(self.item, start=self.start_angle + angle)
        self.start_angle += angle
        #if self.start_angle >= 360:
        #    self.start_angle -= 360



if __name__ == '__main__':
    root = tk.Tk()
    options = ['Name', 'Home Phone Number', 'Work Phone Number', 'Personal Phone Number', 'Email', 'Home Address', 'Notes']
    WheelSpinner(root, options, width=300, height=300)
    root.mainloop()
