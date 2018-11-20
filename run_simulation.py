# Converted from Ben's ipython script
import numpy as np
import pandas as pd
import pyautogui as mouse
import time
from scipy import interpolate
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os
#  import time as clock

# Running constants
mouse_delay = 0
images = 'C:\\Users\\gotwa\\Desktop\\PARALLAX\\AutoGuiImages\\'
data_folder = 'C:\\Users\\gotwa\\Documents\\RASAero II\\'

atmo_data = pd.read_csv('atmo_data.csv')
thrust_curve = pd.read_csv('Valkyrie_Thrust_Curve.csv')

engine_len = 10
unstable_score = 100000

# Define physical constants
g = 9.80665         # [SI]
O2_flow = 0.9825    # [kg/s]
CH4_flow = 0.3275   # [kg/s]
O2_rho = 1141.      # [SI]
CH4_rho = 442.62    # [SI]

density = interpolate.interp1d(np.array(atmo_data['height(m)']),
                               np.array(atmo_data[' Density(kg/meter^3)']))
mach1 = interpolate.interp1d(np.array(atmo_data['height(m)']), np.array(
                                 atmo_data['Speed of Sound (meters/second)']))


def make_nosecone(base_di, length, tip_di, shape, power):
    '''
    Inputs: diameter of the base of the nosecone (in), length of the
    nosecone (in), diameter of the tip of the nosecone (in), shape of
    the nosecone (numer 1-7, see below), power of the power law, should
    that be the shape (float 0-1)

    Shape key:
    1 = Conical
    2 = Tangent Ogive
    3 = Von Karman Ogive
    4 = Power Law
    5 = LV-Haack
    6 = Parabolic
    7 = Elliptical
    '''
    # Open the nosecone window
    mouse.moveTo(add_nose[0], add_nose[1], duration=mouse_delay)
    mouse.doubleClick()

    # Input the base diameter
    mouse.moveTo(nose_di[0], nose_di[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(base_di))

    # Input the length
    mouse.moveTo(nose_len[0], nose_len[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(length))

    # Input the tip diameter
    mouse.moveTo(nose_tip[0], nose_tip[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(tip_di))

    # Select the shape
    mouse.moveTo(nose_shape_drop_down[0], nose_shape_drop_down[1],
                 duration=mouse_delay)
    mouse.click()
    if shape is 1:
        coords = nose_conical
    elif shape is 2:
        coords = nose_tangent_ogive
    elif shape is 3:
        coords = nose_von_karman_ogive
    elif shape is 4:
        coords = nose_power_law
    elif shape is 5:
        coords = nose_LV_Haack
    elif shape is 6:
        coords = nose_parabolic
    else:
        coords = nose_elliptical

    mouse.moveTo(coords[0], coords[1], duration=mouse_delay)
    mouse.click()

    if shape is 4:
        mouse.moveTo(nose_power_law_input[0], nose_power_law_input[1])
        mouse.doubleClick()
        mouse.typewrite(str(power))

    # Finish the nosecone
    mouse.moveTo(finish_nose[0], finish_nose[1], duration=mouse_delay)
    mouse.click()


def make_body_fins(length, count, root_chord, span, tip_chord, sweep,
                   thickness, bottom_sep, shape, le_len, te_len, le_radius):
    # Open the body/fins window
    mouse.moveTo(add_body[0], add_body[1], duration=mouse_delay)
    mouse.doubleClick()

    # Set length of body
    mouse.moveTo(body_len[0], body_len[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(length))

    # Open the fin window
    mouse.moveTo(open_fin_window[0], open_fin_window[1], duration=mouse_delay)
    mouse.doubleClick()

    # Set fin count
    mouse.moveTo(fin_count[0], fin_count[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(count))

    # Set root chord
    mouse.moveTo(fin_root_chord[0], fin_root_chord[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(root_chord))

    # Set span
    mouse.moveTo(fin_span[0], fin_span[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(span))

    # Set tip chord
    mouse.moveTo(fin_tip_chord[0], fin_tip_chord[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(tip_chord))

    # Set sweep
    mouse.moveTo(fin_sweep[0], fin_sweep[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(sweep))

    # Set thickness
    mouse.moveTo(fin_thickness[0], fin_thickness[1], duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(thickness))

    # Set bottom offset
    mouse.moveTo(fin_dist_tube_bottom[0], fin_dist_tube_bottom[1],
                 duration=mouse_delay)
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite(str(bottom_sep))

    # Select the shape
    # Right now only doing subsonic NACA, rounded, square
    mouse.moveTo(fin_shape_drop_down[0], fin_shape_drop_down[1],
                 duration=mouse_delay)
    mouse.click()

    shapes = [fin_hexagonal, fin_subsonic_NACA, fin_double_wedge,
              fin_biconvex, fin_single_wedge, fin_hexagonal_blunt_base,
              fin_rounded, fin_square]
    coords = shapes[shape-1]

    mouse.moveTo(coords[0], coords[1], duration=mouse_delay)
    mouse.click()

    if shape in [1, 3, 6]:
        mouse.moveTo(fin_le_diamond_airfoil_len)
        mouse.doubleClick()
        mouse.typewrite(str(le_len))

    if shape is 1:
        mouse.moveTo(fin_te_diamond_airfoil_len)
        mouse.doubleClick()
        mouse.typewrite(str(te_len))

    if shape in [1, 3, 4, 5, 6, 7]:
        mouse.moveTo(fin_le_radius)
        mouse.doubleClick()
        mouse.typewrite(str(le_radius))

    # Finish the fins
    mouse.moveTo(finish_fin[0], finish_fin[1], duration=mouse_delay)
    mouse.click()

    # Finish the body
    mouse.moveTo(finish_body[0], finish_body[1], duration=mouse_delay)
    mouse.click()


def make_boat_tail(length):
    # Open the boat tail window
    mouse.moveTo(add_boat)
    mouse.click()

    # Tab over to the length window
    mouse.hotkey('tab')
    mouse.typewrite(str(length))

    # Set the exit diamater. Right now just set to 6"
    mouse.hotkey('tab')
    mouse.typewrite('6')

    # Tab over to the add option. We are not allowing boat fins.
    # Add the boat
    mouse.hotkey('tab')
    mouse.hotkey('tab')
    mouse.hotkey('enter')


def find_nose_buttons():
    add_nose = list(mouse.locateCenterOnScreen(images+'add_nose.png'))
    mouse.moveTo(add_nose[0], add_nose[1], duration=.3)
    mouse.doubleClick()
    time.sleep(0.5)
    nose_di = list(mouse.locateCenterOnScreen(images+'nose_di.png'))
    nose_di[0] = nose_di[0] + 50
    nose_len = [nose_di[0], nose_di[1]+45]
    nose_tip = [nose_di[0], nose_di[1]+90]
    nose_power_law_input = [nose_tip[0], nose_tip[1]+60]

    nose_shape_drop_down = [nose_di[0]+335, nose_di[1]]
    nose_conical = [nose_shape_drop_down[0], nose_shape_drop_down[1]+40]
    nose_tangent_ogive = [nose_shape_drop_down[0], nose_shape_drop_down[1]+65]
    nose_von_karman_ogive = [nose_shape_drop_down[0],
                             nose_shape_drop_down[1]+90]
    nose_power_law = [nose_shape_drop_down[0], nose_shape_drop_down[1]+115]
    nose_LV_Haack = [nose_shape_drop_down[0], nose_shape_drop_down[1]+140]
    nose_parabolic = [nose_shape_drop_down[0], nose_shape_drop_down[1]+165]
    nose_elliptical = [nose_shape_drop_down[0], nose_shape_drop_down[1]+200]

    finish_nose = [nose_shape_drop_down[0]-360, nose_shape_drop_down[1]+330]

    # Cancel the nosecone window
    mouse.hotkey('enter')

    return [add_nose, nose_di, nose_len, nose_tip, nose_power_law_input,
            nose_shape_drop_down, nose_conical, nose_tangent_ogive,
            nose_von_karman_ogive, nose_power_law, nose_LV_Haack,
            nose_parabolic, nose_elliptical, finish_nose]


def find_body_fins_buttons():
    add_body = list(mouse.locateCenterOnScreen(images+'add_body.png'))
    mouse.moveTo(add_body[0], add_body[1], duration=.3)
    mouse.doubleClick()

    time.sleep(0.8)  # give the window time to open
    body_len = list(mouse.locateCenterOnScreen(images+'body_len.png',
                                               grayscale=True))
    body_len[0] = body_len[0] + 50
    mouse.moveTo(body_len[0], body_len[1])
    mouse.doubleClick()
    mouse.hotkey('del')
    mouse.typewrite('38')  # random value to illuminate fin window

    open_fin_window = [body_len[0]-120, body_len[1]+100]
    mouse.moveTo(open_fin_window[0], open_fin_window[1], duration=.3)
    mouse.doubleClick()

    time.sleep(0.8)  # give the window time to open
    fin_count = list(mouse.locateCenterOnScreen(images+'fin_count.png',
                                                grayscale=True))
    fin_count[0] = fin_count[0] + 100

    fin_root_chord = fin_count[0], fin_count[1]+50
    mouse.moveTo(fin_root_chord[0], fin_root_chord[1])
    mouse.doubleClick()
    mouse.typewrite('15')

    fin_span = [fin_count[0], fin_count[1]+95]
    mouse.moveTo(fin_span[0], fin_span[1])
    mouse.doubleClick()
    mouse.typewrite('15')

    fin_tip_chord = [fin_count[0], fin_count[1]+140]
    mouse.moveTo(fin_tip_chord[0], fin_tip_chord[1])
    mouse.doubleClick()
    mouse.typewrite('12')

    fin_sweep = [fin_count[0], fin_count[1]+188]
    mouse.moveTo(fin_sweep[0], fin_sweep[1])
    mouse.doubleClick()
    mouse.typewrite('4')

    fin_thickness = [fin_count[0], fin_count[1]+235]
    mouse.moveTo(fin_thickness[0], fin_thickness[1])
    mouse.doubleClick()
    mouse.typewrite('0.125')

    fin_dist_tube_bottom = [fin_count[0], fin_count[1]+278]
    mouse.moveTo(fin_dist_tube_bottom[0], fin_dist_tube_bottom[1])
    mouse.doubleClick()
    mouse.typewrite('15')

    fin_shape_drop_down = [fin_count[0]+105, fin_count[1]+340]
    mouse.moveTo(fin_shape_drop_down[0], fin_shape_drop_down[1])
    mouse.click()

    fin_subsonic_NACA = [fin_count[0]+105, fin_count[1]+405]
    mouse.moveTo(fin_subsonic_NACA[0], fin_subsonic_NACA[1])
    mouse.click()
    fin_rounded = [fin_count[0]+105, fin_count[1]+535]
    fin_square = [fin_count[0]+105, fin_count[1]+565]

    # Other fin shapes
    fin_hexagonal = [fin_subsonic_NACA[0], fin_subsonic_NACA[1]-30]
    fin_double_wedge = [fin_subsonic_NACA[0], fin_subsonic_NACA[1]+25]
    fin_biconvex = [fin_subsonic_NACA[0], fin_subsonic_NACA[1]+55]
    fin_single_wedge = [fin_subsonic_NACA[0], fin_subsonic_NACA[1]+80]
    fin_hexagonal_blunt_base = [fin_subsonic_NACA[0], fin_subsonic_NACA[1]+100]

    # Parameters for certain shapes
    fin_le_diamond_airfoil_len = [fin_dist_tube_bottom[0],
                                  fin_dist_tube_bottom[1]+125]
    fin_te_diamond_airfoil_len = [fin_dist_tube_bottom[0],
                                  fin_dist_tube_bottom[1]+185]
    fin_le_radius = [fin_dist_tube_bottom[0], fin_dist_tube_bottom[1]+230]

    finish_fin = [fin_count[0] + 285, fin_count[1] + 525]

    # Move over to cancel and click to close fin
    for i in range(8):
        mouse.hotkey('tab')
    mouse.hotkey('enter')

    finish_body = [body_len[0], body_len[1]+300]
    mouse.moveTo(finish_body[0], finish_body[1])
    mouse.click()  # Add the body section

    return [add_body, body_len, open_fin_window, fin_count, fin_root_chord,
            fin_span, fin_tip_chord, fin_sweep, fin_thickness,
            fin_dist_tube_bottom, fin_shape_drop_down, fin_subsonic_NACA,
            fin_rounded, fin_square, fin_hexagonal, fin_double_wedge,
            fin_biconvex, fin_single_wedge, fin_hexagonal_blunt_base,
            fin_le_diamond_airfoil_len, fin_te_diamond_airfoil_len,
            fin_le_radius, finish_fin, finish_body]


def find_aero_plot_buttons():
    aero_reference = list(mouse.locateCenterOnScreen(images+'aero_plots.png'))
    aero_reference[0] = aero_reference[0]+350
    aero_reference[1] = aero_reference[1]+500
    aero_file = [aero_reference[0]-865, aero_reference[1]-560]
    mouse.moveTo(aero_file[0], aero_file[1], duration=.5)
    aero_export = [aero_reference[0]-690, aero_reference[1]-630]
    aero_to_CSV = [aero_reference[0]-350, aero_reference[1]-630]
    return [aero_reference, aero_file, aero_export, aero_to_CSV]


def find_flight_sim_buttons():
    mouse.moveTo(flight_simulation_button[0], flight_simulation_button[1])
    mouse.doubleClick()
    time.sleep(3)

    engine = list(mouse.locateCenterOnScreen(images+'flight_sim_ref.png'))

    mouse.moveTo(engine[0], engine[1])
    mouse.doubleClick()
    time.sleep(0.1)
    mouse.hotkey('down')
    mouse.hotkey('tab')
    mouse.typewrite('15')
    mouse.hotkey('tab')
    mouse.typewrite('4')
    mouse.hotkey('tab')
    mouse.typewrite('50')
    for i in range(16):
        mouse.hotkey('tab')
    mouse.hotkey('enter')

    view_flight_data = [engine[0]+1500, engine[1]]
    mouse.moveTo(view_flight_data[0], view_flight_data[1])
    mouse.click()
    time.sleep(1)

    stability_ref = list(
        mouse.locateCenterOnScreen(images+'stability_ref.png'))
    close_stability_warning = [stability_ref[0]+1150, stability_ref[1]-120]
    mouse.moveTo(close_stability_warning[0], close_stability_warning[1])

    mouse.click()
    time.sleep(3)
    flight_data_ref = list(
        mouse.locateCenterOnScreen(images+'flight_data_ref.png'))
    flight_data_file_button = [flight_data_ref[0], flight_data_ref[1]-50]
    mouse.moveTo(flight_data_file_button[0], flight_data_file_button[1])
    export_flight = [flight_data_file_button[0], flight_data_file_button[1]+25]
    flight_to_csv = [export_flight[0]+250, export_flight[1]]

    close_flight_sim = [flight_data_file_button[0]+1800,
                        flight_data_file_button[1]-50]
    mouse.moveTo(close_flight_sim[0], close_flight_sim[1])
    mouse.click()

    return [engine, view_flight_data, stability_ref, close_stability_warning,
            flight_data_ref, flight_data_file_button, export_flight,
            flight_to_csv, close_flight_sim]


# SYSTEM SETUP
# Nosecone buttons
[add_nose, nose_di, nose_len, nose_tip, nose_power_law_input,
 nose_shape_drop_down, nose_conical, nose_tangent_ogive, nose_von_karman_ogive,
 nose_power_law, nose_LV_Haack, nose_parabolic, nose_elliptical,
 finish_nose] = find_nose_buttons()

make_nosecone(12, 12, 0, 2, .5)

# Body and fin buttons
[add_body, body_len, open_fin_window, fin_count, fin_root_chord, fin_span,
 fin_tip_chord, fin_sweep, fin_thickness, fin_dist_tube_bottom,
 fin_shape_drop_down, fin_subsonic_NACA, fin_rounded, fin_square,
 fin_hexagonal, fin_double_wedge, fin_biconvex, fin_single_wedge,
 fin_hexagonal_blunt_base, fin_le_diamond_airfoil_len,
 fin_te_diamond_airfoil_len, fin_le_radius, finish_fin,
 finish_body] = find_body_fins_buttons()

# Boat tail button. Everything besides opening the window can
# be done with tabbing/the fin window buttons
add_boat = list(mouse.locateCenterOnScreen(images+'add_boat.png'))

# General window buttons
file_button = [add_nose[0]-20, add_nose[1]-55]
new_rocket = [add_nose[0]-20, add_nose[1]-10]
aero_plots_button = [add_nose[0]+630, add_nose[1]]
flight_simulation_button = [add_nose[0]+800, add_nose[1]]

# Aero plot buttons
mouse.moveTo(aero_plots_button[0], aero_plots_button[1], duration=0.3)
mouse.doubleClick()
time.sleep(3)
[aero_reference, aero_file, aero_export, aero_to_CSV] = \
    find_aero_plot_buttons()
mouse.moveTo(aero_file[0]+1280, aero_file[1]-50, duration=.3)  # close window
mouse.click()

# Flight sim buttons
[engine, view_flight_data, stability_ref, close_stability_warning,
 flight_data_ref, flight_data_file_button, export_flight, flight_to_csv,
 close_flight_sim] = find_flight_sim_buttons()

close_flight_setup = [engine[0]+1750, engine[1]-180]
mouse.moveTo(close_flight_setup[0], close_flight_setup[1])
mouse.click()
mouse.hotkey('enter')

mouse.moveTo(file_button[0], file_button[1])
mouse.click()
time.sleep(.3)

mouse.moveTo(new_rocket[0], new_rocket[1])
mouse.click()
time.sleep(0)
mouse.hotkey('left')
mouse.hotkey('enter')


# In[102]:

def make_rocket(radius, wet_weight, nose_len, body_len, boat_len, cg_loc,
                nose_shape, nose_tip_di, nose_power, fin_count, fin_root_chord,
                fin_span, fin_tip_chord, fin_sweep, fin_thickness,
                fin_base_sep, fin_shape, fin_le_rad, fin_le_len, fin_te_len,
                name):
    '''
    Given input parameters, generate the needed csv files for the
    rest of PARALLAX to analyze it. The inputs are:
    1) Rocket radius (in)
    2) Wet weight (lbs)
    3) Nosecone len (in)
    4) Body len (in)
    5) Boat len (in)
    6) Cg loc (in from tip)

    7) Nosecone shape (integer 1-7, see make_nosecone)
    8) Nosecone tip diameter (in)
    9) Nosecone power (float 0-1, only for shape 4)

    10) Number of fins (integer > 3)
    11) Fin root chord length (in)
    12) Fin span (in)
    13) Fin tip chord length (in)
    14) Fin sweep distance (in)
    15) Fin thickness (in)
    16) Fin separation from base (in)

    17) Fin shape (integer 1-9, see make_body_fins)
    18) Fin LE radius (in, only for shapes 1, 3, 4, 5, 6, 7)
    19) Fin LE airfoil length (in, only for shapes 1, 3, 6)
    20) Fin TE airfoil length (in, only for shape 1)
    '''

    if os.path.exists(data_folder + 'CD_' + name + '.csv'):
        print('The combination ' + name + ' has already been simulated')
        return

    make_nosecone(radius, nose_len, nose_tip_di, nose_shape, nose_power)

    make_body_fins(body_len, fin_count, fin_root_chord, fin_span,
                   fin_tip_chord, fin_sweep, fin_thickness, fin_base_sep,
                   fin_shape, fin_le_len, fin_te_len, fin_le_rad)

    if boat_len is not 0:
        make_boat_tail(boat_len)

    def get_aero_csv():
        mouse.moveTo(aero_plots_button)
        mouse.click()
        time.sleep(3)

        # The aero plots window shows up in a different place each time???
        aero_reference = list(mouse.locateCenterOnScreen(
            images+'aero_plots.png'))
        aero_reference[0] = aero_reference[0]+350
        aero_reference[1] = aero_reference[1]+500
        aero_file = [aero_reference[0]-865, aero_reference[1]-560]
        aero_export = [aero_file[0], aero_file[1]+50]
        aero_to_CSV = [aero_file[0]+300, aero_file[1]+50]

        # Save the CD CSV
        mouse.moveTo(aero_file)
        mouse.click()
        mouse.moveTo(aero_export)
        time.sleep(.6)
        mouse.moveTo(aero_to_CSV)
        mouse.click()
        mouse.typewrite('CD_'+name)
        mouse.hotkey('enter')
        time.sleep(.3)

        # Close the aero plots window
        mouse.moveTo(aero_file[0]+1280, aero_file[1]-50, duration=.3)
        mouse.click()
    get_aero_csv()

    def setup_flight_sim():
        # Open the flight sim window
        mouse.moveTo(flight_simulation_button)
        mouse.doubleClick()
        time.sleep(.6)

        # Set up the engine stuff
        mouse.moveTo(engine)
        mouse.doubleClick()
        time.sleep(0.1)
        mouse.hotkey('down')
        mouse.hotkey('tab')
        mouse.typewrite(str(cg_loc))
        mouse.hotkey('tab')
        mouse.typewrite('4')  # Just always set the nozzel exit diameter to 4
        mouse.hotkey('tab')
        mouse.typewrite(str(wet_weight))
        for i in range(16):
            mouse.hotkey('tab')
        mouse.hotkey('enter')
    setup_flight_sim()

    def attempt_flight_sim():
        mouse.moveTo(view_flight_data)
        mouse.click()
        time.sleep(1)

        # The stability warning shows up in different places too??
        try:  # If it's unstable just give up
            stability_ref = list(mouse.locateCenterOnScreen(
                images+'unstable.png'))
            close_stability_warning = \
                [stability_ref[0]+700, stability_ref[1]-80]
            mouse.moveTo(close_stability_warning)
            mouse.click()

            print('This one was unstable:', name)
            print()
        except Exception:  # If not unstable, close marginal stability window
            try:
                stability_ref = list(mouse.locateCenterOnScreen(
                    images+'stability_ref.png'))
                close_stability_warning = [stability_ref[0]+1150,
                                           stability_ref[1]-120]
                mouse.moveTo(close_stability_warning[0],
                             close_stability_warning[1])
                mouse.click()
            except Exception:
                time.sleep(0)

            time.sleep(1.3)
            mouse.moveTo(flight_data_file_button)
            mouse.click()
            mouse.moveTo(export_flight)
            time.sleep(0.6)
            mouse.moveTo(flight_to_csv)
            mouse.click()

            mouse.typewrite('F_'+name)
            mouse.hotkey('enter')
            close_flight_sim = [flight_data_file_button[0]+1800,
                                flight_data_file_button[1]-50]
            mouse.moveTo(close_flight_sim)
            mouse.click()
            time.sleep(0.4)

        # Close the flight sim window
        close_flight_setup = [engine[0]+1750, engine[1]-180]
        mouse.moveTo(close_flight_setup[0], close_flight_setup[1])
        mouse.click()
        mouse.hotkey('enter')
    attempt_flight_sim()

    def clear_rocket():
        # Clear the rocket
        mouse.moveTo(file_button[0], file_button[1])
        mouse.click()
        time.sleep(.3)
        mouse.moveTo(new_rocket[0], new_rocket[1])
        mouse.click()
        time.sleep(0)
        mouse.hotkey('left')
        mouse.hotkey('enter')
    clear_rocket()


class flight():
    def __init__(self, CD_file_path, F_file_path, dry_mass, dry_CoM,
                 radius, tube_radius, tank_top_loc, thrust_margin, name):
        '''
        Heart of PARSECs in-house simulations. Takes in data from
        RASAero II simulations and other rocket parameters, returns
        trajectory/stability predictions and plots.
        Inputs:
        1) File path to the RASAero II aero plots csv file for
            this design
        2) File path to the RASAero II flight simulation csv file for
            this design. The "dummy flight" is only to get effective
            frontal area
        3) Dry mass of the rocket (lbs). This is immeadiately internally
            converted to kg since all math is done in SI
        4) Distance from the tip of the nose to the CoM of dry rocket
            (in). This is immeadiately internally converted to m
        5) Radius of the rocket (in). This is immeadiately internally
            converted to m
        6) Radius of the CH4 tube running through the O2 tank (in).
            This is immeadiately internally converted to m
        7) Distance between the tip of the nose and top of the CH4
            tank (in). This is used to calculate change to the CoM as
            fuel and oxidizer are expelled. This is immeadiately internally
            converted to m.
        8) Margins on the thrust the engine is producing (percentage)
            Thrust = 800*(1-margin/100)
        9) Name of the design, for saving outputs (str)
        '''

        self.aero_data = pd.read_csv(CD_file_path)
        self.dummy_flight = pd.read_csv(F_file_path)
        self.dry_mass = dry_mass*0.453592  # Convert pounds to Kg
        self.dry_CoM = dry_CoM*0.0254
        self.rocket_radius = radius*0.0254
        self.CH4_tube_r = tube_radius*0.0254
        self.tank_top_to_nose_tip = tank_top_loc*0.0254
        self.thrust_margin = thrust_margin
        self.design_title = name

        # Design-specific constants

        # Seconds the engine can burn for with given margins
        self.burn_time = 9208./(800.*(1.-(self.thrust_margin/100.)))

        # Volume of needed O2 in m^3, including user-defined margin
        self.O2_vol = (O2_flow*self.burn_time/O2_rho)

        # Volume of needed CH4 in m^3, including user-defined margin
        self.CH4_vol = (CH4_flow*self.burn_time/CH4_rho)

        # Just adding total liquid weight,\
        self.wet_mass = self.dry_mass + (O2_flow*self.burn_time) + \
            (CH4_flow*self.burn_time)

        # height of the o2 tank [m]
        self.O2_res_len = self.O2_vol/(np.pi*(self.rocket_radius**2 -
                                              self.CH4_tube_r**2))

        # length of the inner CH4 tube [m]
        self.CH4_tube_len = self.O2_res_len

        # volume of inner CH4 tube [m^3]
        self.CH4_tube_vol = np.pi*self.CH4_tube_r**2*self.CH4_tube_len

        # volume of the upper CH4 tank [m^3]
        self.CH4_res_vol = self.CH4_vol - self.CH4_tube_vol

        # height of upper CH4 tank [m]
        self.CH4_res_len = self.CH4_res_vol/(np.pi*self.rocket_radius**2)

        # time after burn starts to empty upper CH4 tank [s]
        self.time_empt_CH4_res = self.CH4_res_vol/(CH4_flow/CH4_rho)

        self.A = self.effective_frontal_area(self.dummy_flight)
    # -----------------------------------------------------------------------
    # Interpolations
    # Density as func of altiude, SI units everywhere
    # Mach 1 as func of altitude, SI units everywhere

    def mach(self, height, velocity):
        '''Takes velocity and height in SI units, returns the Mach number'''
        return velocity/mach1(height)

    def CD_from_mach(self, m):
        f = interpolate.interp1d(np.array(self.aero_data['Mach']),
                                 np.array(self.aero_data['CD']))
        # NOTE: VELOCITY IS IN MACH, NOT SI.
        # Defining a function below to deal with that.
        return f(m)

    def drag_coef(self, height, velocity):
        '''
        Takes height, velocity in SI units and returns the dimensionless
        drag coefficient.
        '''
        velocity = abs(velocity)
        m = self.mach(height, velocity)
        # The lowest velocity it calculates for is 0.01,
        # and we can't interpolate beyond the range
        if m < 0.01:
            return self.CD_from_mach(0.01)
        else:
            return self.CD_from_mach(m)

    def CP_from_mach(self, m):
        CP = interpolate.interp1d(np.array(self.aero_data['Mach']),
                                  np.array(self.aero_data['CP']))
        return CP(m)

    def CoP(self, height, velocity):
        '''
        Takes height in m and velocity in m/s, returns location of the CoP m
        '''
        velocity = abs(velocity)
        m = self.mach(height, velocity)
        # The lowest velocity it calculates for is 0.01,
        # and we can't interpolate beyond the range
        if m < 0.01:
            return self.CP_from_mach(0.01)*0.0254
        else:
            return self.CP_from_mach(m)*0.0254

    # -----------------------------------------------------------------------
    # Misc. other calcs before trajectory
    def effective_frontal_area(self, data):
        # lb to N
        drags = np.array(self.dummy_flight['Drag (lb)'])*4.44822
        # ft to m
        heights = np.array(self.dummy_flight['Altitude (ft)'])*0.3048
        # Convert from feet/sec to m/s
        velocities = np.array(self.dummy_flight['Velocity (ft/sec)'])*0.3048
        densities = density(heights)
        cds = np.array(self.dummy_flight['CD'])

        x = cds*densities*np.square(velocities)/2

        fit = np.polyfit(x, drags, 1)

        return fit[0]

    # ------------------------------------------------------------------------
    # Trajectory related things
    def drag_force(self, height, velocity):
        '''Takes height, velocity in SI units and returns drag in SI units'''
        return density(height) * velocity**2 * self.A * \
            self.drag_coef(height, velocity) / 2.

    def mass(self, t):
        if t < self.burn_time:
            return self.wet_mass - (O2_flow+CH4_flow)*t
        else:
            return self.wet_mass - (O2_flow+CH4_flow)*self.burn_time

    def thrust(self, t):
        if t < self.burn_time:
            return 3558.58*(1-self.thrust_margin/100.)
        else:
            return 0

    def trajectory(self, time):
        '''
        Takes an array of times and returns an array of positions and an
        array of velocities at those times
        '''
        def derivatives(state, t):
            x, v = state
            dx = v
            if v >= 0:
                dv = (self.thrust(t) - self.drag_force(x, v) -
                      self.mass(t)*g)/self.mass(t)
            elif v < 0:
                dv = (self.drag_force(x, v) - self.mass(t)*g)/self.mass(t)
            return [dx, dv]

        init_state = [0, 0]
        state = odeint(derivatives, init_state, time)

        x = np.zeros(len(time))
        v = np.zeros(len(time))

        for s in range(len(state)):
            x[s] = state[s][0]
            v[s] = state[s][1]

        return x, v

    # ------------------------------------------------------------------------
    # Stability related things
    def CoM_loc(self, t):
        # Masses of each component
        if t < self.burn_time:
            remaining_O2_mass = (self.O2_vol*O2_rho) - (O2_flow)*t
            if t < self.time_empt_CH4_res:
                remaining_CH4_res_mass = \
                    (self.CH4_res_vol*CH4_rho) - (CH4_flow)*t
                remaining_CH4_tube_mass = self.CH4_tube_vol*CH4_rho
            else:
                remaining_CH4_res_mass = 0
                remaining_CH4_tube_mass = (self.CH4_tube_vol*CH4_rho) - \
                    (CH4_flow)*(t-self.time_empt_CH4_res)
        else:
            return self.dry_CoM  # this is in m

        # Locations of CoMs of each components
        O2_CoM_loc = self.O2_res_len - \
            self.O2_res_len*(0.5 - t/(2.*self.burn_time)) + \
            self.tank_top_to_nose_tip + self.CH4_res_len

        if t < self.time_empt_CH4_res:
            CH4_res_CoM_loc = self.CH4_res_len - \
                self.CH4_res_len*(0.5 - t/(2.*self.time_empt_CH4_res)) + \
                self.tank_top_to_nose_tip
            CH4_tube_CoM_loc = self.CH4_tube_len/2. + \
                self.tank_top_to_nose_tip + self.CH4_res_len
        else:
            CH4_res_CoM_loc = 0  # Doesn't matter, multiplied by zero
            CH4_tube_CoM_loc = self.CH4_tube_len - \
                self.CH4_tube_len * \
                (0.5 - (t-self.time_empt_CH4_res) /
                 (2.*(self.burn_time - self.time_empt_CH4_res))) + \
                self.tank_top_to_nose_tip + self.CH4_res_len

        return (self.dry_mass*self.dry_CoM + remaining_O2_mass*O2_CoM_loc +
                remaining_CH4_res_mass*CH4_res_CoM_loc +
                remaining_CH4_tube_mass*CH4_tube_CoM_loc) / \
            (self.dry_mass+remaining_O2_mass +
             remaining_CH4_res_mass+remaining_CH4_tube_mass)
    # ------------------------------------------------------------------------
    # Outputs

    def produce_outputs(self):
        def full_output_table():
            # t1 = clock.time()
            time = np.arange(0, 50, 0.1)
            x, v = self.trajectory(time)
            # print 'Trajec. took ' + str(clock.time()-t1)

            # t2 = clock.time()
            COMs = np.zeros(len(time))
            COPs = np.zeros(len(time))
            machs = np.zeros(len(time))
            for i in range(len(time)):
                COMs[i] = self.CoM_loc(time[i])
                COPs[i] = self.CoP(x[i], v[i])
                machs[i] = self.mach(x[i], v[i])
            stability = (COPs-COMs)/self.rocket_radius
            # print 'Stability took ' + str(clock.time() - t2)

            data = {'Time (s)': time, 'Altitude (ft)': x*3.28084,
                    'Velocity (ft/s)': v*3.28084, 'Velocity (mach)': machs,
                    'Center of Mass (m from nose)': COMs,
                    'Center of Pressure (m from nose)': COPs,
                    'Stability Margin': stability}
            output = pd.DataFrame.from_dict(data)
            output.to_csv('Result_' + self.design_title+'.csv')

        def altitude_plot():
            data = pd.read_csv(self.design_title+'_full_data.csv')
            time = data['Time (s)']
            x = data['Altitude (ft)']
            plt.plot(time, x)
            plt.xlabel('Time (s)')
            plt.ylabel('Altitude (ft)')
            plt.title('Altitude')
            plt.tight_layout()
            plt.savefig(self.design_title+' Altitude', dpi=300,
                        bbox_inches='tight')

            plt.clf()
            plt.cla()
            plt.close()

        def velocity_plot():
            data = pd.read_csv(self.design_title+'_full_data.csv')
            time = data['Time (s)']
            v = data['Velocity (mach)']
            plt.plot(time, v)
            plt.xlabel('Time (s)')
            plt.ylabel('Velocity (mach)')
            plt.title('Velocity')
            plt.tight_layout()
            plt.savefig(self.design_title+' Velocity', dpi=300,
                        bbox_inches='tight')

            plt.clf()
            plt.cla()
            plt.close()

        def stability_plot():
            data = pd.read_csv(self.design_title+'_full_data.csv')
            time = data['Time (s)']
            s = data['Stability Margin']
            plt.plot(time, s)
            plt.xlabel('Time (s)')
            plt.ylabel('Stability Margin')
            plt.title('Stability- ideally >1 subsonic, >2 if faster')
            plt.tight_layout()
            plt.savefig(self.design_title+' Stability', dpi=300,
                        bbox_inches='tight')

            plt.clf()
            plt.cla()
            plt.close()

        full_output_table()
#         altitude_plot()
#         velocity_plot()
#         stability_plot()
# a = flight(p, f, 50, 20, 10, .2, 30, 30, 'test')
# a.produce_outputs()


def score_design(radius, dry_mass, nose_len, body_len, boat_len, dry_CoM,
                 nose_shape, nose_tip_di, nose_power, fin_count,
                 fin_root_chord, fin_span, fin_tip_chord, fin_sweep,
                 fin_thickness, fin_base_sep, fin_shape, fin_le_rad,
                 fin_le_len, fin_te_len, CH4_tube_radius, thrust_margin):
    burn_t = (9208./(800.*(1.-(thrust_margin/100.))))

    # Keep it in pounds
    wet_weight = (burn_t * (O2_flow + CH4_flow))*2.20462 + dry_mass
    len_tank_assembly = (0.00690077*(radius*0.0254)**(-2.))*39.3701  # [in]
    nose_to_tank = nose_len + body_len + boat_len - engine_len - \
        len_tank_assembly
    nose_to_tank_m = nose_to_tank*0.0254  # [m]

    def calc_wet_CoM():
        rocket_r_m = radius*0.0254  # in to m
        CH4_tube_r_m = CH4_tube_radius*0.0254  # in to m
        O2_vol = (O2_flow*burn_t)/O2_rho
        CH4_vol = (CH4_flow*burn_t)/CH4_rho

        # height of the o2 tank [m]
        O2_res_len = O2_vol/(np.pi*(rocket_r_m**2. - CH4_tube_r_m**2.))
        CH4_tube_len = O2_res_len  # length of the inner CH4 tube [m]

        # volume of inner CH4 tube [m^3]
        CH4_tube_vol = np.pi*CH4_tube_r_m**2.*CH4_tube_len

        # volume of the upper CH4 tank [m^3]
        CH4_res_vol = CH4_vol - CH4_tube_vol
        CH4_res_len = CH4_res_vol/(np.pi*rocket_r_m**2.)

        # Masses of each component
        remaining_O2_mass = O2_vol*O2_rho
        remaining_CH4_res_mass = CH4_res_vol*CH4_rho
        remaining_CH4_tube_mass = CH4_tube_vol*CH4_rho

        # Locations of CoMs of each components
        CH4_res_CoM_loc = nose_to_tank_m + CH4_res_len/2.
        CH4_tube_CoM_loc = nose_to_tank_m + CH4_res_len + CH4_tube_len/2.
        O2_CoM_loc = CH4_tube_CoM_loc

        # Convert them all back to [in] from [SI]
        remaining_O2_mass = remaining_O2_mass*2.20462
        remaining_CH4_res_mass = remaining_CH4_res_mass*2.20462
        remaining_CH4_tube_mass = remaining_CH4_tube_mass*2.20462

        CH4_res_CoM_loc = CH4_res_CoM_loc*39.3701
        CH4_tube_CoM_loc = CH4_tube_CoM_loc*39.3701
        O2_CoM_loc = O2_CoM_loc*39.3701

        return (dry_mass*dry_CoM + remaining_O2_mass*O2_CoM_loc +
                remaining_CH4_res_mass*CH4_res_CoM_loc +
                remaining_CH4_tube_mass*CH4_tube_CoM_loc) \
            / (dry_mass+remaining_O2_mass+remaining_CH4_res_mass +
               remaining_CH4_tube_mass)

    wet_CoM = calc_wet_CoM()
    rocket_name = str(radius) + '_' + str(dry_mass) + '_' + str(nose_len) + \
        '_' + str(body_len) + '_' + str(boat_len) + '_' + str(dry_CoM) + \
        '_' + str(nose_shape) + '_' + str(nose_tip_di) + '_' + \
        str(nose_power) + '_' + str(fin_count) + '_' + str(fin_root_chord) + \
        '_' + str(fin_span) + '_' + str(fin_tip_chord) + '_' + \
        str(fin_sweep) + '_' + str(fin_thickness) + '_' + str(fin_base_sep) + \
        '_' + str(fin_shape) + '_' + str(fin_le_rad) + '_' + \
        str(fin_le_len) + '_' + str(fin_te_len) + '_' + \
        str(CH4_tube_radius) + '_' + str(thrust_margin)

    make_rocket(radius, wet_weight, nose_len, body_len, boat_len, wet_CoM,
                nose_shape, nose_tip_di, nose_power, fin_count,
                fin_root_chord, fin_span, fin_tip_chord, fin_sweep,
                fin_thickness, fin_base_sep, fin_shape, fin_le_rad,
                fin_le_len, fin_te_len, rocket_name)

    # If it went unstable for RASAero, don't run it further
    if not os.path.exists(data_folder + 'CD_' + rocket_name + '.csv'):
        return unstable_score

    flight_sim = flight(data_folder + 'CD_' + rocket_name + '.csv',
                        data_folder + 'F_' + rocket_name + '.csv',
                        dry_mass, dry_CoM, radius, CH4_tube_radius,
                        nose_to_tank, thrust_margin, rocket_name)
    flight_sim.produce_outputs()

    # Score the run
    # Altitude contribution
    a = pd.read_csv('Result_'+rocket_name+'.csv')
    apogee = max(a['Altitude (ft)'])
    if apogee <= 45000.:
        altitude_score = 45000. - apogee
    else:
        altitude_score = 6*(apogee-45000.)

    # Stability contribution
    stability_error = 0
    for i in range(len(a['Stability Margin'])):
        if a['Velocity (mach)'][i] < 1.:
            stability_error += abs(1.-a['Stability Margin'][i])
        else:
            stability_error += abs(2.-a['Stability Margin'][i])
    stability_error = stability_error*40

    print('Altitude Score: ' + str(altitude_score))
    print('Stability: ' + str(stability_error))

    return altitude_score+stability_error
