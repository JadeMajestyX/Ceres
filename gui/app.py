import customtkinter
import os
from PIL import Image
from gui.views.home_view import HomeView
from gui.views.actuators_view import ActuatorsView
from gui.views.plants_view import PlantsView
from gui.views.sensores_view import SensoresView
from gui.views.config_view import ConfigView
from gui.views.config_view import ConfigView


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ceres")
        self.geometry("1280x720")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"..", "assets", "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ico.png")), size=(26, 26))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "ico.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.sensor = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "sensor_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "sensor_light.png")), size=(20, 20))
        self.actuadores = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "actuator_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "actuator_light.png")), size=(20, 20))
        self.plantas = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "plant-dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "plant-light.png")), size=(20, 20))
        self.config = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "config.png")),
                                     dark_image=Image.open(os.path.join(image_path, "config.png")), size=(20, 20))


        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Ceres  ", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.sensores_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Sensores",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.sensor, anchor="w", command=self.sensores_button_event)
        self.sensores_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Actuadores",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.actuadores, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Plantas",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.plantas, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")
        self.config_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Configuración",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             image=self.config, anchor="w", command=self.config_button_event)
        self.config_button.grid(row=5, column=0, sticky="ew")


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = HomeView(self)
        self.home_frame.grid_columnconfigure(0, weight=1)

        # create Sensores frame
        self.sensores_frame = SensoresView(self)
        self.sensores_frame.grid_columnconfigure(0, weight=1)

        # create Actuators frame
        self.actuators_frame = ActuatorsView(self)
        self.actuators_frame.grid_columnconfigure(0, weight=1)


        self.plants_frame = PlantsView(self) #plantas

        self.config_frame = ConfigView(self)
        self.config_frame.grid_columnconfigure(0, weight=1)



        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.sensores_button.configure(fg_color=("gray75", "gray25") if name == "sensores" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "sensores":
            self.sensores_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sensores_frame.grid_forget()
        if name == "frame_3":
            self.actuators_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.actuators_frame.grid_forget()

        if name == "frame_4":
              self.plants_frame.grid(row=0, column=1, sticky="nsew")  #aquí estaba mal, se repetia el third_frame
        else:
            self.plants_frame.grid_forget()
            self.config_button.configure(fg_color=("gray75", "gray25") if name == "configuracion" else "transparent")

        if name == "configuracion":
            self.config_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.config_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def sensores_button_event(self):
        self.select_frame_by_name("sensores")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")
        
    def config_button_event(self):
        self.select_frame_by_name("configuracion")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

