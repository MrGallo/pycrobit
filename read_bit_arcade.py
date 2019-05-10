import time
import threading

import arcade

from pycrobit import Microbit, connect_microbit
from pycrobit import utils

WIDTH = 640
HEIGHT = 480

player_x = 0
player_y = 0
window = arcade.open_window(WIDTH, HEIGHT, "My Arcade Game")


def setup():
    global microbit

    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/60)

    with connect_microbit("COM3") as microbit:
        arcade.run()


def update(delta_time):
    global microbit, player_x, player_y
    # 0 - WIDTH

    # Get microbit data
    accelerometer_x = microbit.accelerometer.get_x()
    accelerometer_y = microbit.accelerometer.get_y()

    # set player location to the microbit x and y location
    # map_value() translates x and y values to the size of the arcade window
    # The range of -1000 to 1000 from the microbit gets translated to
    # a range of 0 to WIDTH to fit our arcade window
    player_x = utils.map_value(accelerometer_x, -1000, 1000, 0, WIDTH)
    player_y = utils.map_value(accelerometer_y, -1000, 1000, HEIGHT, 0)

    # is_pressed() checks if the button is being held.
    if microbit.button_a.is_pressed():
        print("button a is being held")

    # was_pressed() ensures only a single trigger
    if microbit.button_a.was_pressed():
        print("button a was pressed down")


@window.event
def on_draw():
    global microbit, player_x
    arcade.start_render()
    # Draw in here...

    if microbit.button_a.is_pressed():
        arcade.draw_lrtb_rectangle_filled(0, WIDTH/2, HEIGHT, 0, arcade.color.RED)
    if microbit.button_b.is_pressed():
        arcade.draw_lrtb_rectangle_filled(WIDTH/2, WIDTH, HEIGHT, 0, arcade.color.ORANGE)

    # DRAW PLAYER
    arcade.draw_circle_filled(player_x, player_y, 25, arcade.color.BLUE)

    gesture = microbit.accelerometer.current_gesture()
    arcade.draw_text(f"gesture: {gesture}", 50, 50, arcade.color.BLACK, font_size=50)


if __name__ == '__main__':
    setup()
