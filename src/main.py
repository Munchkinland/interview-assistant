import sys
from PyQt5.QtWidgets import QApplication
from gui import InterviewAssistantGUI

def main():
  app = QApplication(sys.argv)
  window = InterviewAssistantGUI()
  window.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()