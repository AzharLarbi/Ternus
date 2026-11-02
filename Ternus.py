import random
import expyriment as xpy

# Experiment initialization
e = xpy.design.Experiment(name="Ternus experiment")
e.data_variable_names = ["condition", "trial", "isi_ms", "frame_ms", "response", "group_response", "key", "rt_ms"]
xpy.control.initialize(e)

# Constants
SCREEN_SIZE = (600, 300)
Background_Color = (0, 0, 0)
Stimuli_color = (255, 255, 255)
Y_POS = -50

# Stimulus Factories
def circle():
    return xpy.stimuli.Circle(radius=20, colour=Stimuli_color)
def triangle():
    return xpy.stimuli.Shape(
        vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, 54),
        colour = Stimuli_color
    )
def rectangle():
    return xpy.stimuli.Rectangle(size=(35, 35), colour=Stimuli_color)

# Screen Configurations
screen_configs = [
    # DOTS stimuli (screen 1 and 2)
    ([-120, -40, 40], [circle, circle, circle]),
    ([-40, 40, 120], [circle, circle, circle]),
    # SHAPES stimuli (screen 3 and 4)
    ([-120, -40, 40], [circle, triangle, rectangle]),
    ([-40, 40, 120], [triangle, rectangle, circle])
]

# Generate Screens
screens = []
for x_coords, stim_factories in screen_configs:
    canvas = xpy.stimuli.Canvas(size=SCREEN_SIZE, colour=Background_Color)
    for x, factory in zip(x_coords, stim_factories):
        stim = factory()
        stim.position = (x, Y_POS)
        stim.plot(canvas)
    screens.append(canvas)

screen1, screen2, screen3, screen4 = screens


# Fixation cross and text screens
thing1 = xpy.stimuli.FixCross(size=(20, 20), line_width=4, colour=(255, 255, 255))
screen5 = xpy.stimuli.BlankScreen(colour=(0, 0, 0))
thing1.plot(screen5)
text1 = xpy.stimuli.TextScreen(heading="Ternus experiment", text="Keep your eyes on the central cross.\n\nLEFT = element motion\nRIGHT = group motion\n\nPress SPACE to start.")
text2 = xpy.stimuli.TextScreen(heading="What did you see?", text="LEFT = element motion\nRIGHT = group motion")
screen6 = xpy.stimuli.BlankScreen(colour=(0, 0, 0))

# Fixation on stimulus and text screens
stim_screens = [screen1, screen2, screen3, screen4, text1, text2]
for scr in stim_screens:
    thing1.plot(scr)

# Preloading
all_screens = [screen1, screen2, screen3, screen4, screen5, screen6, text1, text2]
for scr in all_screens:
    scr.preload()

# Define ISI values as a constant
ISI_VALUES = [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]

# Automatically build and randomize blocks using a loop
blocks = []
for name in ["DOTS", "SHAPES"]:
    b = xpy.design.Block(name=name)
    b.set_factor("condition", name)
    
    for v in ISI_VALUES:
        t = xpy.design.Trial()
        t.set_factor("isi_ms", v)
        b.add_trial(t)
        
    random.shuffle(b.trials)
    blocks.append(b)

b1, b2 = blocks

# screens that both blocks share
common_stimuli = [screen5, text2, screen5, screen6]

# Map each block to its unique first two screens
block_configurations = [
    (b1, [screen1, screen2]),
    (b2, [screen3, screen4])
]

# Assign stimuli  using iteration
for block, unique_screens in block_configurations:
    for t in block.trials:
        for s in unique_screens + common_stimuli:
            t.add_stimulus(s)

# Experiment start
e.add_block(b1)
e.add_block(b2)
xpy.control.start(skip_ready_screen=True)

# Counterbalancing
if e.subject % 2 == 0:
    e.blocks.reverse()

# Instructions
text1.present()
e.keyboard.wait(keys=[xpy.misc.constants.K_SPACE])

# Trial presentation
for b in e.blocks:
    for t in b.trials:
        v = t.get_factor("isi_ms")
        
        # Initial screen
        t.stimuli[2].present()
        e.clock.wait(200)

        # Ternus alternating frames (3 cycles)
        for _ in range(3):
            for stim in [t.stimuli[0], t.stimuli[1]]:
                stim.present()
                e.clock.wait(250)
                if v > 0:
                    t.stimuli[4].present() # ISI blank/cross screen
                    e.clock.wait(v)

        # Response collection
        t.stimuli[3].present()
        k, r = e.keyboard.wait(keys=[xpy.misc.constants.K_LEFT, xpy.misc.constants.K_RIGHT])

        # Map keyboard input using a dictionary lookup
        response_map = {
            xpy.misc.constants.K_LEFT: ("element", 0),
            xpy.misc.constants.K_RIGHT: ("group", 1)
        }
        a, g = response_map.get(k, ("unknown", -1))

        # Intertrial interval
        t.stimuli[5].present()
        e.clock.wait(500)
        
        # Data saving
        e.data.add([b.get_factor("condition"), t.id, v, 250, a, g, k, r])
        e.data.save()

# Experiment end
xpy.control.end()