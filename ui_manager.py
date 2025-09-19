from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.clock import Clock

Window.fullscreen = 'auto'

KV_STRING = """
<MainLayout>:
    # --- BACKGROUND VIDEO PLAYERS (Layered for crossfading) ---
    Video:
        id: video_player_a
        source: 'videos/Plant_Swaying_Video_Generation.mp4'
        state: 'play'
        options: {'loop': True}
        allow_stretch: True
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        opacity: 1

    Video:
        id: video_player_b
        state: 'stop'
        options: {'loop': True}
        allow_stretch: True
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        opacity: 0
    
    # --- INVISIBLE BUTTON OVER PLANT ---
    # This button is transparent and sits in the middle of the screen.
    # When pressed, it triggers the 'touched' video animation.
    Button:
        size_hint: 0.4, 0.6
        pos_hint: {'center_x': 0.5, 'center_y': 0.45}
        background_color: 0, 0, 0, 0 # Makes the button invisible
        on_press: root.play_touch_video()

    # --- SENSOR CONTROL PANEL (Overlays the background video) ---
    BoxLayout:
        orientation: 'vertical'
        size_hint: 0.35, 0.4
        pos_hint: {'right': 0.98, 'center_y': 0.5}
        spacing: 15
        padding: 20
        canvas.before:
            Color:
                rgba: 0.1, 0.12, 0.15, 0.8
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

    # --- Buttons ---
    Button:
        text: 'Exit'
        size_hint: None, None
        size: '150dp', '60dp'
        pos_hint: {'x': 0.02, 'top': 0.98}
        on_press: app.stop()
        background_color: 0.8, 0.2, 0.2, 0.9
    Button:
        text: 'Live Data'
        size_hint: None, None
        size: '150dp', '60dp'
        pos_hint: {'right': 0.98, 'top': 0.98}
        on_press: root.reset_sliders()
        background_color: 0.2, 0.5, 0.8, 0.9
    Button:
        text: 'Camera'
        size_hint: None, None
        size: '150dp', '60dp'
        pos_hint: {'x': 0.02, 'y': 0.02}
        on_press: root.toggle_camera()
        background_color: (0.2, 0.8, 0.2, 0.9) if root.camera_active else (0.4, 0.4, 0.4, 0.9)
    Button:
        text: 'Mic'
        size_hint: None, None
        size: '150dp', '60dp'
        pos_hint: {'right': 0.98, 'y': 0.02}
        on_press: root.toggle_mic()
        background_color: (0.2, 0.8, 0.2, 0.9) if root.mic_active else (0.4, 0.4, 0.4, 0.9)
"""

Builder.load_string(KV_STRING)

class MainLayout(FloatLayout):
    camera_active = BooleanProperty(False)
    mic_active = BooleanProperty(False)
    active_player_id = StringProperty('a')
    previous_state = StringProperty('happy') # Remembers the state before being touched

    video_map = {
        "happy": "Plant_Swaying_Video_Generation.mp4",
        "thirsty": "Thirsty_Plant_Video_Generation.mp4",
        "scare_of_dark": "Plant_Scared_of_the_Dark_Video.mp4",
        "enjoying_sun": "Plant_Enjoys_Sun_In_Looping_Video.mp4",
        "smart": "Plant_Acting_Smart_Video_Generation.mp4",
        "touched": "Plant_Touched.mp4" # New state for the touch video
    }

    def start_transition(self, dt):
        """This function starts the fade animation and is called by the Clock."""
        if self.active_player_id == 'a':
            active_player = self.ids.video_player_a
            inactive_player = self.ids.video_player_b
        else:
            active_player = self.ids.video_player_b
            inactive_player = self.ids.video_player_a

        anim = Animation(opacity=0, duration=0.7)
        anim.bind(on_complete=self.on_fade_out_complete)
        anim.start(active_player)
        Animation(opacity=1, duration=0.7).start(inactive_player)

    def _transition_to_video(self, new_source, loop=True):
        """Helper method to handle the logic for transitioning between videos."""
        if self.active_player_id == 'a':
            active_player = self.ids.video_player_a
            inactive_player = self.ids.video_player_b
        else:
            active_player = self.ids.video_player_b
            inactive_player = self.ids.video_player_a
        
        if active_player.source == new_source:
            return

        inactive_player.source = new_source
        inactive_player.options['loop'] = loop # Set whether the video should loop
        inactive_player.state = 'play'
        
        if not loop:
            # If not looping, bind an event to know when the video ends
            inactive_player.bind(on_eos=self.on_touch_video_finished)

        Clock.schedule_once(self.start_transition, 0.1)

    def on_kv_post(self, base_widget):
        self.update_plant_status()

    def play_touch_video(self):
        """Called when the invisible button is pressed."""
        print("Plant touched!")
        touched_video_source = f"videos/{self.video_map['touched']}"
        self._transition_to_video(touched_video_source, loop=False)

    def on_touch_video_finished(self, video_player):
        """Called when the non-looping 'touched' video ends."""
        print("Touch video finished. Reverting to previous state.")
        # Unbind the event so it doesn't trigger again for other videos
        video_player.unbind(on_eos=self.on_touch_video_finished)
        # Trigger an update, which will revert to the last saved 'previous_state'
        self.update_plant_status()

    def toggle_camera(self):
        self.camera_active = not self.camera_active
        self.update_plant_status()

    def toggle_mic(self):
        self.mic_active = not self.mic_active
        self.update_plant_status()

    def on_fade_out_complete(self, animation, faded_out_widget):
        """Called when the old video has finished fading out."""
        faded_out_widget.state = 'stop'
        self.active_player_id = 'b' if self.active_player_id == 'a' else 'a'

    def update_plant_status(self, *args):
        moisture = self.ids.moisture_slider.value
        light = self.ids.light_slider.value
        self.ids.moisture_label.text = f"Soil Moisture: {int(moisture)}%"
        self.ids.light_label.text = f"Ambient Light: {int(light)}%"

        active_player = self.ids[f"video_player_{self.active_player_id}"]
        # If the touch video is still playing, don't change it with slider updates.
        if active_player.source.endswith(self.video_map['touched']):
            return

        if self.camera_active or self.mic_active:
            new_state = "smart"
        else:
            new_state = "happy"
            if moisture < 30:
                new_state = "thirsty"
            elif light < 20:
                new_state = "scare_of_dark"
            elif light >= 80:
                new_state = "enjoying_sun"
        
        # Save the current state so we can return to it after being touched
        self.previous_state = new_state
        video_filename = self.video_map.get(self.previous_state)
        new_video_source = f"videos/{video_filename}"
        
        self._transition_to_video(new_video_source, loop=True)


    def reset_sliders(self):
        self.ids.moisture_slider.value = 50
        self.ids.light_slider.value = 80

class PlantApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    PlantApp().run()

