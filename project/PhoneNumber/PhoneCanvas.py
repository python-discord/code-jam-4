import tkinter as tk
import math
from project.MouseController import MouseController
from project.PhoneNumber.PhoneButton import PhoneButton


class PhoneCanvas(tk.Canvas):
    """
    Class for PhoneCanvas, draws a working rotary phone. The user can click and drag the button in order to dial a
    phone number. It outputs

    === Public Attributes ===
    canvas_size: Size of the canvas (square canvas of size X size)
    radius: Biggest radius of the phone
    phone_button_radius: Radius of all the phone buttons
    phone_button_pos_radius: Radius of the circle where all the phone buttons are layed out
    circle_buttons: List containing all the phone buttons.
    mouse_controller: MouseController object linked to the root window of the canvas.

    === Methods ===
    create_circle: Simple canvas method allowing to draw a circle.
    create_circle_arc: Simple canvas method allowing to draw a circle arc.
    send_output_number: This method is called by the PhoneButton when their rotating animation is done. It sends
                        the number to the __output_entry
    rotate_all_circles: This method rotates all the PhoneButton by the given angle.
    verify_click_position: This method verifies where the user clicked. If it's inside one of the PhoneButton, it
                           calls the PhoneButton.on_mouse_down() method.
    mouse_release: This method is called when the mouse button is released. It calls the PhoneButton method of the
                   button that was clicked.
    update_current_phone_number: This method verifies the position of all the PhoneButton and store the current phone
                                 number that should be dialed if the user stops moving.
    find_angle_from_center: This method takes a position (x,y) and returns the angle of this position according to
                            the center of the phone.
    """
    def __init__(self, master, width=300):
        super().__init__(master, width=width, height=width)
        self.master = master
        self.configure(bg='#00536a', border=0, bd=0, highlightthickness=0, relief='ridge')
        self.canvas_size = width
        self.radius = int(self.canvas_size/2 * 0.99)
        self.phone_button_radius = int(self.radius*0.10)
        # radius of the circle where all the buttons will be layed out. 
        self.phone_button_pos_radius = int(0.7*self.canvas_size/2)  
        # List containing all the buttons
        self.circle_buttons = []
        self.mouse_controller = MouseController(master)

        # Stores the phone number that will be output in the current click.
        self.__current_phone_number = None
        self.__clicked_button = None

        # draw all the components of the phone
        self.__draw_circles()
        self.__draw_phone_buttons()
        self.__draw_all_numbers()
        self.__draw_stopper()

        self.bind("<Button-1>", self.verify_click_position)
        self.bind("<ButtonRelease-1>", self.mouse_release)


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

    def send_output_number(self):
        # TODO -> Figure out exactly how the output will be managed.
        return self.__current_phone_number.text

    def rotate_all_circles(self, angle: float) -> None:
        """
        This method rotates all the PhoneButton by the given angle (rad)
        :param angle: angle that we want to rotate all the buttons (rad)
        :return: None
        """
        for circle in self.circle_buttons:
            circle.rotate(angle)
        # Redraw all the numbers on top of the PhoneButton.
        self.__draw_all_numbers()

    def verify_click_position(self, event) -> None:
        """
        This method verifies the click position and call the PhoneButton.on_click_down() method if the click is
        inside the PhoneButton.
        :param event: The event is a "<Button-1>" event.
        :return: None
        """
        x = event.x
        y = event.y
        for button in self.circle_buttons:
            if button.is_position_inside_circle(x, y):
                self.__current_phone_number = None
                self.__clicked_button = button
                button.on_click_down()
                return

    def mouse_release(self, event) -> None:
        """
        This method is linked to the button release event. It verifies if a button was being dragged and calls its
        on_click_release method if that's the case.
        :param event: "<ButtonRelease-1>"
        :return: None
        """
        if self.__clicked_button is not None:
            self.__clicked_button.on_click_release()
            self.__clicked_button = None

    def update_current_phone_number(self) -> None:
        """
        This method verifies all the PhoneButton position and change the __current_phone_number variable to the number
        that should be dialed if the user release the current drag.
        :return: None
        """
        min_angle = 5.000
        current_button = None
        nearest_angle = math.inf
        for button in self.circle_buttons:
            if min_angle <= button.find_current_angle() < nearest_angle:
                nearest_angle = button.find_current_angle()
                current_button = button
        if current_button is not None and self.__current_phone_number is None:
            self.__current_phone_number = current_button
        elif current_button is not None and int(current_button.text) < int(self.__current_phone_number.text):
            self.__current_phone_number = current_button

    def find_angle_from_center(self, pos_x: int, pos_y: int) -> float:
        """
        This methods calculates the angle of a given position x,y from the center of the phone.
        :param pos_x: X position to calculate the angle to
        :param pos_y: Y position to calculate the angle to
        :return: angle in rad
        """
        # First quadrant of the circle.
        if pos_x <= self.canvas_size/2 and pos_y <= self.canvas_size/2:
            try:
                angle = math.atan((self.canvas_size/2 - pos_y) / (self.canvas_size/2 - pos_x))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#1 Current angle = " + str(angle))
            return angle
        # 2nd quadrant of the circle.
        elif pos_y <= self.canvas_size/2 <= pos_x:
            try:
                angle = math.atan((pos_x - self.canvas_size/2)/(self.canvas_size/2 - pos_y))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#2 Current angle = " + str(angle + 90/180*math.pi))
            return angle + 90/180*math.pi
        # 3rd quadrant of the circle.
        elif pos_x >= self.canvas_size/2 and pos_y >= self.canvas_size/2:
            try:
                angle = math.atan((pos_y - self.canvas_size/2) / (pos_x - self.canvas_size/2))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#3 Current angle = " + str(angle + 180 / 180 * math.pi))
            return angle + 180/180*math.pi
        # 4th quadrant of the circle.
        else:
            try:
                angle = math.atan((self.canvas_size/2 - pos_x)/(pos_y - self.canvas_size/2))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#4 Current angle = " + str(angle + 270 / 180 * math.pi))
            return angle + 270/180*math.pi

    def __draw_circles(self):
        self.create_circle(self.canvas_size/2, self.canvas_size/2, self.radius, fill='black',
                           tag='main_circle', outline='#00536a', width='5')
        self.create_circle(self.canvas_size/2, self.canvas_size/2, self.radius*0.40, fill='#00536a',
                           outline='#00536a', width='3')

    def __draw_phone_buttons(self):
        angle = 30 / 180 * math.pi
        for i in range(0, 10):
            x_center_of_circle = int(self.canvas_size/2 - self.phone_button_pos_radius * math.cos(angle))
            y_center_of_circle = int(self.canvas_size/2 - self.phone_button_pos_radius * math.sin(angle))
            self.circle_buttons.append(PhoneButton(self, x_center_of_circle, y_center_of_circle,
                                                   int(self.canvas_size/2), int(self.canvas_size/2),
                                                   self.phone_button_radius, str(i)))
            angle += 25 / 180 * math.pi

    def __draw_stopper(self):
        stopper_angle = 60
        stopper_radius = self.radius * 0.15

        self.create_circle_arc(self.canvas_size/2, self.canvas_size/2, stopper_radius, fill='#00536a',
                               outline='white', width=5,
                               start=stopper_angle-90, end=stopper_angle+90, style='arc')
        x1 = self.canvas_size/2 - stopper_radius*math.cos((90-stopper_angle)/180*math.pi)
        y1 = self.canvas_size/2 - stopper_radius*math.sin((90-stopper_angle)/180*math.pi)
        x2 = self.canvas_size/2 - self.radius*math.sin((90-stopper_angle)/180*math.pi)
        y2 = self.canvas_size / 2 + self.radius * math.cos((90 - stopper_angle) / 180 * math.pi)
        x3 = self.canvas_size / 2 + stopper_radius * math.cos((90 - stopper_angle) / 180 * math.pi)
        y3 = self.canvas_size / 2 + stopper_radius * math.sin((90 - stopper_angle) / 180 * math.pi)

        self.create_polygon([x1, y1, x2, y2, x3, y3], fill='#00536a', outline='white', width=5)
        self.create_circle(self.canvas_size / 2, self.canvas_size / 2, stopper_radius-4, fill='#00536a', width=0)

    def __draw_all_numbers(self):
        angle = 30 / 180 * math.pi
        for i in range(0, 10):
            x_center_of_circle = self.canvas_size/2 - self.phone_button_pos_radius * math.cos(angle)
            y_center_of_circle = self.canvas_size/2 - self.phone_button_pos_radius * math.sin(angle)
            self.create_text(x_center_of_circle, y_center_of_circle, text=i, font=('Calibri', int(0.05*self.canvas_size)))
            angle += 25 / 180 * math.pi


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    PhoneCanvas(root, tk.Entry)
    root.mainloop()


