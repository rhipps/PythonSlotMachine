import Tkinter as tkinter
from PIL import Image, ImageTk

#######################################################################
#                       Startup Game Configuration                    #
#######################################################################

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Configure the game for play
slotMachineConfig = open("slotmachineconfig", "r")

GAME_THEME = slotMachineConfig.readline().strip()
START_IN_FULLSCREEN = slotMachineConfig.readline().strip()
JACKPOT_VALUE = slotMachineConfig.readline().strip()

if GAME_THEME == "":
    GAME_THEME = "default"

GAME_THEME = "themes/" + GAME_THEME

#######################################################################
#                       Function Definitions                          #
#######################################################################


def toggle_fullscreen(event):
    if window.attributes("-fullscreen"):
        window.attributes("-fullscreen", False)
    else:
        window.attributes("-fullscreen", True)


def shift_slot_tiles(param_slot_wheel_canvas, param_slot_wheel_tiles, param_min_tile_index, param_max_tile_index):

    global TILE_HEIGHT

    for tile_index in xrange(param_min_tile_index, param_max_tile_index):
        slot_wheel_tile = param_slot_wheel_tiles[tile_index]
        slot_tile_y_coord = param_slot_wheel_canvas.coords(slot_wheel_tile)[1]

        for row_index in xrange(0, ROW_COUNT + 1):

            stop_point = TILE_HEIGHT * row_index

            if slot_tile_y_coord < stop_point:
                param_slot_wheel_canvas.coords(slot_wheel_tile, (0, stop_point))
                if param_slot_wheel_canvas.coords(slot_wheel_tile)[1] >= window_resize_height:
                    param_slot_wheel_canvas.coords(slot_wheel_tile, (0, 0))
                break


def finish_spin(param_slot_wheel_canvas, param_slot_wheel_tiles, slot_wheel_canvas_index):

    min_tile_index = ROW_COUNT * slot_wheel_canvas_index
    max_tile_index = ROW_COUNT + ROW_COUNT * slot_wheel_canvas_index

    shift_slot_tiles(param_slot_wheel_canvas, param_slot_wheel_tiles, min_tile_index, max_tile_index)


def action_button(event):

    global slot_wheel_is_spinning
    global slot_wheel_images
    global slot_wheel_canvases
    global slot_wheel_tiles
    global window_resize_height

    if True in slot_wheel_is_spinning:
        for index, slot_wheel_status in enumerate(slot_wheel_is_spinning):
            if slot_wheel_is_spinning[index]:
                slot_wheel_is_spinning[index] = False
                finish_spin(slot_wheel_canvases[index], slot_wheel_tiles, index)
                for tile_index in xrange(0, ROW_COUNT):
                    position = int(slot_wheel_canvases[index].coords(slot_wheel_tiles[tile_index])[1] / (window_resize_height / ROW_COUNT))
                    slot_tile_scoring_positions[index*ROW_COUNT + position] = slot_wheel_configuration[index*ROW_COUNT + tile_index]
                if index == COLUMN_COUNT-1:
                    score_game()
                return
    else:
        for index, slot_wheel_status in enumerate(slot_wheel_is_spinning):
            slot_wheel_is_spinning[index] = True


def get_slot_machine_state():

    global ROW_COUNT
    global COLUMN_COUNT

    slot_machine_state = [""] * ROW_COUNT
    for score_index in xrange(0, ROW_COUNT):
        slot_row = ""
        for column_index in xrange(0, COLUMN_COUNT):
            slot_row = "%s %s" % (slot_row, str(slot_tile_scoring_positions[score_index + ROW_COUNT*column_index]))
        slot_machine_state[score_index] = slot_row

    return slot_machine_state


def score_game():

    global JACKPOT_VALUE
    cash_out = 0
    jackpot_winner = False
    jackpot = "1 1 1 1 1"
    tier_one_payout = ["3 3 3", "4 4 4"]
    tier_two_payout = ["3 3 3 3", "4 4 4 4"]
    tier_three_payout = ["3 3 3 3 3", "4 4 4 4 4"]
    double_tier_one_payout = ["2 2 2"]
    double_tier_two_payout = ["2 2 2 2"]

    final_state = get_slot_machine_state()
    for score_row in final_state:
        found_winning_payout = False
        if jackpot in score_row:
            jackpot_winner = True
            found_winning_payout = True
            cash_out = JACKPOT_VALUE
            break
        if any(tier_three_value in score_row for tier_three_value in tier_three_payout) and not found_winning_payout:
            cash_out += 25
            found_winning_payout = True
        if any(tier_two_value in score_row for tier_two_value in tier_two_payout) and not found_winning_payout:
            cash_out += 10
            found_winning_payout = True
        if any(tier_one_value in score_row for tier_one_value in tier_one_payout) and not found_winning_payout:
            cash_out += 5
            found_winning_payout = True
        if any(double_tier_two_value in score_row for double_tier_two_value in double_tier_two_payout) and not found_winning_payout:
            cash_out += 20
            found_winning_payout = True
        if any(double_tier_one_value in score_row for double_tier_one_value in double_tier_one_payout) and not found_winning_payout:
            cash_out += 10
            found_winning_payout = True

    print cash_out
#######################################################################
#                       WINDOW Details                                #
#######################################################################

window = tkinter.Tk()
window.title("Slot Machine")
window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
window.configure(background="black")
window.attributes("-fullscreen", START_IN_FULLSCREEN)

#Control bindings
window.bind("<Escape>", toggle_fullscreen)
window.bind("<space>", action_button)

#Slot machine window layout
window.rowconfigure(0, weight=1, uniform="rows")
window.columnconfigure(0, weight=1, uniform="columns")
window.columnconfigure(1, weight=1, uniform="columns")
window.columnconfigure(2, weight=1, uniform="columns")
window.columnconfigure(3, weight=1, uniform="columns")
window.columnconfigure(4, weight=1, uniform="columns")
window.columnconfigure(5, weight=1, uniform="columns")
window.columnconfigure(6, weight=1, uniform="columns")

#######################################################################
#                Constants and System Variables                       #
#######################################################################

COLUMN_COUNT = 5
ROW_COUNT = 4

slot_machine_spinning = True
slot_wheel_is_spinning = [False] * COLUMN_COUNT
slot_wheel_canvases = [None] * COLUMN_COUNT
slot_wheel_images = [None] * COLUMN_COUNT * ROW_COUNT
slot_wheel_tiles = [None] * COLUMN_COUNT * ROW_COUNT
slot_wheel_configuration = [1, 2, 3, 4, 1, 4, 2, 3, 1, 4, 3, 2, 1, 2, 3, 4, 1, 3, 4, 3]
slot_tile_scoring_positions = list(slot_wheel_configuration)

if START_IN_FULLSCREEN:
    window_resize_width = window.winfo_screenwidth()
    window_resize_height = window.winfo_screenheight()
else:
    window_resize_width = WINDOW_WIDTH
    window_resize_height = WINDOW_HEIGHT

TILE_HEIGHT = window_resize_height / ROW_COUNT
#######################################################################
#                       Slot Wheel Setup                              #
#######################################################################

for index, image in enumerate(slot_wheel_images):
    slot_wheel_images[index] = Image.open(GAME_THEME + "/slotImg" + str(slot_wheel_configuration[index]) + ".png")

for index, image in enumerate(slot_wheel_images):
    slot_wheel_images[index] = ImageTk.PhotoImage(image.resize((window_resize_width/(COLUMN_COUNT+2), window_resize_height/ROW_COUNT), Image.ANTIALIAS))

for index, wheel in enumerate(slot_wheel_canvases):
    slot_wheel_canvases[index] = tkinter.Canvas(window)
    for image_index in xrange(0, ROW_COUNT):
        slot_wheel_image = slot_wheel_images[index*ROW_COUNT + image_index]
        x_coord = 0
        y_coord = slot_wheel_image.height()*image_index
        slot_wheel_tiles[index*ROW_COUNT + image_index] = slot_wheel_canvases[index].create_image(x_coord, y_coord, image=slot_wheel_image, anchor="nw")

    slot_wheel_canvases[index].grid(row=0, column=index + 1, sticky="nsew")


#######################################################################
#                       Start of Game Loop                            #
#  slot_wheel_canvas - list of canvas that slot images are drawn on   #
#               equal to COLUMN_COUNT                                 #
#                                                                     #
#  slot_wheel_is_spinning - list of spinning state of each wheel      #
#                           that is also listed in slot_wheel         #
#######################################################################

while True:

    # Check the state of the slot wheels
    if True in slot_wheel_is_spinning:
        slot_machine_spinning = True
    else:
        slot_machine_spinning = False

    # Go through each slot wheel and tile and move accordingly
    if slot_machine_spinning:
        for slot_wheel_canvas_index, slot_wheel_canvas in enumerate(slot_wheel_canvases):
            if slot_wheel_is_spinning[slot_wheel_canvas_index]:
                min_tile_index = ROW_COUNT * slot_wheel_canvas_index
                max_tile_index = ROW_COUNT + ROW_COUNT * slot_wheel_canvas_index
                shift_slot_tiles(slot_wheel_canvas, slot_wheel_tiles, min_tile_index, max_tile_index)

    window.update()
