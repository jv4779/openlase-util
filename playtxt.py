
import pylase as ol

import sys

if len(sys.argv) <=1:
    print(sys.argv[0]+" <banner_text> <ilda_txt_file> [command_string]")
    print("  command_string:")
    print("      \"repeat <count>\" \"start <frame_number>\" \"end <frame_number>\"")
    print("  example:")
    print("      "+sys.argv[0]+" \"\" animation.txt")
    print("      "+sys.argv[0]+" \"Title\" frame.txt \"repeat 60\"")
    print("      "+sys.argv[0]+" \"Title\" background.txt \"repeat 2 start 1 end 60\"")
    sys.exit(1)

banner = sys.argv[1]
ildTxtFilename = sys.argv[2]
if len(sys.argv) > 3:
    command = sys.argv[3]
else:
    command = ""

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def pairs(lst):
    return zip(lst[0::2], lst[1::2])

if ol.init(10) < 0:
    sys.exit(1)

params = ol.RenderParams()
params.rate = 48000;
params.start_wait = 4
params.start_dwell = 2
params.curve_dwell = 1
params.corner_dwell = 2
params.end_dwell = 4
params.end_wait = 2
ol.setRenderParams(params)


if banner != "":
    font = ol.getDefaultFont()
    fsize = 10000.0
    yoff = (1/2.0) * fsize
    w = ol.getStringWidth(font, fsize, banner)

repeatCount = 1
startFrame = 1
endFrame = -1

for token in pairs(command.split()):
    if token[0] == 'repeat':
        repeatCount = int(token[1])
    elif token[0] == 'start':
        startFrame = int(token[1])
    elif token[0] == 'end':
        endFrame = int(token[1])

openPath = False
renderFrame = False

def render_frame():
    global renderFrame
    global openPath

    if renderFrame:
        if openPath:
            ol.end()
            openPath = False
        ol.renderFrame(30)
    renderFrame = False

for count in range(repeatCount):
    currentFrame = 0
    with open(ildTxtFilename,"r") as f:
        for line in f:
            tokens = line.split()
    
            #print tokens

            if len(tokens) < 1:
                continue
    
            if tokens[0] == "palette":
                render_frame()
                continue

            if tokens[0] == "frame":
                render_frame()

                currentFrame += 1
                if currentFrame >= startFrame:
                    if endFrame > 0 and currentFrame > endFrame:
                        break
                    renderFrame = True
                    openPath = False
                    ol.loadIdentity()
                    ol.scale((1.0/32768, 1.0/32768))
                    ol.translate((0, 0))
                    if banner != "":
                        ol.drawString(font, (-w/2,yoff), fsize, ol.C_GREEN, banner)
                continue

            if is_number(tokens[0]):
                if renderFrame:
                    x = float(tokens[0])
                    y = float(tokens[1])
                    palette_i = int(tokens[2])
    
                    if not openPath:
                        ol.begin(0)
                        openPath = True
                    elif palette_i < 0:
                        ol.end()
                        ol.begin(0)
                        openPath = True

                    ol.vertex((x,y),ol.C_RED)
                    continue

    render_frame()

ol.shutdown()

