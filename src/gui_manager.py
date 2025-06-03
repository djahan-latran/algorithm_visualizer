"""A gui manager to bundle the different panel sections and gui elements"""
from src.gui.gui_panels import MainPanel, MenuPanel, AnimationPanel, CodePanel, SettingsPanel, InfoPanel
from src.utility.styles import AppColours, AppFonts


class GuiManager:
    """
    Initiates and bundles the different panel sections.
    """
    
    def __init__(self, controller, pg_manager):
        """
        Initiates the GuiManager instance.

        Parameters
        ----------

        controller : class instance
            Controller instance for app logic

        pg_manager : class instance
            the pygame_gui manager that is needed to update the gui elements.

        Attributes
        ----------

        fonts : class instance
            AppFonts instance to pass to the panels
        
        colours : class instance
            AppColours instance to pass to the panels
        """
        self.controller = controller
        self.pg_manager = pg_manager
        
        #Fonts and colors instance
        self.fonts = AppFonts()
        self.colours = AppColours()
    
    def create_gui(self):
        """
        Creates the different panels
        """

        self.main_panel = MainPanel(self.fonts, 
                                    self.colours, 
                                    self.controller
                                    )
        self.menu_panel = MenuPanel(self.pg_manager, 
                                    self.controller
                                    )
        self.menu_panel.create_menu()
        self.animation_panel = AnimationPanel(self.fonts,
                                              self.colours,
                                              self.main_panel.screen,
                                              self.controller
                                              )
        self.code_panel = CodePanel(self.pg_manager,
                                    self.controller
                                    )
        self.settings_panel = SettingsPanel(self.fonts, 
                                            self.colours, 
                                            self.pg_manager, 
                                            self.main_panel.screen,
                                            self.controller
                                            )
        self.settings_panel.create_settings()
        self.settings_panel.create_control_sliders()
        self.info_panel = InfoPanel(self.fonts, 
                                    self.colours,
                                    self.pg_manager, 
                                    self.controller
                                    )
        self.info_panel.create_header()