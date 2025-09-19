from kivy.app import App
from kivy.uix.video import Video

class TestApp(App):
    def build(self):
        return Video(
            source=r"c:\Users\edwar\OneDrive\Documents\Programming\MiniProject\videos\Plant_Swaying_Video_Generation.mp4",
            state="play",
            options={'eos': 'loop'}
        )

if __name__ == "__main__":
    TestApp().run()
