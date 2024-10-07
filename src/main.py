from kivy.app import App
from gui_kivy import InterviewAssistantGUI

class InterviewAssistantApp(App):
  def build(self):
      return InterviewAssistantGUI()

def main():
  InterviewAssistantApp().run()

if __name__ == "__main__":
  main()