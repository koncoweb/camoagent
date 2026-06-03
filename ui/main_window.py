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
                background-color: #FFFFFF;
                border: none;
                border-radius: 12px;
                padding: 8px;
                font-size: 28px;
            }
            QPushButton:hover {
                background-color: #FFF0E6;
            }
            QPushButton:pressed {
                background-color: #FFE0CC;
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
                background-color: #FFFFFF;
                border: 2px solid #EE4D2D;
                border-radius: 12px;
                padding: 8px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #FFF0E6;
                border-color: #FF6347;
            }
            QPushButton:pressed {
                background-color: #FFE0CC;
            }
        """)


class IconBar(QFrame):
    icon_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(70)
        self.setStyleSheet("""
            QFrame {
                background-color: #EE4D2D;
                border-right: 2px solid #CC3D1D;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(12)
        layout.addAlignment = Qt.AlignmentFlag.AlignTop

        self.browser_btn = EmojiButton("🛒", "Shopee Browser", self)
        self.browser_btn.clicked.connect(lambda: self.icon_clicked.emit("browser"))
        layout.addWidget(self.browser_btn)

        self.ads_btn = EmojiButton("📢", "Shopee Ads", self)
        self.ads_btn.clicked.connect(lambda: self.icon_clicked.emit("ads"))
        layout.addWidget(self.ads_btn)

        self.spy_btn = EmojiButton("🕵️", "Spy Agent - Market Research", self)
        self.spy_btn.clicked.connect(lambda: self.icon_clicked.emit("spy"))
        layout.addWidget(self.spy_btn)

        self.crew_btn = EmojiButton("🤖", "AI Crew", self)
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
                background-color: #FFFAF5;
                border-left: 2px solid #F5A623;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 15, 10, 15)

        title = QLabel("📋 STATUS")
        title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: #EE4D2D;")
        layout.addWidget(title)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #F5A623;
                border-radius: 8px;
                color: #333333;
                font-family: 'Consolas', monospace;
                font-size: 11px;
                padding: 8px;
            }
        """)
        layout.addWidget(self.status_text)

        self.log_browser_event("ShopeeAgent started")

    def log_browser_event(self, message: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.append(f"<span style='color:#EE4D2D'>[{timestamp}]</span> {message}")

    def update_status(self, agent: str, status: str):
        color = "#28A745" if status == "ready" else "#F5A623" if status == "working" else "#DC3545"
        self.log_browser_event(f"<span style='color:{color}'>[{agent}]</span> {status}")


class MainWindow(QFrame):
    def __init__(self, browser_manager, crew_executor):
        super().__init__()
        self.browser_manager = browser_manager
        self.crew_executor = crew_executor

        self._spy_session_active = False
        self._spy_browser_open = False
        self._ads_session_active = False

        self.setWindowTitle("ShopeeAgent - AI Shopee Manager")
        self.setFixedSize(900, 650)
        self.setStyleSheet("background-color: #FFF5F0;")

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)

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

        main_layout.addWidget(self.stacked_widget, stretch=1)

        self.status_panel = StatusPanel()
        main_layout.addWidget(self.status_panel)

    def setup_connections(self):
        self.chat_widget.send_message.connect(self.on_chat_message)
        self.crew_executor.status_update.connect(self.status_panel.update_status)
        self.crew_executor.status_update.connect(self.crew_panel.update_status)
        self.crew_executor.message_ready.connect(self.chat_widget.add_agent_message)
        
        self.browser_manager.browser_ready.connect(lambda: self.status_panel.log_browser_event("Shopee Browser ready!"))
        self.browser_manager.error_occurred.connect(lambda e: self.status_panel.log_browser_event(f"Browser Error: {e}"))
        self.browser_manager.browser_closed.connect(lambda: self.status_panel.log_browser_event("Browser closed"))

    def on_icon_clicked(self, icon_name: str):
        if icon_name == "settings":
            self._open_settings_dialog()
            return

        if icon_name == "crew" or icon_name == "analytics":
            self.status_panel.log_browser_event("Panel opened — chat session preserved")
            if icon_name == "crew":
                self.stacked_widget.setCurrentWidget(self.crew_panel)
            else:
                self.stacked_widget.setCurrentWidget(self.analytics_panel)
            return

        if self._spy_session_active and icon_name != "spy":
            self.stacked_widget.setCurrentWidget(self.chat_widget)
            self.status_panel.log_browser_event("🕵️ Returned to Spy Agent session")
            return

        if self._ads_session_active and icon_name not in ("ads", "browser"):
            self.stacked_widget.setCurrentWidget(self.chat_widget)
            self.status_panel.log_browser_event("📢 Returned to Ads session")
            return

        if icon_name == "browser":
            self._spy_session_active = False
            self._ads_session_active = False
            self.chat_widget.set_spy_mode(False)
            self.chat_widget.clear_chat()
            self.browser_manager.launch_browser()
            self.status_panel.log_browser_event("Launching Shopee Seller Center...")
            self.stacked_widget.setCurrentWidget(self.chat_widget)
        elif icon_name == "ads":
            if not self.browser_manager.is_ready():
                self.status_panel.log_browser_event("⚠️ Please open the browser first by clicking 🛒 icon")
                self.chat_widget.add_user_message("⚠️ Please open the browser first by clicking the 🛒 icon, then navigate to Shopee Ads dashboard manually.")
                return
            self._spy_session_active = False
            self._ads_session_active = True
            self.chat_widget.set_spy_mode(False)
            self.chat_widget.clear_chat()
            self.status_panel.log_browser_event("🔍 Starting Shopee Ads Analysis...")
            self.stacked_widget.setCurrentWidget(self.chat_widget)
            self.chat_widget.add_user_message("🔍 **Starting Shopee Ads Analysis...**")
            self.crew_executor.execute_shopee_ads_task(
                task_description="Analyze Shopee ads performance",
                page=self.browser_manager.get_page()
            )
        elif icon_name == "spy":
            if self._spy_session_active:
                self.stacked_widget.setCurrentWidget(self.chat_widget)
                self.status_panel.log_browser_event("🕵️ Returned to Spy Agent session")
                return
            self._ads_session_active = False
            self._handle_spy_agent_click()

    def on_settings_changed(self, settings: dict):
        self.crew_executor.update_settings(settings)
        self.status_panel.log_browser_event(f"Settings: Model={settings['model']}, MaxIter={settings['max_iter']}")

    def _open_settings_dialog(self):
        dialog = SettingsPanel(self)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec()

    def _handle_spy_agent_click(self):
        if self.browser_manager.is_ready():
            self.status_panel.log_browser_event("Closing existing browser for Spy Agent...")
            self.browser_manager.close()

        self._spy_session_active = True
        self.status_panel.log_browser_event("🕵️ Launching Spy Agent - Shopee Marketplace...")
        self.stacked_widget.setCurrentWidget(self.chat_widget)

        self.chat_widget.clear_chat()
        self.chat_widget.set_context_header("🕵️ Spy Agent - Market Research")
        self.chat_widget.add_user_message(
            "🕵️ **Spy Agent - Market Research**\n\n"
            "**Langkah:**\n"
            "1. Cari produk atau browse kategori di browser\n"
            "2. Klik tombol aksi di atas untuk mulai analisis\n\n"
            "_Spy Agent scan sebagai pembeli biasa — tidak perlu login._"
        )

        self.browser_manager.launch_browser(target_url="https://shopee.co.id")
        self.chat_widget.set_spy_mode(True)

    def _on_spy_action(self, action: str):
        if action == "scan_market":
            self.status_panel.log_browser_event("🕵️ Starting Market Scan...")
            self.chat_widget.add_user_message("📡 **Scanning Shopee Marketplace...**\n\nExtracting all products with structured DOM extraction...")
            self.crew_executor.execute_spy_task(
                task_description="Use scan_shopee_market to extract ALL product data from the current search results. Use extract_structured=True for accurate JSON data.",
                page=self.browser_manager.get_page()
            )
        elif action == "review_mine":
            self.status_panel.log_browser_event("🕵️ Starting Review Mining...")
            self.chat_widget.add_user_message("💬 **Mining Customer Reviews...**\n\nExtracting pain points & strengths from reviews...\n\nNavigate to a product page first, then click the button.")
            self.crew_executor.execute_spy_task(
                task_description="Navigate to a top-selling product page, click the Reviews tab, then use mine_product_reviews to extract customer sentiment. Identify pain points (1-2 stars) and strengths (4-5 stars).",
                page=self.browser_manager.get_page()
            )
        elif action == "store_profile":
            self.status_panel.log_browser_event("🕵️ Starting Store Profiling...")
            self.chat_widget.add_user_message("🏪 **Analyzing Competitor Store...**\n\nExtracting store metrics, rating, followers, badges...\n\nNavigate to a store page first, then click the button.")
            self.crew_executor.execute_spy_task(
                task_description="Use profile_shopee_store on the current store page. Extract name, rating, followers, product count, badges, and official status. Then use scan_shopee_market to scan the store's products.",
                page=self.browser_manager.get_page()
            )
        elif action == "full_report":
            self.status_panel.log_browser_event("🕵️ Starting Full Market Intelligence...")
            self.chat_widget.add_user_message("🎯 **Full Market Intelligence Report**\n\nRunning complete analysis pipeline:\n1. 📡 Market Scan\n2. 📊 Competitor Analysis\n3. 📈 Trend Detection\n4. 💬 Review Mining\n5. 🎯 Strategy Synthesis\n\nThis may take 5-8 minutes...")
            self.crew_executor.execute_spy_task(
                task_description="Run COMPLETE market intelligence: 1) scan_shopee_market for ALL products, 2) analyze_market_gaps for opportunities, 3) Navigate to top 3 competitor product pages and mine_product_reviews, 4) Generate comprehensive strategy report with Executive Summary, Competitor Landscape, Gap Opportunities, Customer Pain Points, Keyword Recommendations, Pricing Strategy, and Risk Assessment.",
                page=self.browser_manager.get_page()
            )
        elif action == "":
            pass

    def on_chat_message(self, message: str):
        if message == "__SPY_START__":
            self._on_spy_action("full_report")
            return
        if message.startswith("__SPY_ACTION__:"):
            action = message.split("__SPY_ACTION__:")[1]
            self._on_spy_action(action)
            return

        self.chat_widget.add_user_message(message)
        self.status_panel.log_browser_event(f"You: {message[:50]}...")
        self.crew_executor.execute_task(message, self.browser_manager.get_page())


class ChatWidget(QFrame):
    send_message = pyqtSignal(str)
    message_ready = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._spy_mode = False
        self._spy_start_btn = None
        self._chat_header_label = None
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("� Shopee Assistant")
        header.setStyleSheet("""
            QLabel {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EE4D2D, stop:1 #FF6347);
                color: white;
                padding: 14px 16px;
                font-size: 15px;
                font-weight: bold;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        header.setFixedHeight(48)
        layout.addWidget(header)

        self._chat_header_label = QLabel("")
        self._chat_header_label.setStyleSheet("""
            QLabel {
                background-color: #28A745;
                color: white;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        self._chat_header_label.setFixedHeight(0)
        self._chat_header_label.hide()
        layout.addWidget(self._chat_header_label)

        # SpyAgent Action Bar
        self._spy_action_bar = QWidget()
        self._spy_action_bar.setStyleSheet("background-color: #F0FFF0; border-bottom: 2px solid #28A745;")
        spy_action_layout = QHBoxLayout(self._spy_action_bar)
        spy_action_layout.setContentsMargins(8, 6, 8, 6)
        spy_action_layout.setSpacing(6)

        actions = [
            ("📡 Scan", "scan_market", "#28A745", "Extract product data from current search"),
            ("💬 Reviews", "review_mine", "#17A2B8", "Mine customer reviews for insights"),
            ("🏪 Store", "store_profile", "#6F42C1", "Profile competitor store"),
            ("🎯 Full Report", "full_report", "#EE4D2D", "Complete market intelligence report"),
        ]

        for label, action_id, color, tooltip in actions:
            btn = QPushButton(f" {label} ")
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 6px 14px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #333333;
                }}
            """)
            btn.clicked.connect(lambda checked, a=action_id: self.send_message.emit(f"__SPY_ACTION__:{a}"))
            spy_action_layout.addWidget(btn)

        spy_action_layout.addStretch()
        self._spy_action_bar.hide()
        layout.addWidget(self._spy_action_bar)

        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("""
            QScrollArea {
                background-color: #FFF8F5;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #FFE0CC;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #EE4D2D;
                border-radius: 4px;
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
        self.message_input.setPlaceholderText("Type your command for Shopee...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #F5A623;
                border-radius: 20px;
                padding: 12px 20px;
                color: #333333;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #EE4D2D;
            }
        """)
        self.message_input.returnPressed.connect(self.on_send_clicked)
        input_layout.addWidget(self.message_input)

        send_btn = QPushButton("Send")
        send_btn.setFixedSize(80, 42)
        send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        send_btn.setStyleSheet("""
            QPushButton {
                background-color: #EE4D2D;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #FF6347;
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
                color: #FFFFFF;
                background-color: #EE4D2D;
                padding: 10px 14px;
                border-radius: 16px;
                border-bottom-right-radius: 4px;
                font-size: 13px;
                margin-left: 20px;
                margin-top: 6px;
                margin-bottom: 6px;
            }
        """)
        msg_widget.setMaximumWidth(400)
        self.chat_layout.addWidget(msg_widget, 0, Qt.AlignmentFlag.AlignRight)

    def add_agent_message(self, message: str):
        html_content = markdown.markdown(
            f"🤖 **Shopee Assistant:**\n\n{message}",
            extensions=['tables', 'fenced_code', 'nl2br']
        )
        
        styled_html = f"""
        <html>
        <head>
        <style>
        body {{
            color: #333333;
            background-color: #FFF0E6;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            padding: 16px;
            margin: 0;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #EE4D2D;
            margin-top: 12px;
            margin-bottom: 8px;
        }}
        p {{
            margin: 8px 0;
        }}
        strong {{
            color: #CC3D1D;
        }}
        em {{
            color: #666666;
        }}
        code {{
            background-color: #FFFFFF;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Consolas', 'Courier New', monospace;
            color: #EE4D2D;
        }}
        pre {{
            background-color: #FFFFFF;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #F5A623;
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
            border: 1px solid #F5A623;
            padding: 8px 12px;
            text-align: left;
        }}
        th {{
            background-color: #EE4D2D;
            color: #FFFFFF;
        }}
        tr:nth-child(even) {{
            background-color: #FFF8F5;
        }}
        a {{
            color: #EE4D2D;
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
            border-left: 4px solid #EE4D2D;
            margin: 10px 0;
            padding: 8px 16px;
            background-color: #FFFFFF;
            color: #666666;
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
                background-color: #FFF0E6;
                border: none;
                border-radius: 12px;
                margin-right: 15px;
                margin-top: 6px;
                margin-bottom: 6px;
            }
        """)
        
        doc = msg_widget.document()
        doc.setTextWidth(420)
        height = int(doc.size().height()) + 25
        msg_widget.setFixedHeight(height)
        msg_widget.setFixedWidth(440)
        
        self.chat_layout.addWidget(msg_widget, 0, Qt.AlignmentFlag.AlignLeft)

    def set_spy_mode(self, active: bool):
        if active:
            self._spy_mode = True
            self._spy_action_bar.show()
            self.message_input.setPlaceholderText("Type command or use action buttons above...")
            if hasattr(self, '_spy_start_btn') and self._spy_start_btn:
                pass
            else:
                self._spy_start_btn = QPushButton("🔍 Start Analysis")
                self._spy_start_btn.setFixedSize(150, 42)
                self._spy_start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                self._spy_start_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #28A745;
                        color: white;
                        border: none;
                        border-radius: 20px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #34D058;
                    }
                """)
                self._spy_start_btn.clicked.connect(self._on_spy_start)
            parent_layout = self.message_input.parent()
            if parent_layout and self._spy_start_btn not in [parent_layout.itemAt(i).widget() for i in range(parent_layout.count())]:
                insert_idx = parent_layout.count() - 1
                parent_layout.insertWidget(insert_idx, self._spy_start_btn)
        else:
            self._spy_mode = False
            self._spy_action_bar.hide()
            self.message_input.setPlaceholderText("Type your command for Shopee...")
            if hasattr(self, '_spy_start_btn') and self._spy_start_btn:
                self._spy_start_btn.setParent(None)
                self._spy_start_btn.deleteLater()
                self._spy_start_btn = None
            if hasattr(self, '_chat_header_label') and self._chat_header_label:
                self._chat_header_label.setText("")
                self._chat_header_label.setFixedHeight(0)
                self._chat_header_label.hide()

    def _on_spy_start(self):
        self.send_message.emit("__SPY_START__")

    def clear_chat(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def set_context_header(self, text: str):
        if hasattr(self, '_chat_header_label') and self._chat_header_label:
            self._chat_header_label.setText(f"  {text}")
            self._chat_header_label.setFixedHeight(28)
            self._chat_header_label.show()
