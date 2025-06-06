"""A gui manager to bundle the different panel sections and gui elements"""
from src.gui.gui_panels import MainPanel, MenuPanel, AnimationPanel, CodePanel, SettingsPanel, InfoPanel
from src.utility.styles import AppColours, AppFonts


class GuiManager: #let the manager go through events and delegate them to panels?
    
    def __init__(self, controller, pg_manager):
        self.controller = controller
        self.pg_manager = pg_manager
        
        #Fonts and colors instance
        self.fonts = AppFonts()
        self.colours = AppColours()
    
    def create_gui(self):
        #Create panels
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