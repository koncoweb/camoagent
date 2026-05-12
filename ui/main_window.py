from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPainter, QPixmap, QIcon

from ui.panels import CrewPanel, AnalyticsPanel, SettingsPanel

import os
import markdown


class IconButton(QPushButton):
    def __init__(self, icon_path: str, tooltip: str, parent=None):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setFixedSize(60, 60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: none;
                border-radius: 12px;
                padding: 8px;
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
            }
            QPushButton:pressed {
                background-color: #1D1D1D;
            }
        """)

        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(36, 36))


class EmojiButton(QPushButton):
    def __init__(self, emoji: str, tooltip: str, parent=None):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setFixedSize(60, 60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(emoji)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: none;
                border-radius: 12px;
                padding: 8px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #3D3D3D;
            }
            QPushButton:pressed {
                background-color: #1D1D1D;
            }
        """)


class IconBar(QFrame):
    icon_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(70)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-right: 1px solid #333;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(15)
        layout.addAlignment = Qt.AlignmentFlag.AlignTop

        self.browser_btn = EmojiButton("🦊", "Browser", self)
        self.browser_btn.clicked.connect(lambda: self.icon_clicked.emit("browser"))
        layout.addWidget(self.browser_btn)

        self.crew_btn = EmojiButton("🤖", "Crew", self)
        self.crew_btn.clicked.connect(lambda: self.icon_clicked.emit("crew"))
        layout.addWidget(self.crew_btn)

        self.analytics_btn = EmojiButton("📊", "Analytics", self)
        self.analytics_btn.clicked.connect(lambda: self.icon_clicked.emit("analytics"))
        layout.addWidget(self.analytics_btn)

        self.settings_btn = EmojiButton("⚙️", "Settings", self)
        self.settings_btn.clicked.connect(lambda: self.icon_clicked.emit("settings"))
        layout.addWidget(self.settings_btn)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


class StatusPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-left: 1px solid #333;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)

        title = QLabel("STATUS")
        title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: #888;")
        layout.addWidget(title)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                border: none;
                color: #CCC;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.status_text)

        self.log_browser_event("Application started")

    def log_browser_event(self, message: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.append(f"<span style='color:#888'>[{timestamp}]</span> {message}")

    def update_status(self, agent: str, status: str):
        color = "#4EC9B0" if status == "ready" else "#DCDCAA" if status == "working" else "#CE9178"
        self.log_browser_event(f"<span style='color:{color}'>[{agent}]</span> {status}")


class MainWindow(QFrame):
    def __init__(self, browser_manager, crew_executor):
        super().__init__()
        self.browser_manager = browser_manager
        self.crew_executor = crew_executor

        self.setWindowTitle("CamoAgent - Super Agent Browser")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #1E1E1E;")

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)

        self.icon_bar = IconBar()
        self.icon_bar.icon_clicked.connect(self.on_icon_clicked)
        main_layout.addWidget(self.icon_bar)

        self.stacked_widget = QStackedWidget()

        self.chat_widget = ChatWidget()
        self.stacked_widget.addWidget(self.chat_widget)

        self.crew_panel = CrewPanel()
        self.stacked_widget.addWidget(self.crew_panel)

        self.analytics_panel = AnalyticsPanel()
        self.stacked_widget.addWidget(self.analytics_panel)

        self.settings_panel = SettingsPanel()
        self.stacked_widget.addWidget(self.settings_panel)

        main_layout.addWidget(self.stacked_widget, stretch=1)

        self.status_panel = StatusPanel()
        main_layout.addWidget(self.status_panel)

    def setup_connections(self):
        self.chat_widget.send_message.connect(self.on_chat_message)
        self.crew_executor.status_update.connect(self.status_panel.update_status)
        self.crew_executor.status_update.connect(self.crew_panel.update_status)
        self.crew_executor.message_ready.connect(self.chat_widget.add_agent_message)
        
        self.settings_panel.settings_changed.connect(self.on_settings_changed)
        
        self.browser_manager.browser_ready.connect(lambda: self.status_panel.log_browser_event("Browser is ready!"))
        self.browser_manager.error_occurred.connect(lambda e: self.status_panel.log_browser_event(f"Browser Error: {e}"))
        self.browser_manager.browser_closed.connect(lambda: self.status_panel.log_browser_event("Browser closed"))

    def on_icon_clicked(self, icon_name: str):
        if icon_name == "browser":
            self.browser_manager.launch_browser()
            self.status_panel.log_browser_event("Launching Camoufox browser...")
            self.stacked_widget.setCurrentWidget(self.chat_widget)
        elif icon_name == "crew":
            self.status_panel.log_browser_event("Crew Configuration panel opened")
            self.stacked_widget.setCurrentWidget(self.crew_panel)
        elif icon_name == "analytics":
            self.status_panel.log_browser_event("Analytics panel opened")
            self.stacked_widget.setCurrentWidget(self.analytics_panel)
        elif icon_name == "settings":
            self.status_panel.log_browser_event("Settings panel opened")
            self.stacked_widget.setCurrentWidget(self.settings_panel)

    def on_settings_changed(self, settings: dict):
        self.crew_executor.update_settings(settings)
        self.status_panel.log_browser_event(f"Settings updated: Model={settings['model']}, MaxIter={settings['max_iter']}, Memory={settings['memory']}, Planning={settings['planning']}")

    def on_chat_message(self, message: str):
        self.chat_widget.add_user_message(message)
        self.status_panel.log_browser_event(f"User: {message[:50]}...")
        self.crew_executor.execute_task(message, self.browser_manager.get_page())


class ChatWidget(QFrame):
    send_message = pyqtSignal(str)
    message_ready = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #252526;
                border-radius: 8px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("💬 Chat Assistant")
        header.setStyleSheet("""
            QLabel {
                background-color: #2D2D30;
                color: white;
                padding: 12px 16px;
                font-size: 14px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        header.setFixedHeight(45)
        layout.addWidget(header)

        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("""
            QScrollArea {
                background-color: #1E1E1E;
                border: none;
            }
        """)
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_area.setWidget(self.chat_content)
        layout.addWidget(self.chat_area, stretch=1)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(12, 12, 12, 12)

        from PyQt6.QtWidgets import QLineEdit
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your command...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #3C3C3C;
                border: none;
                border-radius: 20px;
                padding: 12px 20px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                outline: 2px solid #007ACC;
            }
        """)
        self.message_input.returnPressed.connect(self.on_send_clicked)
        input_layout.addWidget(self.message_input)

        send_btn = QPushButton("Send")
        send_btn.setFixedSize(70, 40)
        send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E90FF;
            }
        """)
        send_btn.clicked.connect(self.on_send_clicked)
        input_layout.addWidget(send_btn)

        layout.addLayout(input_layout)

    def on_send_clicked(self):
        message = self.message_input.text().strip()
        if message:
            self.send_message.emit(message)
            self.message_input.clear()

    def add_user_message(self, message: str):
        msg_widget = QLabel(message)
        msg_widget.setWordWrap(True)
        msg_widget.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        msg_widget.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                background-color: #2D2D30;
                padding: 10px 14px;
                border-radius: 12px;
                font-size: 13px;
                margin-left: 20px;
                margin-top: 6px;
                margin-bottom: 6px;
            }
        """)
        # Set max width to prevent it from stretching across the entire screen
        msg_widget.setMaximumWidth(380)
        self.chat_layout.addWidget(msg_widget, 0, Qt.AlignmentFlag.AlignRight)

    def add_agent_message(self, message: str):
        html_content = markdown.markdown(
            f"🤖 **Assistant:**\n\n{message}",
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        
        styled_html = f"""
        <html>
        <head>
        <style>
        body {{
            color: #4EC9B0;
            background-color: #2D2D30;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            padding: 16px;
            margin: 0;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #4EC9B0;
            margin-top: 12px;
            margin-bottom: 8px;
        }}
        p {{
            margin: 8px 0;
        }}
        strong {{
            color: #FFFFFF;
        }}
        em {{
            color: #CE9178;
        }}
        code {{
            background-color: #1E1E1E;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Courier New', monospace;
            color: #DCDCAA;
        }}
        pre {{
            background-color: #1E1E1E;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }}
        th, td {{
            border: 1px solid #3C3C3C;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #1E1E1E;
            color: #4EC9B0;
        }}
        tr:nth-child(even) {{
            background-color: #252526;
        }}
        a {{
            color: #569CD6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            margin: 8px 0;
            padding-left: 24px;
        }}
        li {{
            margin: 4px 0;
        }}
        blockquote {{
            border-left: 4px solid #4EC9B0;
            margin: 10px 0;
            padding: 8px 16px;
            background-color: #252526;
            color: #9CDCFE;
        }}
        </style>
        </head>
        <body>{html_content}</body>
        </html>
        """
        
        msg_widget = QTextEdit()
        msg_widget.setReadOnly(True)
        msg_widget.setHtml(styled_html)
        msg_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msg_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msg_widget.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        msg_widget.setStyleSheet("""
            QTextEdit {
                background-color: #2D2D30;
                border: none;
                border-radius: 12px;
                margin-right: 15px;
                margin-top: 6px;
                margin-bottom: 6px;
            }
        """)
        
        # Calculate height based on content
        doc = msg_widget.document()
        doc.setTextWidth(420) # Fixed width for height calculation
        height = int(doc.size().height()) + 25
        msg_widget.setFixedHeight(height)
        msg_widget.setFixedWidth(440)
        
        self.chat_layout.addWidget(msg_widget, 0, Qt.AlignmentFlag.AlignLeft)
