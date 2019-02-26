import tkinter as tk
import os
import math
from PIL import Image, ImageTk
from project.MouseController import MouseController
from project.PhoneNumber.PhoneButton import PhoneButton
import project.PhoneNumber.add_canvas_method


class PhoneCanvas(tk.Canvas):
    """
    TO-DO
    Class for PhoneCanvas

    === Public Attributes ===
    canvas_size: Name of the contact
    radius: All phone numbers of the contact
    phone_button_radius: All email addresses of the contact
    addresses: All physical addresses of the contact
    notes: Any notes the user wishes to leave for the contact

    === Methods ===
    change_name: Allows the user to change the name of the contact
    add_phone_number: Allows the user to add a phone number to any of the
                      categories Home, Work or Personal
    change_phone_number: Allows the user to change a number already entered, if
                         the number does not exist then nothing is done.
                         If the new_num param is '', then the number is removed
    add_address: Allows the user to add either an email address or a physical
                 address to the contact
    change_email_address: Allows the user to change an email address already
                          entered if the address does not exist then nothing is
                          done. If the new_add param is '', then the address is
                          removed
    change_address: Allows the user to change an email address already entered
                    if the address does not exist then nothing is done.
                    If the new_add param is '', then the address is removed

    new_note: Allows the user to leave a note for the contact
    change_note: Allows the user to change a note already entered, if the note
                 doesn't exist then nothing is done. If the new_note param is ''
                 then the notes is deleted

    """
    def __init__(self, master, width=600):

        super().__init__(master, width=width, height=width)

        self.canvas_size = width
        self.radius = int(self.canvas_size/2 * 0.9)
        self.phone_button_radius = int(self.radius*0.10)
        self.mouse_controller = MouseController(master)

        # radius of the circle where all the buttons will be layed out. 
        self.phone_button_pos_radius = int(0.7*self.canvas_size/2)  
        # List containing all the buttons
        self.circle_buttons = []
        # Stores the phone number that will be output in the current click.
        self.current_phone_number = None
        self.clicked_button = None

        # draw all the components of the phone
        self.draw_circles()
        self.draw_phone_buttons()
        self.draw_all_numbers()
        self.draw_stopper()

        self.bind("<Button-1>", self.verify_click_position)
        self.bind("<ButtonRelease-1>", self.mouse_release)
        
        self.pack()

    def send_output_number(self):
        if self.current_phone_number is not None:
            print(self.current_phone_number)

    def draw_circles(self):
        self.create_circle(self.canvas_size/2, self.canvas_size/2, self.radius, fill='black',
                           tag='main_circle', outline='#00536a', width='5')
        self.create_circle(self.canvas_size/2, self.canvas_size/2, self.radius*0.40, fill='#00536a',
                           outline='#00536a', width='3')

    def draw_phone_buttons(self):
        angle = 30 / 180 * math.pi
        for i in range(0, 10):
            x_center_of_circle = int(self.canvas_size/2 - self.phone_button_pos_radius * math.cos(angle))
            y_center_of_circle = int(self.canvas_size/2 - self.phone_button_pos_radius * math.sin(angle))
            self.circle_buttons.append(PhoneButton(self, x_center_of_circle, y_center_of_circle,
                                                   int(self.canvas_size/2), int(self.canvas_size/2),
                                                   self.phone_button_radius, str(i)))
            angle += 25 / 180 * math.pi

    def draw_stopper(self):
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

    def draw_all_numbers(self):
        angle = 30 / 180 * math.pi
        for i in range(0, 10):
            x_center_of_circle = self.canvas_size/2 - self.phone_button_pos_radius * math.cos(angle)
            y_center_of_circle = self.canvas_size/2 - self.phone_button_pos_radius * math.sin(angle)
            self.create_text(x_center_of_circle, y_center_of_circle, text=i, font=('Calibri', int(0.05*self.canvas_size)))
            angle += 25 / 180 * math.pi

    def rotate_all_circles(self, angle):
        for circle in self.circle_buttons:
            circle.rotate(angle)
        self.draw_all_numbers()

    def verify_click_position(self, event):
        x = event.x
        y = event.y

        for button in self.circle_buttons:
            if button.is_position_inside_circle(x, y):
                self.current_phone_number = None
                self.clicked_button = button
                button.on_click_down()
                return

    def mouse_release(self, event):
        if self.clicked_button is not None:
            self.clicked_button.on_click_release()
            self.clicked_button = None

    def update_current_phone_number(self):
        min_angle = 5.000
        current_button = None
        nearest_angle = math.inf
        for button in self.circle_buttons:
            if button.find_current_angle() < nearest_angle and button.find_current_angle() >= min_angle:
                nearest_angle = button.find_current_angle()
                current_button = button
        if current_button is not None and self.current_phone_number is None:
            self.current_phone_number = current_button
        elif current_button is not None and int(current_button.text)<int(self.current_phone_number.text):
            self.current_phone_number = current_button

    def find_angle_from_center(self, pos_x, pos_y):
        if pos_x <= self.canvas_size/2 and pos_y <= self.canvas_size/2:
            try:
                angle = math.atan((self.canvas_size/2 - pos_y) / (self.canvas_size/2 - pos_x))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#1 Current angle = " + str(angle))
            return angle
        elif pos_x >= self.canvas_size/2 and pos_y <= self.canvas_size/2:
            try:
                angle = math.atan((pos_x - self.canvas_size/2)/(self.canvas_size/2 - pos_y))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#2 Current angle = " + str(angle + 90/180*math.pi))
            return angle + 90/180*math.pi
        elif pos_x >= self.canvas_size/2 and pos_y >= self.canvas_size/2:
            try:
                angle = math.atan((pos_y - self.canvas_size/2) / (pos_x - self.canvas_size/2))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#3 Current angle = " + str(angle + 180 / 180 * math.pi))
            return angle + 180/180*math.pi
        else:
            try:
                angle = math.atan((self.canvas_size/2 - pos_x)/(pos_y - self.canvas_size/2))
            except ZeroDivisionError:
                angle = 90/180*math.pi
            # print("#4 Current angle = " + str(angle + 270 / 180 * math.pi))
            return angle + 270/180*math.pi



if __name__ == '__main__':
    root = tk.Tk()
    PhoneCanvas(root)
    root.mainloop()


