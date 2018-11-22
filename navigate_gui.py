from time import sleep
from subprocess import Popen
from pywinauto import Desktop

# Import-time setup
sim_path = 'C:\Program Files (x86)\RASAero II\RASAero II.exe'
desktop = Desktop(backend='uia')
window_main = desktop['RAS Aero II Dialog']


# RASAero API
def make_nosecone(shape, diameter, length, tip_radius):
    window_main['Add Nose Cone'].click_input(double=True)
    window = window_main['Nose Cone']
    window.child_window(auto_id="1001", control_type="Edit").type_keys(shape)
    window.child_window(auto_id='mtb_Diameter').window().type_keys(diameter)
    window.child_window(auto_id='mtb_LEBluntRadius').window()\
        .type_keys(tip_radius)
    window.child_window(auto_id='mtb_Length').window().type_keys(length)
    window.Add.click()


def make_body(length, fin_count, root_chord, span, tip_chord, sweep_distance,
              fin_thickness, base_distance, airfoil_section,
              le_length=None, te_length=None, le_radius=None):
    '''
    Note: airfoil_section is an integer representing which airfoil to select.
    '''
    window_main['Add a Body Tube Section'].click_input(double=True)
    window_body = window_main['Body Tube']

    # Body setup
    window_body.child_window(auto_id='mtb_Length').window().type_keys(length)

    # Airfoil setup
    window_body.Fins.click_input()
    window_fins = window_main['Fins']
    window_fins.child_window(auto_id='1001').\
        type_keys('{HOME}{DOWN ' + str(airfoil_section) + '}')
    if le_length:
        window_fins.child_window(auto_id='FX1').window().type_keys(le_length)
    if te_length:
        window_fins.child_window(auto_id='FX3').window().type_keys(te_length)
    if le_radius:
        window_fins.child_window(auto_id='FinLERadius').window()\
            .type_keys(le_radius)

    # Fins setup
    window_fins.child_window(auto_id='FinCount').window().type_keys(fin_count)
    window_fins.child_window(auto_id='Chord').window().type_keys(root_chord)
    window_fins.child_window(auto_id='Span').window().type_keys(span)
    window_fins.child_window(auto_id='TipChord').window().type_keys(tip_chord)
    window_fins.child_window(auto_id='SweepDistance').window().\
        set_text(sweep_distance)
    window_fins.child_window(auto_id='FinThickness').window().\
        set_text(fin_thickness)
    window_fins.child_window(auto_id='Loc').window().type_keys(base_distance)

    # Return to main dialog
    window_fins.OK.click()
    window_body.Add.click()


def make_boattail(length, rear_di):
    window_main['Add a Boattail'].click_input(double=True)
    window = window_main['BoatTail']
    window.child_window(auto_id='mtb_Length').window().type_keys(length)
    window.child_window(auto_id='mtb_RearDiameter').window().type_keys(rear_di)
    window.Add.click()


def save_aero_plots(path):
    raise NotImplementedError # TODO


def save_flight_sim(path):
    raise NotImplementedError # TODO
