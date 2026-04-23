import product
import numpy as np

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QSlider, QFrame, QCheckBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt


class EmotionSlider(QWidget):
    def __init__(self, title):
        super().__init__()

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.update_value)

        self.left_label = QLabel("0.00")
        self.right_label = QLabel("1.00")

        self.value_label = QLabel("0.50")
        self.value_label.setAlignment(Qt.AlignCenter)
        self.value_label.setStyleSheet("font-size: 14px;")

        slider_row = QHBoxLayout()
        slider_row.addWidget(self.left_label)
        slider_row.addWidget(self.slider)
        slider_row.addWidget(self.right_label)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addLayout(slider_row)
        layout.addWidget(self.value_label)
        self.setLayout(layout)

    def update_value(self):
        self.value_label.setText(f"{self.get_value():.2f}")

    def get_value(self):
        return self.slider.value() / 100.0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Song Emotion Generator")
        self.resize(1000, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: black;
                background: transparent;
                border: none;
            }
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                padding: 10px 24px;
                min-width: 160px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2c5f99;
            }
            QFrame {
                background: white;
                border: 1px solid #999;
                border-radius: 6px;
            }
            QCheckBox {
                font-size: 15px;
                color: black;
            }                           
        """)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(8)
        central.setLayout(main_layout)

        title = QLabel("What we feeling:")
        title.setStyleSheet("font-size: 28px; font-weight: bold; border: none; background: transparent;")
        main_layout.addWidget(title)

        now_label = QLabel("Now:")
        now_label.setStyleSheet("font-size: 20px; font-weight: bold; border: none; background: transparent;")
        main_layout.addWidget(now_label)

        self.now_sad_happy = EmotionSlider("Sad — Happy")
        self.now_calm_energetic = EmotionSlider("Calm — Energetic")
        self.now_relaxed_stressed = EmotionSlider("Relaxed — Stressed")

        now_grid = QGridLayout()
        now_grid.setHorizontalSpacing(20)
        now_grid.setVerticalSpacing(10)
        now_grid.addWidget(self.now_sad_happy, 0, 0)
        now_grid.addWidget(self.now_calm_energetic, 0, 1)
        now_grid.addWidget(self.now_relaxed_stressed, 0, 2)
        main_layout.addLayout(now_grid)

        want_label = QLabel("Want to achieve:")
        want_label.setStyleSheet("font-size: 20px; font-weight: bold; border: none; background: transparent;")
        main_layout.addWidget(want_label)

        self.want_sad_happy = EmotionSlider("Sad — Happy")
        self.want_calm_energetic = EmotionSlider("Calm — Energetic")
        self.want_relaxed_stressed = EmotionSlider("Relaxed — Stressed")

        want_grid = QGridLayout()
        want_grid.setHorizontalSpacing(20)
        want_grid.setVerticalSpacing(10)
        want_grid.addWidget(self.want_sad_happy, 0, 0)
        want_grid.addWidget(self.want_calm_energetic, 0, 1)
        want_grid.addWidget(self.want_relaxed_stressed, 0, 2)
        main_layout.addLayout(want_grid)

        self.explicit_checkbox = QCheckBox("Include explicit songs")
        self.explicit_checkbox.setChecked(False)
        checkbox_row = QHBoxLayout()
        checkbox_row.addStretch()
        checkbox_row.addWidget(self.explicit_checkbox)
        checkbox_row.addStretch()
        main_layout.addLayout(checkbox_row)

        button_row = QHBoxLayout()
        button_row.addStretch()

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_song)
        button_row.addWidget(self.generate_button)

        button_row.addStretch()
        main_layout.addLayout(button_row)

        self.song_box = QFrame()
        song_layout = QVBoxLayout()
        song_layout.setContentsMargins(12, 12, 12, 12)
        song_layout.setSpacing(8)

        self.song_text = QLabel("No song generated yet.")
        self.song_text.setStyleSheet("font-size: 16px;")
        self.song_text.setWordWrap(True)
        self.song_text.setTextFormat(Qt.RichText)
        self.song_text.setOpenExternalLinks(True)
        self.song_text.setTextInteractionFlags(Qt.TextBrowserInteraction)

        song_layout.addWidget(self.song_text)

        self.song_box.setLayout(song_layout)
        main_layout.addWidget(self.song_box)

        # Added feature, spotify html embed 
        # self.song_html = QWebEngineView()
        # self.song_html.setHtml("""""")
        # song_layout.addWidget(self.song_html) 

    def generate_song(self):
        current_emotion = np.array([
            self.now_sad_happy.get_value(),
            self.now_calm_energetic.get_value(),
            self.now_relaxed_stressed.get_value()
        ])

        goal_emotion = np.array([
            self.want_sad_happy.get_value(),
            self.want_calm_energetic.get_value(),
            self.want_relaxed_stressed.get_value()
        ])

        delta_emotion = tuple(goal_emotion - current_emotion)

        try:

            include_explicit = self.explicit_checkbox.isChecked()
            skip_explicit = not include_explicit

            song = product.get_closest_song(delta_emotion, skip_explicit=skip_explicit)
            song_name = song["name"]
            song_link = song["song_link"]
            song_id = song['id']
            self.song_text.setText(
                f"<div style='font-size:16px;'>"
                f"<a href='{song_link}'><b>{song_name}</b></a><br>"
                f"</div>"
            )
#             spotify_embed = f"""
# <iframe style="border-radius:12px" 
#     src="https://open.spotify.com/embed/track/{song_id}?utm_source=generator" 
#     width="100%" height="100%" frameBorder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
# </iframe>
# """
#             self.song_html.setHtml(spotify_embed)
        except Exception as e:
            self.song_text.setText(f"Error: {e}")