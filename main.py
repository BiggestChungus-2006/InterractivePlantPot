from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty

# Set the application to run in fullscreen mode
Window.fullscreen = 'auto'

# --- KIVY DESIGN LANGUAGE STRING ---
# By embedding the KV code here, we remove any file loading issues.
KV_STRING = """
<MainLayout>:
    # --- BACKGROUND IMAGE (covers the whole screen) ---
    Image:
        id: plant_image
        source: 'images/happy.png'
        allow_stretch: True
        keep_ratio: False  # This ensures the image fills the entire screen
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    # --- SENSOR CONTROL PANEL (Overlays the background image) ---
    BoxLayout:
        orientation: 'vertical'
        size_hint: 0.35, 0.4
        pos_hint: {'right': 0.98, 'center_y': 0.5}
        spacing: 15
        padding: 20
        canvas.before:
            Color:
                rgba: 0.1, 0.12, 0.15, 0.8  # Semi-transparent background
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [15]

        Label:
            id: moisture_label
            text: 'Soil Moisture: 50%'
            font_size: '18sp'
            size_hint_y: None
            height: '30dp'
        Slider:
            id: moisture_slider
            min: 0
            max: 100
            value: 50
            on_value: root.update_plant_status()
            size_hint_y: None
            height: '48dp'

        Label:
            id: light_label
            text: 'Ambient Light: 80%'
            font_size: '18sp'
            size_hint_y: None
            height: '30dp'
        Slider:
            id: light_slider
            min: 0
            max: 100
            value: 80
            on_value: root.update_plant_status()
            size_hint_y: None
            height: '48dp'

    # --- TOP-LEFT EXIT BUTTON ---
    Button:
        text: 'Exit'
        size_hint: None, None
        size: '150dp', '60dp'  # Increased size
        pos_hint: {'x': 0.02, 'top': 0.98}
        on_press: app.stop()
        background_color: 0.8, 0.2, 0.2, 0.9 # Reddish color

    # --- TOP-RIGHT RESET BUTTON ---
    Button:
        text: 'Reset'
        size_hint: None, None
        size: '150dp', '60dp'  # Increased size
        pos_hint: {'right': 0.98, 'top': 0.98}
        on_press: root.reset_sliders()
        background_color: 0.2, 0.5, 0.8, 0.9 # Blueish color

    # --- BOTTOM-LEFT CAMERA TOGGLE BUTTON ---
    Button:
        text: 'Camera'
        size_hint: None, None
        size: '150dp', '60dp'  # Increased size
        pos_hint: {'x': 0.02, 'y': 0.02}
        on_press: root.toggle_camera()
        # Change color based on the camera_active property
        background_color: (0.2, 0.8, 0.2, 0.9) if root.camera_active else (0.4, 0.4, 0.4, 0.9)

    # --- BOTTOM-RIGHT MIC TOGGLE BUTTON ---
    Button:
        text: 'Mic'
        size_hint: None, None
        size: '150dp', '60dp'  # Increased size
        pos_hint: {'right': 0.98, 'y': 0.02}
        on_press: root.toggle_mic()
        # Change color based on the mic_active property
        background_color: (0.2, 0.8, 0.2, 0.9) if root.mic_active else (0.4, 0.4, 0.4, 0.9)
"""

# Load the KV string
Builder.load_string(KV_STRING)

class MainLayout(FloatLayout):
    """
    This class is the root widget of our application.
    It now includes state tracking for the camera and mic.
    """
    # Properties to track the state of the new buttons
    camera_active = BooleanProperty(False)
    mic_active = BooleanProperty(False)

    def on_kv_post(self, base_widget):
        """
        Kivy method called after KV rules are applied. Good for initialization.
        """
        self.update_plant_status()

    def toggle_camera(self):
        """Called when the Camera button is pressed."""
        self.camera_active = not self.camera_active
        print(f"Camera state: {'Active' if self.camera_active else 'Inactive'}")
        self.update_plant_status()

    def toggle_mic(self):
        """Called when the Mic button is pressed."""
        self.mic_active = not self.mic_active
        print(f"Mic state: {'Active' if self.mic_active else 'Inactive'}")
        self.update_plant_status()

    def update_plant_status(self, *args):
        """
        Core logic function, now checks for camera/mic state first.
        """
        # First, update the labels regardless of state
        moisture = self.ids.moisture_slider.value
        light = self.ids.light_slider.value
        self.ids.moisture_label.text = f"Soil Moisture: {int(moisture)}%"
        self.ids.light_label.text = f"Ambient Light: {int(light)}%"

        # Check if camera or mic is active
        if self.camera_active or self.mic_active:
            new_state = "smart"
        else:
            # If neither is active, revert to sensor-based logic
            new_state = "happy"
            if moisture < 30:
                new_state = "thirsty"
            elif light < 20:
                new_state = "scare_of_dark"
            elif light >= 80:
                new_state = "enjoying_sun"
        
        new_image_source = f"images/{new_state}.png"

        if self.ids.plant_image.source != new_image_source:
            self.ids.plant_image.source = new_image_source
            print(f"Plant state changed to: {new_state}")
    
    def reset_sliders(self):
        """Resets the sliders to their default values."""
        self.ids.moisture_slider.value = 50
        self.ids.light_slider.value = 80
        # The update triggers automatically due to the 'on_value' binding


class PlantApp(App):
    """
    This is the main application class.
    """
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    PlantApp().run()

