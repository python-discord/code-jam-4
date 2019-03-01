import tkinter as tk
from random import randint
import time
import math
from project.MouseController import MouseController

class WheelSpinner(tk.Frame):

    def __init__(self, master, wheel_options, radius, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.radius = radius
        self.display_label = tk.Label(self)
        self.wheel_options = wheel_options
        self.size = radius*2.1
        self.canvas = tk.Canvas(self, width=self.size, height=self.size)
        self.drawn_arc = []
        self.count = None
        self.angle_increment = None

        self.frame = 0
        self.speed = 400
        #self.draw()
        self.display_label.pack()
        self.canvas.pack()

        self.canvas.bind("<Button-1>", lambda event: self.verify_click_position(event))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.on_mouse_release(event))

        self.__drawn = False
        self.__rotation_speed_list = []
        self.__is_dragging = False
        self.__init_drag_pos = None
        self.__current_time = None
        self.__delta_time = None
        self.__is_rotating = False
        self.__mouse_controller = MouseController(self.canvas)

        self.update()
        self.pack()

    def draw(self):
        self.count = len(self.wheel_options)
        angle = 0
        self.angle_increment = 360/self.count
        for option in self.wheel_options:
            print(option)
            if self.wheel_options[self.count-1] == option:
                self.drawn_arc.append(RotatingArc(self, self.size/2, self.size/2, self.radius, angle, 360, option,
                                                  fill=self.generate_random_color(), width=3))
            else:
                self.drawn_arc.append(RotatingArc(self, self.size/2, self.size/2, self.radius, angle,
                                                  angle + self.angle_increment, option,
                                                  fill=self.generate_random_color(), width=3))
            angle = angle + self.angle_increment

        self.__drawn = True

    def erase(self):
        self.canvas.delete('all')

    def display_current_winner(self):
        winner = None
        for arc in self.drawn_arc:
            if 90 >= arc.start_angle >= 90-self.angle_increment:

                winner = arc.text
        if winner is not None:
            self.display_label['text'] = winner

    def update(self):
        if not self.__drawn:
            self.after(33, self.update)
            return
        if self.__current_time is None:
            self.__delta_time = 1 / 30
        else:
            self.__delta_time = time.time() - self.__current_time

        if self.__is_rotating:
            self.rotate_all_with_speed()
            self.calculate_new_speed()
            self.display_current_winner()

        if self.__is_dragging:
            print('drag')
            self.drag()

        self.after(33, self.update)

    def verify_click_position(self, event):
        if self.__is_dragging or self.__is_rotating:
            return

        if not self.__drawn:
            self.draw()
            self.__drawn = True
            return

        x, y = event.x, event.y

        #self.is_rotating = True

        if math.sqrt(math.pow(self.size/2 - x, 2) + math.pow(self.size/2 - y, 2)) <= self.radius:
            self.__is_dragging = True
            self.__rotation_speed_list = []
            self.__init_drag_pos = x, y

    def drag(self):
        x0, y0 = self.__init_drag_pos
        x, y = self.__mouse_controller.get_absolute_position()
        angle_to_rotate = math.atan2(y - self.size/2, x - self.size/2) - math.atan2(y0 - self.size/2, x0 - self.size/2)
        self.rotate_all(-angle_to_rotate/math.pi*180)
        self.__rotation_speed_list.append((angle_to_rotate/math.pi*180/self.__delta_time))
        self.__init_drag_pos = x, y

    def on_mouse_release(self, event):
        if self.__is_dragging:
            self.__is_dragging = False
            self.__calculate_initial_speed()
            self.__is_rotating = True

    def __calculate_initial_speed(self):
        self.speed = -self.__rotation_speed_list[-1]

    def rotate_all(self, degree):
        for arc in self.drawn_arc:
            arc.rotate(degree)

    def rotate_all_with_speed(self):
        for arc in self.drawn_arc:
            arc.rotate(self.speed * self.__delta_time)

    def calculate_new_speed(self):
        speed_pos = abs(self.speed)
        if speed_pos >= 2000:
            acceleration = 600 * -math.copysign(1, self.speed)
        elif speed_pos >= 1000:
            acceleration = 250 * -math.copysign(1, self.speed)
        elif speed_pos >= 600:
            acceleration = 120 * -math.copysign(1, self.speed)
        elif speed_pos >= 350:
            acceleration = 60 * -math.copysign(1, self.speed)
        elif speed_pos >= 200:
            acceleration = 30 * -math.copysign(1, self.speed)
        elif speed_pos >= 100:
            acceleration = 20 * -math.copysign(1, self.speed)
        else:
            acceleration = 10 * -math.copysign(1, self.speed)

        if math.copysign(1, self.speed) != math.copysign(1, self.speed + acceleration*self.__delta_time):
            self.speed = 0
            self.finish_rotation()
        else:
            self.speed = self.speed + acceleration*self.__delta_time
        print('speed = ' + str(self.speed))
        print(acceleration)

    def finish_rotation(self):
        self.__is_rotating = False
        self.erase()
        self.__drawn = False

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
        if self.start_angle >= 360:
            self.start_angle -= 360
        if self.start_angle < 0:
            self.start_angle += 360



if __name__ == '__main__':
    root = tk.Tk()
    options = ['Name', 'Home Phone Number', 'Work Phone Number', 'Personal Phone Number', 'Email', 'Home Address', 'Notes']
    WheelSpinner(root, options, width=300, height=500, radius=150)
    root.mainloop()
