import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer
from game.game_logic import Game, Player
from ai.ai_interface import generate_ai_response

# Disable GPU hardware acceleration for Qt rendering
os.environ["QT_QUICK_BACKEND"] = "software"

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.setWindowTitle("AI-Powered Adventure Game")
        self.setGeometry(100, 100, 750, 550)
        self.setStyleSheet("background-color: #1e1e1e;")  # Dark background

        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        main_widget.setLayout(self.layout)

        # Font setup for different sections
        story_font = QFont("Georgia", 13)
        input_font = QFont("Helvetica", 11, QFont.Bold)

        # Story Display Area with gradient background and padding (using QPlainTextEdit)
        self.story_text = QPlainTextEdit(self)
        self.story_text.setReadOnly(True)
        self.story_text.setFont(story_font)
        self.story_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide scrollbar
        self.story_text.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2e2e2e, stop:1 #c42727);
            color: #ffffff;  /* White text */
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #444;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5);
        """)
        self.layout.addWidget(self.story_text)

        # Input Frame for Entry and Button with spacing
        self.input_frame = QHBoxLayout()
        self.input_frame.setSpacing(10)
        self.layout.addLayout(self.input_frame)

        # User Input Field with subtle gradient and rounded corners
        self.entry = QLineEdit(self)
        self.entry.setFont(input_font)
        self.entry.setStyleSheet("""
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #3e3e3e, stop:1 #2e2e2e);
            color: #ffffff;  /* White text */
            padding: 8px;
            border-radius: 10px;
            border: 1px solid #555;
            margin-right: 5px;
        """)
        self.entry.setPlaceholderText("Type your choice here...")
        self.input_frame.addWidget(self.entry)

        # Submit Button with vibrant color accent
        self.send_button = QPushButton("Submit", self)
        self.send_button.setFont(input_font)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #43868a, stop:1 #0b2659);
                color: #ffffff;  /* White text */
                padding: 8px 20px;
                border-radius: 10px;
                border: 1px solid #5b7dbd;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #9dabc4, stop:1 #4d6799);
            }
            QPushButton:pressed {
                background-color: #5e35b1;
            }
        """)
        self.send_button.clicked.connect(self.submit_choice)
        self.input_frame.addWidget(self.send_button)

        # Continue Button to let AI generate the next part of the story
        self.continue_button = QPushButton("Continue", self)
        self.continue_button.setFont(input_font)
        self.continue_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #3b5998, stop:1 #8b9dc3);
                color: #ffffff;
                padding: 8px 20px;
                border-radius: 10px;
                border: 1px solid #3b5998;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #4a69b1, stop:1 #9faed8);
            }
            QPushButton:pressed {
                background-color: #344e86;
            }
        """)
        self.continue_button.clicked.connect(self.continue_story)
        self.input_frame.addWidget(self.continue_button)

        # Connect Enter key with the button
        self.entry.returnPressed.connect(self.submit_choice)

        # Initialize game logic
        self.player = Player("Hero")

        # Initialize typing effect attributes
        self.typing_text = ""
        self.current_char_index = 0

        # Initialize the game and set callback
        self.game = Game(self.player, self.show_text_typing_effect)
        self.game.start_game()

    def show_text_typing_effect(self, text, use_typing=True):
        """Initialize the typing effect with optional direct display for debugging."""
        if use_typing:
            self.typing_text = text
            self.current_char_index = 0
            self.story_text.appendPlainText("")  # Add a new line for typing effect
            self.type_next_chunk()  # Start the typing effect
        else:
            self.story_text.appendPlainText(text)  # Show the full text directly

    def type_next_chunk(self):
        """Add the next chunk of characters to the text area."""
        chunk_size = 5  # Number of characters to add per update
        if self.current_char_index < len(self.typing_text):
            # Append the next chunk of text
            next_chunk = self.typing_text[self.current_char_index:self.current_char_index + chunk_size]
            self.story_text.insertPlainText(next_chunk)
            self.current_char_index += chunk_size

            # Schedule the next update with singleShot for smoother control
            QTimer.singleShot(100, self.type_next_chunk)
        else:
            # Typing effect completed
            pass

    def submit_choice(self):
        """Handle the user's choice submission."""
        user_input = self.entry.text()
        if user_input:
            self.show_text_typing_effect(f"\n> {user_input}", use_typing=False)
            self.entry.clear()
            self.game.process_choice(user_input)

    def continue_story(self):
        """Let the AI continue generating the story without user input."""
        self.show_text_typing_effect("\n> Continue...", use_typing=False)

        try:
            ai_generated_text = generate_ai_response("Continue the story")  # Make sure generate_ai_response works
            self.show_text_typing_effect(ai_generated_text, use_typing=False)
        except Exception as e:
            print(f"Error generating AI response: {e}")
            self.show_text_typing_effect("An error occurred while generating the AI response.", use_typing=False)

def main():
    app = QApplication(sys.argv)

    # Set global application palette for a dark theme
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor("#1e1e1e"))
    dark_palette.setColor(QPalette.WindowText, QColor("white"))
    dark_palette.setColor(QPalette.Base, QColor("#2e2e2e"))
    dark_palette.setColor(QPalette.AlternateBase, QColor("#3e3e3e"))
    dark_palette.setColor(QPalette.ToolTipBase, QColor("white"))
    dark_palette.setColor(QPalette.ToolTipText, QColor("white"))
    dark_palette.setColor(QPalette.Text, QColor("white"))
    dark_palette.setColor(QPalette.Button, QColor("#3e3e3e"))
    dark_palette.setColor(QPalette.ButtonText, QColor("white"))
    dark_palette.setColor(QPalette.BrightText, QColor("red"))
    dark_palette.setColor(QPalette.Highlight, QColor("#777777"))
    dark_palette.setColor(QPalette.HighlightedText, QColor("black"))
    app.setPalette(dark_palette)

    # Create and show the main window
    window = GameWindow()
    window.show()

    # Run the application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()