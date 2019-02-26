import math


class PhoneButton:
    """
        Class for phone button

        === Public Attributes ===
        parent_canvas: Canvas on which the button will be drawn.
        position_x: current x position of the button
        position_y: Current y position of the button
        rotation_point_x: x position of the center of rotation of the button
        rotation_point_y: y position of the center of rotation of the button
        radius: radius of the button
        text: text that is written in the button
        is_dragging: bool variable that stores if the button is currently being dragged
        item: contains the circle item for the canvas to use
        initial_angle: angle from the center of rotation of the initial position

        === Methods ===
        draw: Draws the circle on its canvas according to its public attributes
        find_current_angle: calculate the current angle from the center of the rotation point (in rad)
        is_position_inside_circle: Allows the user to verify if a position (x,y) is inside the circle of the PhoneButton
        rotate: Allows the user to rotate the button (from its center of rotation) by a given angle (rad)
        on_click_down: This method is called by the parent canvas when a click is inside the button. It starts the
                       private drag methods which allows to rotate the phone.
        on_click_release: This method is called by the parent canvas when the click is released. It starts the
                          rotating animation and sends the input to the parent canvas.
        """
    def __init__(self, parent_canvas, position_x: int, position_y: int,
                 rotation_point_x: int, rotation_point_y: int, radius: int, text: str):
        self.parent_canvas = parent_canvas
        self.position_x = position_x
        self.position_y = position_y
        self.rotation_point_x = rotation_point_x
        self.rotation_point_y = rotation_point_y
        self.radius = radius
        self.text = text
        self.is_dragging = False
        self.item = None
        self.initial_angle = self.find_current_angle()
        self.__max_angle = None
        self.draw()

    def draw(self) -> None:
        """
        This method draws the circle button at the location contained in it's attributes.
        :return: None
        """
        self.item = self.parent_canvas.create_circle(self.position_x, self.position_y, self.radius,
                                                     outline='#00536a', width='3', fill='white',)

    def find_current_angle(self) -> float:
        """
        :return: Returns the current angle (rad) positioning the center of the PhoneButton from the rotation point.
        """
        return self.parent_canvas.find_angle_from_center(self.position_x, self.position_y)

    def is_position_inside_circle(self, x, y) -> bool:
        """
        This method verifies if the position (x,y) is inside the circle of the PhoneButton
        :param x: absolute X position that is getting verified
        :param y: absolute Y position that is getting verified
        :return: returns True if the position that is getting verified is inside the circle of the PhoneButton,
                 returns False if not.
        """
        if math.sqrt(math.pow(self.position_x - x, 2) + math.pow(self.position_y - y, 2)) <= self.radius:
            return True
        else:
            return False

    def rotate(self, angle) -> None:
        """
        This method allows the user to rotate the button by the angle of its choice around the rotation point
        (typically the rotation point is the center of the phone)
        :param angle: angle to rotate the button (rad)
        :return: None
        """
        # Calculate the new x,y position of the PhoneButton
        pos_radius = self.parent_canvas.phone_button_pos_radius
        new_angle = self.find_current_angle() + angle
        new_position_x = self.parent_canvas.canvas_size/2 - pos_radius * math.cos(new_angle)
        new_position_y = self.parent_canvas.canvas_size/2 - pos_radius * math.sin(new_angle)
        x_to_move = new_position_x - self.position_x
        y_to_move = new_position_y - self.position_y

        # Update the position attributes
        self.position_x = new_position_x
        self.position_y = new_position_y

        # Move the button
        self.parent_canvas.move(self.item, x_to_move, y_to_move)

    def on_click_down(self) -> None:
        """
        This method is called by the parent canvas when the user clicks inside the button. It switch the is_dragging
        bool, reinitialize the max angle, and start the __drag() method.
        :return: None
        """
        self.is_dragging = True
        self.__max_angle = self.initial_angle
        self.__drag()

    def on_click_release(self) -> None:
        """
        This method is called by the parent canvas when the user releases the button. It switch the is_dragging
        bool, and starts the rotating animation.
        :return: None
        """
        self.is_dragging = False
        self.__animate_rotating_buttons()

    def __animate_rotating_buttons(self) -> None:
        rotating_speed = 0.08
        total_angle_to_rotate = self.find_current_angle() - self.initial_angle
        if self.find_current_angle() != self.initial_angle:
            if total_angle_to_rotate <= rotating_speed:
                self.parent_canvas.rotate_all_circles(-total_angle_to_rotate)
                self.parent_canvas.send_output_number()
            else:
                self.parent_canvas.rotate_all_circles(-rotating_speed)
                self.parent_canvas.after(50, self.__animate_rotating_buttons)

    def __drag(self) -> None:
        if self.is_dragging:
            angle_to_rotate = self.__find_angle_to_rotate_from_mouse_pos()
            self.parent_canvas.rotate_all_circles(angle_to_rotate)

            self.__update_highest_angle()
            self.parent_canvas.after(30, self.__drag)

    def __find_angle_to_rotate_from_mouse_pos(self) -> float:
        angle_of_stopper = 5.100
        mouse_pos_x, mouse_pos_y = self.parent_canvas.mouse_controller.get_absolute_position()

        current_mouse_pos_angle = self.parent_canvas.find_angle_from_center(mouse_pos_x, mouse_pos_y)
        current_button_angle = self.find_current_angle()

        if current_mouse_pos_angle <= self.initial_angle:
            angle_to_rotate = self.initial_angle - current_button_angle
        else:
            angle_to_rotate = current_mouse_pos_angle - current_button_angle
            if angle_to_rotate <= math.pi / 2:

                # If the next position would be passed the stopper, we stop the rotation at the stopper angle
                if self.find_current_angle() + angle_to_rotate >= angle_of_stopper:
                    angle_to_rotate = angle_of_stopper - self.find_current_angle()
        return angle_to_rotate

    def __update_highest_angle(self) -> None:
        if self.find_current_angle() > self.__max_angle:
            self.__max_angle = self.find_current_angle()
            self.parent_canvas.update_current_phone_number()







