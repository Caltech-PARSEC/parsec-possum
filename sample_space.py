'''
Code to get a hyperopt sample space of rocket parameters, and default
sample spaces that should cover most search cases.
'''


def get_sample_space(
        # Fixed
        dry_mass=65,
        thrust_margin=15,
        # Learnable
        radius=None,
        dry_com=None,
        nose_len=None, body_len=None, boat_len=None,
        nose_shape=None, nose_tip_di=None, nose_power=None,
        fin_count=None, fin_root_chord=None, fin_span=None, fin_tip_chord=None,
        fin_sweep=None, fin_thickness=None, fin_base_sep=None, fin_shape=None,
        fin_le_rad=None, fin_le_len=None, fin_te_len=None,
        ch4_tube_radius=None):
    '''
    Gets a sample space of rocket parameters, many of which are optional.
    Optional (None) parameters are fixed if provided a value and learned
    otherwise.

    Arguments (fixed)
    -----------------
    dry_mass : float
        Weight of rocket without fuel and oxidizer, in pounds.
    thrust_margin : float [0, 100]
        Inefficiency of the engine as a percentage.

    Arguments (learnable)
    ---------------------
    radius : float [2, 15]
        Radius of the main body, in inches.
    dry_com : float [0, 1]
        Distance from the tip of the nose to the center of mass of the dry
        rocket, as a proportion from
        nose_len + body_len - (tank_and_engine_len / 2)
        to nose_len + body_len - (tank_and_engine_len / 3).
    nose_len : float [2, 30]
        Length of the nosecone, in inches.
    body_len : float [1.5, 4]
        Length of the rocket body in inches is computed as body_len *
        (0.00690077 * ((radius * 0.0254) ** -2) * 39.3701 + 10).
        The second quantity is tank_and_engine_len.
    boat_len : float [0, 10]
        Length of the engine shroud, in inches.
    nose_shape : int [1, 7]
        Indicates which nose shape is used.
    nose_tip_di : float [0, 2]
        Diameter of the nosecone tip, in inches.
    nose_power : float [0, 0.99]
        Power law relationship determining nosecone tip shape.
        Only used if nose_shape = 4.
    fin_count : int [3, 4]
        Number of fins on the rocket.
    fin_root_chord : float [0, 1]
        Length of fin in contact with the body as a proportion from 2 inches to
        (body_len + nose_len) / 2.
    fin_span : float [0, 1]
        How far the fin projects from the body, as a proportion from 2 inches
        to (body_len + nose_len) / 2.
    fin_tip_chord : float [0, 1]
        Length of the outermost edge of the fin as a proportion from 0 to
        fin_root_chord.
    fin_sweep : float [0, 1]
        How far towards the back of the rocket the fins sweep out, as a
        proportion from 0 to fin_root_chord.
    fin_thickness : int [1, 10]
        Thickness of the fins in eighth-inches.
    fin_base_sep : float [0, 1]
        Placement of the fins relative to the bottom of the body, as a
        proportion from fin_root_chord to (body_len + nose_len) / 2.
    fin_shape : int [1, 9]
        Indicates which fin shape is used.
    fin_le_rad : float [0.1, 1]
        Only used for fin_shape 1, 3, 4, 5, 6, and 7. Likely not important.
    fin_le_len : float [0.1, 3]
        Length of the airfoil of the leading edge of the fin. Only used for
        fin_shape 1, 3, and 6. Likely not important.
    fin_te_len : float [0.1, 3]
        Length of the airfoil of the trailing edge of the fin. Only used for
        fin_shape 1. Likely not important.
    ch4_tube_radius : int [1, 16]
        Radius of the pipe carrying fuel from the reservoir through the
        oxidizer reservoir in eigth-inches. Likely not important.

    Returns
    -------
    list
        A list of arguments in order of above, either numeric or as hyperopt
        parameter expressions.
    '''
    raise(NotImplementedError)  # TODO


def parse_args(args):
    '''
    Parse a list of arguments produced by hyperopt into a kwargs dict
    acceptable by score_design. Also converts proportions into real values and
    puts all values into correct units.

    Arguments
    ---------
    args : list of numbers
        The arguments as an in-order list of numbers.

    Returns
    -------
    dict from string to number
        A dictionary with keys equal to the argument names of score_design
        and values equal to the in-order values of args in the correct units.
    '''
    radius = args[2]
    nose_len = args[4]
    body_len_frac = args[5]
    tank_and_engine_len = 0.00690077 * ((radius * 0.0254) ** -2) * 39.3701 + 10
    body_len = body_len_frac * tank_and_engine_len
    fin_root_chord = _scale(args[11], 2, (body_len + nose_len) / 2)
    fin_shape = args[17]

    return {
        'dry_mass': args[0],
        'thrust_margin': args[1],
        'radius': radius,
        'dry_com': _scale(args[3],
                          nose_len + body_len - (tank_and_engine_len / 2),
                          nose_len + body_len - (tank_and_engine_len / 3)),
        'nose_len': nose_len,
        'body_len': body_len,
        'boat_len': args[6],
        'nose_shape': args[7],
        'nose_tip_di': args[8],
        'nose_power': args[9],
        'fin_count': args[10],
        'fin_root_chord': fin_root_chord,
        'fin_span': _scale(args[12], 2, (body_len + nose_len) / 2),
        'fin_tip_chord': _scale(args[13], 0, fin_root_chord),
        'fin_sweep': _scale(args[14], 0, fin_root_chord),
        'fin_thickness': args[15] / 8,
        'fin_base_sep': _scale(args[16],
                               fin_root_chord, (body_len + nose_len) / 2),
        'fin_shape': fin_shape,
        'fin_le_rad': args[18] if fin_shape in [1, 3, 4, 5, 6, 7] else None,
        'fin_le_len': args[19] if fin_shape in [1, 3, 6] else None,
        'fin_te_len': args[20] if fin_shape == 1 else None,
        'ch4_tube_radius': args[21] / 8
    }


def _scale(in_, min_, max_):
    '''
    Scale a value in the range [0, 1] to the range [min_, max_].

    Arguments
    ---------
    in_ : float [0, 1]
        The proportional value.
    min_ : float
        The minimum output value, mapped to when in_ = 0.
    max_ : float
        The maximum output value, mapped to when in_ = 1.

    Returns
    -------
    float : [min_, max_]
        The proportional value scaled into the output range.
    '''
    assert(0 < in_ < 1)
    assert(min_ < max_)
    return in_ * (max_ - min_) + min_
