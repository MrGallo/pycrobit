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

    new_x = utils.map_value(microbit.accelerometer.get_x(), -1000, 1000, 0, WIDTH)
    new_y = utils.map_value(microbit.accelerometer.get_y(), -1000, 1000, HEIGHT, 0)

    if microbit.button_a.was_pressed():
        print("hello")

    if abs(new_x - player_x) > 15:
        player_x = new_x
    if abs(new_y - player_y) > 15:
        player_y = new_y


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
