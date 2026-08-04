"""

--- INITIAL SETUP ---

"""
# --- RESET BUTTON ---
# Press Button A to clear the score

def on_button_pressed_a():
    global score
    score = 0
    basic.show_number(score)
    basic.pause(500)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)

score = 0
# 1. Initialize the goalkeeper at the 90-degree center position on start
pins.servo_write_pin(AnalogPin.P1, 90)
# 2. Fix the scoreboard: Force Pin 16 to stay HIGH (fixes constant scoring)
pins.set_pull(DigitalPin.P16, PinPullMode.PULL_UP)
# 3. Show a happy face to confirm the code has started correctly
basic.show_icon(IconNames.HAPPY)
basic.pause(500)
basic.clear_screen()
# --- MAIN GAME LOOP ---
# Very fast loop for high responsiveness

def on_forever():
    global score
    # 4. SCOREBOARD (Pin 16 + GND)
    # 0 means ball hit the foil target
    if pins.digital_read_pin(DigitalPin.P16) == 0:
        score += 1
        music.play_tone(262, music.beat(BeatFraction.WHOLE))
        # Goal sound
        # Flashing LED celebration
        for index in range(2):
            basic.show_icon(IconNames.SQUARE)
            basic.pause(100)
            basic.clear_screen()
            basic.pause(100)
        basic.show_number(score)
        basic.pause(1000)
    # Debounce: wait to avoid double-points
    # 5. GOALKEEPER (IR Sensor on Pin 2)
    # Detects ball approaching the goal
    if pins.digital_read_pin(DigitalPin.P2) == 0:
        # Move at maximum speed: Full sweep from 0 to 180 degrees
        # No more random: always dives across the entire goal
        pins.servo_write_pin(AnalogPin.P1, 0)
        # Sweep to far left
        basic.pause(250)
        # Short pause for hardware to reach 0
        pins.servo_write_pin(AnalogPin.P1, 180)
        # Sweep to far right
        basic.pause(400)
        # Wait for full 180-degree move
        # Return to 90 degrees center
        pins.servo_write_pin(AnalogPin.P1, 90)
        basic.pause(400)
    else:
        # Wait to finish returning to center
        # If no ball is detected, ensure motor is stopped at 90 degrees
        pins.servo_write_pin(AnalogPin.P1, 90)
    basic.pause(50)
basic.forever(on_forever)
