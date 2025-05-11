"""Variables to track different states of the application"""


class AppStates:
    def __init__(self):
        self.running = False
        self.algo_running = False

        self.algo_generator = None

        self.selected_algo = None
        self.curr_algo_cat = None
        self.value_to_find = None

        self.target_sel_phase = False
        self.target_selected = False

        self.obstacle_sel_phase = False
        self.obstacle_selected = False