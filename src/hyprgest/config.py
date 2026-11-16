from hyprgest.models import Gesture

COMMANDS = {
    Gesture.SWIPE_LEFT: 'dispatch hl.dsp.focus({ workspace = "e-1" })',
    Gesture.SWIPE_RIGHT: 'dispatch hl.dsp.focus({ workspace = "e+1" })',
}
