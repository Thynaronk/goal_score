/**
 * --- INITIAL SETUP ---
 */
// --- RESET BUTTON ---
// Press Button A to clear the score
input.onButtonPressed(Button.A, function () {
    score = 0
    basic.showNumber(score)
    basic.pause(500)
    basic.clearScreen()
})
let score = 0
// 1. Initialize the goalkeeper at the 90-degree center position on start
pins.servoWritePin(AnalogPin.P1, 90)
// 2. Fix the scoreboard: Force Pin 16 to stay HIGH (fixes constant scoring)
pins.setPull(DigitalPin.P16, PinPullMode.PullUp)
// 3. Show a happy face to confirm the code has started correctly
basic.showIcon(IconNames.Happy)
basic.pause(500)
basic.clearScreen()
// --- MAIN GAME LOOP ---
// Very fast loop for high responsiveness
basic.forever(function () {
    // 4. SCOREBOARD (Pin 16 + GND)
    // 0 means ball hit the foil target
    if (pins.digitalReadPin(DigitalPin.P16) == 0) {
        score += 1
        music.playTone(262, music.beat(BeatFraction.Whole))
        // Goal sound
        // Flashing LED celebration
        for (let index = 0; index < 2; index++) {
            basic.showIcon(IconNames.Square)
            basic.pause(100)
            basic.clearScreen()
            basic.pause(100)
        }
        basic.showNumber(score)
        basic.pause(1000)
    }
    // Debounce: wait to avoid double-points
    // 5. GOALKEEPER (IR Sensor on Pin 2)
    // Detects ball approaching the goal
    if (pins.digitalReadPin(DigitalPin.P2) == 0) {
        // Move at maximum speed: Full sweep from 0 to 180 degrees
        // No more random: always dives across the entire goal
        pins.servoWritePin(AnalogPin.P1, 0)
        // Sweep to far left
        basic.pause(250)
        // Short pause for hardware to reach 0
        pins.servoWritePin(AnalogPin.P1, 180)
        // Sweep to far right
        basic.pause(400)
        // Wait for full 180-degree move
        // Return to 90 degrees center
        pins.servoWritePin(AnalogPin.P1, 90)
        basic.pause(400)
    } else {
        // Wait to finish returning to center
        // If no ball is detected, ensure motor is stopped at 90 degrees
        pins.servoWritePin(AnalogPin.P1, 90)
    }
    basic.pause(50)
})
