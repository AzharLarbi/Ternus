import random
import expyriment as xpy

# Experiment initialization
e = xpy.design.Experiment(name="Ternus experiment", background_colour=(0, 0, 0), foreground_colour=(255, 255, 255))
e.data_variable_names = ["condition", "trial", "isi_ms", "frame_ms", "response", "group_response", "key", "rt_ms"]
xpy.control.initialize(e)

# DOTS stimuli
list1 = []
screen1 = xpy.stimuli.Canvas(size=(600, 300), colour=(0, 0, 0))
xpy.stimuli.Circle(radius=20, position=(-120, -50), colour=(255, 255, 255)).plot(screen1)
xpy.stimuli.Circle(radius=20, position=(-40, -50), colour=(255, 255, 255)).plot(screen1)
xpy.stimuli.Circle(radius=20, position=(40, -50), colour=(255, 255, 255)).plot(screen1)

screen2 = xpy.stimuli.Canvas(size=(600, 300), colour=(0, 0, 0))
xpy.stimuli.Circle(radius=20, position=(-40, -50), colour=(255, 255, 255)).plot(screen2)
xpy.stimuli.Circle(radius=20, position=(40, -50), colour=(255, 255, 255)).plot(screen2)
xpy.stimuli.Circle(radius=20, position=(120, -50), colour=(255, 255, 255)).plot(screen2)

# SHAPES stimuli
screen3 = xpy.stimuli.Canvas(size=(600, 300), colour=(0, 0, 0))
xpy.stimuli.Circle(radius=20, position=(-120, -50), colour=(255, 255, 255)).plot(screen3)
xpy.stimuli.Shape(vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, 54), position=(-40, -50), colour=(255, 255, 255)).plot(screen3)
xpy.stimuli.Rectangle(size=(35, 35), position=(40, -50), colour=(255, 255, 255)).plot(screen3)

screen4 = xpy.stimuli.Canvas(size=(600, 300), colour=(0, 0, 0))
xpy.stimuli.Shape(vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, 54), position=(-40, -50), colour=(255, 255, 255)).plot(screen4)
xpy.stimuli.Rectangle(size=(35, 35), position=(40, -50), colour=(255, 255, 255)).plot(screen4)
xpy.stimuli.Circle(radius=20, position=(120, -50), colour=(255, 255, 255)).plot(screen4)

# Fixation cross and text screens
thing1 = xpy.stimuli.FixCross(size=(20, 20), line_width=4, colour=(255, 255, 255))
screen5 = xpy.stimuli.BlankScreen(colour=(0, 0, 0))
thing1.plot(screen5)
text1 = xpy.stimuli.TextScreen(heading="Ternus experiment", text="Keep your eyes on the central cross.\n\nLEFT = element motion\nRIGHT = group motion\n\nPress SPACE to start.")
text2 = xpy.stimuli.TextScreen(heading="What did you see?", text="LEFT = element motion\nRIGHT = group motion")
screen6 = xpy.stimuli.BlankScreen(colour=(0, 0, 0))

# Fixation on stimulus and text screens
thing1.plot(screen1)
thing1.plot(screen2)
thing1.plot(screen3)
thing1.plot(screen4)
thing1.plot(text1)
thing1.plot(text2)

# Preloading
screen1.preload()
screen2.preload()
screen3.preload()
screen4.preload()
screen5.preload()
text1.preload()
text2.preload()
screen6.preload()

# DOTS block and trial construction
b1 = xpy.design.Block(name="DOTS")
b1.set_factor("condition", "DOTS")
for v in [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]:
    t = xpy.design.Trial()
    t.set_factor("isi_ms", v)
    b1.add_trial(t)

# Randomization of DOTS trials
for i in range(len(b1.trials) - 1, 0, -1):
    j = random.randint(0, i)
    b1.trials[i], b1.trials[j] = b1.trials[j], b1.trials[i]

# SHAPES block and trial construction
b2 = xpy.design.Block(name="SHAPES")
b2.set_factor("condition", "SHAPES")
for v in [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]:
    t = xpy.design.Trial()
    t.set_factor("isi_ms", v)
    b2.add_trial(t)

# Randomization of SHAPES trials
for i in range(len(b2.trials) - 1, 0, -1):
    j = random.randint(0, i)
    b2.trials[i], b2.trials[j] = b2.trials[j], b2.trials[i]

# Stimuli for DOTS trials
for t in b1.trials:
    t.add_stimulus(screen1)
    t.add_stimulus(screen2)
    t.add_stimulus(screen5)
    t.add_stimulus(text2)
    t.add_stimulus(screen5)
    t.add_stimulus(screen6)

# Stimuli for SHAPES trials
for t in b2.trials:
    t.add_stimulus(screen3)
    t.add_stimulus(screen4)
    t.add_stimulus(screen5)
    t.add_stimulus(text2)
    t.add_stimulus(screen5)
    t.add_stimulus(screen6)

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
        t.stimuli[2].present()
        e.clock.wait(200)

        for i in range(3):
            t.stimuli[0].present()
            e.clock.wait(250)
            if v > 0:
                t.stimuli[4].present()
                e.clock.wait(v)

            t.stimuli[1].present()
            e.clock.wait(250)
            if v > 0:
                t.stimuli[4].present()
                e.clock.wait(v)

        # Response collection
        t.stimuli[3].present()
        k, r = e.keyboard.wait(keys=[xpy.misc.constants.K_LEFT, xpy.misc.constants.K_RIGHT])

        if k == xpy.misc.constants.K_LEFT:
            a = "element"
            g = 0
        else:
            a = "group"
            g = 1

        # Intertrial interval
        t.stimuli[5].present()
        e.clock.wait(500)
        # Data saving
        e.data.add([b.get_factor("condition"), t.id, v, 250, a, g, k, r])
        e.data.save()

# Experiment end
xpy.control.end()