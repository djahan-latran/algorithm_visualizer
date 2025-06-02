"""Variables to track different states of the application"""


class AppStates:
    def __init__(self):
        self.app_running = False
        self.algo_running = False

        self.surface_update_intv = 1/50
        self.gui_update_intv = 1/60
        self.surface_updated = 0
        self.gui_updated = 0

        self.algo_generator = None

        self.selected_algo = None
        self.curr_algo_cat = None
        self.value_to_find = None
        self.values = None
        self.info_text = None
        self.code_text = None
        self.text_updated = False

        self.target_sel_phase = False
        self.target_selected = False
        self.target_loc = None

        self.obstacle_sel_phase = False
        self.obstacle_selected = False

        self.checkerboard = None

        self.parameter_reset = False
        self.board_rect_amount = (34, 20) # Should make animation panel pass that info to controller to create board
        self.anim_surf_size = (680, 400) # Info for the controller to create the board

        self.next_algo_step = False
        self.next_animation_frame = False

        self.draw_bg_info = {"positive": [], "neutral": [], "negative": []}
        self.draw_pf_info = {"current": None, "visited": None, "path": None}