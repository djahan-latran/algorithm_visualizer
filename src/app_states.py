

class AppStates:
    """
    AppStates holds mutiple variables and flags that get manipulated by the controller
    on certain actions. The view uses the info to know what to display at any moment.
    """
    def __init__(self):
        # Tracks if app and algorithm are running
        self.app_running = False
        self.algo_running = False

        # Update interval for gui and animation surface (decoupled)
        self.surface_update_intv = 1/50
        self.gui_update_intv = 1/60
        # Timer when they lastly got updated
        self.surface_updated = 0
        self.gui_updated = 0

        # Holds the algorithm generator
        self.algo_generator = None

        # Currently selected algorithm name and category
        self.selected_algo = None
        self.curr_algo_cat = None

        # Target value (for basic search algs)
        self.value_to_find = None
        # The values of the list that isinput for search and sort algorithms
        self.values = None

        # The texts that are displayed on the info and code panels
        self.info_text = None
        self.code_text = None
        # Tracks if text has to be updated if different algo got selected
        self.text_updated = False

        # Tracks if it is target selection phase and if target got selected
        self.target_sel_phase = False
        self.target_selected = False
        self.target_loc = None

        # Tracks if it is obstacle selection phase and if obstacles got selected
        self.obstacle_sel_phase = False
        self.obstacle_selected = False

        # The grid (2d list) for graph traversal algorithms
        self.checkerboard = None

        # Tracks if paramters should or got reset
        self.parameter_reset = False
        self.board_rect_amount = (34, 20) # Should make animation panel pass that info to controller to create board
        self.anim_surf_size = (680, 400) # Info for the controller to create the board

        # Let's controller know if next generator step should be allowed
        self.next_algo_step = False
        # Let's view know if next animation frame should be rendered
        self.next_animation_frame = False

        # The dictionaries that retrieve info from the Model which can then be read by the View.
        self.draw_bg_info = {"positive": [], "neutral": [], "negative": []}
        self.draw_pf_info = {"current": None, "visited": None, "path": None}