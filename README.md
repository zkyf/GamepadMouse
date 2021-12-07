# GamepadMouse
Control your mouse with gamepad

Only tested with Xbox One Controller

setting.json
```
{
    "mouse_x_axis": 0,    # idx of axis to control cursor x
    "mouse_y_axis": 1,    # idx of axis to control cursor y
    "scroll_x_axis": 2,   # idx of axis to control hscroll
    "scroll_y_axis": 3,   # idx of axis to control vscroll

    "move_speed": 2.0,    # speed of mouse panning
    "scroll_speed": 2.0,  # speed of scrolling

    "left_key": 0,        # btn for mouse left key
    "right_key": 1,       # btn for mouse right key
    "screen_keyboard": 2, # btn to open screen keyboard (ctrl + win + o)
    "esc": 3,             # btn for esc key
    "win_tab": 6,         # btn to switch window (win + tab)
    "win": 7              # btn to open start menu
}
```

To use screen keyboard, pls run as admin
