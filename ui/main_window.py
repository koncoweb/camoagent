from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QTextEdit, QScrollArea, QLineEdit,
    QFrame, QSizePolicy, QSpacerItem, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPainter, QPixmap, QIcon

from ui.panels import CrewPanel, AnalyticsPanel, SettingsPanel

import os
import markdown

# ── Elegant palette ─────────────────────────────────────────────
ACCENT   = "#4A90D9"   # professional blue
ACCENT_H = "#357ABD"
SUCCESS  = "#4CAF50"
ERROR    = "#C62828"
WARNING  = "#E65100"
SIDEBAR  = "#2B2B2B"
SIDEBAR_H="#3C3C3C"
PAGE_BG  = "#F5F5F5"
CARD_BG  = "#FFFFFF"
TEXT     = "#1A1A1A"
TEXT_MUTED="#666666"
TEXT_SUB  ="#999999"
BORDER   = "#E0E0E0"

# ── Shopee popular categories (Indonesia) ───────────────────────
SHOPEE_CATEGORIES = [
    ("📱 Handphone & Aksesoris",      "Handphone & Aksesoris"),
    ("👗 Fashion Wanita",              "Fashion Wanita"),
    ("👕 Fashion Pria",                "Fashion Pria"),
    ("💄 Kecantikan",                  "Kecantikan"),
    ("🍜 Makanan & Minuman",           "Makanan & Minuman"),
    ("🏠 Perlengkapan Rumah",          "Perlengkapan Rumah"),
    ("🎮 Elektronik",                  "Elektronik"),
    ("👶 Ibu & Bayi",                  "Ibu & Bayi"),
    ("🏋️ Olahraga & Outdoor",          "Olahraga & Outdoor"),
    ("📚 Buku & Alat Tulis",           "Buku & Alat Tulis"),
    ("🐶 Hewan Peliharaan",            "Hewan Peliharaan"),
    ("🚗 Otomotif",                    "Otomotif"),
    ("💊 Kesehatan",                   "Kesehatan"),
    ("🎁 Voucher & Layanan",           "Voucher & Layanan"),
]


class LoadingWidget(QFrame):
    """Animated loading indicator shown while agents are executing."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(52)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #EEF4FB;
                border: 1px solid {ACCENT};
                border-radius: 8px;
            }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(10)

        # simple text-based spinner that we'll animate with a timer
        self._spinner = QLabel("◌")
        self._spinner.setFont(QFont("Segoe UI", 18))
        self._spinner.setStyleSheet(f"color: {ACCENT}; border: none; background: transparent;")
        self._spinner.setFixedWidth(30)
        layout.addWidget(self._spinner)

        self._label = QLabel("Agent is working...")
        self._label.setStyleSheet(f"color: {TEXT}; font-size: 12px; border: none; background: transparent;")
        layout.addWidget(self._label, stretch=1)
        layout.addStretch()

        # animation state
        self._frames = ["◌", "◌", "○", "◎", "◉", "●", "◉", "◎", "○"]
        self._idx = 0
        self._timer = None

    def start(self, text: str = "Agent is working..."):
        self._label.setText(text)
        self.show()
        if self._timer is None:
            from PyQt6.QtCore import QTimer
            self._timer = QTimer(self)
            self._timer.timeout.connect(self._tick)
            self._timer.start(120)

    def stop(self):
        if self._timer:
            self._timer.stop()
            self._timer = None
        self.hide()

    def _tick(self):
        self._idx = (self._idx + 1) % len(self._frames)
        self._spinner.setText(self._frames[self._idx])

    def set_text(self, text: str):
        self._label.setText(text)


class IconButton(QPushButton):
    def __init__(self, icon_path: str, tooltip: str, parent=None):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setFixedSize(60, 60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {SIDEBAR};
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 28px;
            }}
            QPushButton:hover {{ background-color: {SIDEBAR_H}; }}
            QPushButton:pressed {{ background-color: {ACCENT}; }}
        """)
        if icon_path and os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(36, 36))


class EmojiButton(QPushButton):
    def __init__(self, emoji: str, tooltip: str, parent=None):
        super().__init__(parent)
        self.setToolTip(tooltip)
        self.setFixedSize(52, 52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(emoji)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 8px;
                padding: 8px;
                font-size: 22px;
            }}
            QPushButton:hover {{ background-color: {SIDEBAR_H}; }}
            QPushButton:pressed {{ background-color: {ACCENT}; }}
        """)


class IconBar(QFrame):
    icon_clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(64)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {SIDEBAR};
                border-right: none;
            }}
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 20, 6, 20)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.browser_btn = EmojiButton("🌐", "Browser", self)
        self.browser_btn.clicked.connect(lambda: self.icon_clicked.emit("browser"))
        layout.addWidget(self.browser_btn)

        self.ads_btn = EmojiButton("📢", "Ads", self)
        self.ads_btn.clicked.connect(lambda: self.icon_clicked.emit("ads"))
        layout.addWidget(self.ads_btn)

        self.spy_btn = EmojiButton("🕵️", "Spy Agent", self)
        self.spy_btn.clicked.connect(lambda: self.icon_clicked.emit("spy"))
        layout.addWidget(self.spy_btn)

        self.crew_btn = EmojiButton("⚙️", "Crews", self)
        self.crew_btn.clicked.connect(lambda: self.icon_clicked.emit("crew"))
        layout.addWidget(self.crew_btn)

        self.analytics_btn = EmojiButton("📊", "Analytics", self)
        self.analytics_btn.clicked.connect(lambda: self.icon_clicked.emit("analytics"))
        layout.addWidget(self.analytics_btn)

        self.settings_btn = EmojiButton("🔧", "Settings", self)
        self.settings_btn.clicked.connect(lambda: self.icon_clicked.emit("settings"))
        layout.addWidget(self.settings_btn)

        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


class StatusPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(220)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {PAGE_BG};
                border-left: 1px solid {BORDER};
            }}
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 14, 12, 14)

        title = QLabel("STATUS")
        title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT_MUTED}; letter-spacing: 1px;")
        layout.addWidget(title)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 6px;
                color: {TEXT};
                font-family: 'Consolas', monospace;
                font-size: 10px;
                padding: 8px;
            }}
        """)
        layout.addWidget(self.status_text)

        self.log_browser_event("ShopeeAgent started")

    def log_browser_event(self, message: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_text.append(f"<span style='color:{ACCENT}'>[{timestamp}]</span> {message}")

    def update_status(self, agent: str, status: str):
        color = SUCCESS if status == "ready" else WARNING if status == "working" else ERROR
        self.log_browser_event(f"<span style='color:{color}'>[{agent}]</span> {status}")


class MainWindow(QFrame):
    def __init__(self, browser_manager, crew_executor):
        super().__init__()
        self.browser_manager = browser_manager
        self.crew_executor = crew_executor

        self._spy_session_active = False
        self._spy_browser_open = False
        self._ads_session_active = False
        self._spy_category = None   # selected Shopee product category
        self._loading = False       # whether agent is currently executing

        self.setWindowTitle("ShopeeAgent v1.3.1")
        self.setFixedSize(900, 650)
        self.setStyleSheet(f"background-color: {PAGE_BG};")

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
        self.crew_executor.status_update.connect(self._on_crew_status)
        self.crew_executor.message_ready.connect(self._on_agent_message)
        
        self.chat_widget.category_selected.connect(self._on_category_selected)
        
        self.browser_manager.browser_ready.connect(lambda: self._on_browser_connected())
        self.browser_manager.error_occurred.connect(lambda e: self._on_browser_error(e))
        self.browser_manager.browser_closed.connect(lambda: self._on_browser_disconnected())

    def _on_browser_connected(self):
        self.status_panel.log_browser_event("Shopee Browser ready!")
        self.crew_panel.update_fox_status(True, self.browser_manager.get_session_path())

    def _on_browser_error(self, error: str):
        self.status_panel.log_browser_event(f"Browser Error: {error}")
        self.crew_panel.update_fox_status(False)

    def _on_browser_disconnected(self):
        self.status_panel.log_browser_event("Browser closed")
        self.crew_panel.update_fox_status(False)

    def _on_crew_status(self, agent: str, status: str):
        """Central handler for crew status updates — updates panels + loading UI."""
        self.status_panel.update_status(agent, status)
        self.crew_panel.update_status(agent, status)

        if status == "working":
            self._loading = True
            self.chat_widget.show_loading(f"{agent} is working...")
        elif status in ("ready", "error"):
            self._loading = False
            self.chat_widget.hide_loading()

    def _on_agent_message(self, message: str):
        """Intercept agent message to hide loading first, then show result."""
        if self._loading:
            self._loading = False
            self.chat_widget.hide_loading()
        self.chat_widget.add_agent_message(message)

    def _on_category_selected(self, category: str):
        """User selected a Shopee category — record it, hide picker."""
        self._spy_category = category
        self.chat_widget.hide_category_picker()
        self.chat_widget.add_user_message(
            f"🎯 **Category:** {category}\n\n"
            "Use the action buttons above to start analysis."
        )
        self.status_panel.log_browser_event(f"🕵️ Category: {category}")

    def on_icon_clicked(self, icon_name: str):
        if icon_name == "settings":
            self._open_settings_dialog()
            return

        # Session guard: during spy/ads session, stay on chat unless user clicks spy/ads/browser
        if self._spy_session_active and icon_name != "spy":
            self.stacked_widget.setCurrentWidget(self.chat_widget)
            self.status_panel.log_browser_event(f"🕵️ Spy session active — '{icon_name}' panel not available. Click 🕵️ to return.")
            return

        if self._ads_session_active and icon_name not in ("ads", "browser", "spy"):
            self.stacked_widget.setCurrentWidget(self.chat_widget)
            self.status_panel.log_browser_event(f"📢 Ads session active — '{icon_name}' panel not available.")
            return

        if icon_name == "crew" or icon_name == "analytics":
            self.status_panel.log_browser_event("Panel opened — chat session preserved")
            if icon_name == "crew":
                self.stacked_widget.setCurrentWidget(self.crew_panel)
            else:
                self.stacked_widget.setCurrentWidget(self.analytics_panel)
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
                self.status_panel.log_browser_event("⚠️ Please open the browser first by clicking 🌐 icon")
                self.chat_widget.add_user_message("⚠️ Please open the browser first by clicking the 🌐 icon, then navigate to Shopee Ads dashboard manually.")
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
        if hasattr(self, '_settings_dialog') and self._settings_dialog is not None:
            self._settings_dialog.raise_()
            self._settings_dialog.activateWindow()
            return

        dialog = SettingsPanel(None)  # parent=None → top-level window
        dialog.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowTitleHint
        )
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.finished.connect(lambda: setattr(self, '_settings_dialog', None))
        self._settings_dialog = dialog

        # Center dialog relatif terhadap main window
        main_geo = self.geometry()
        dw, dh = dialog.width(), dialog.height()
        x = main_geo.x() + (main_geo.width() - dw) // 2
        y = main_geo.y() + (main_geo.height() - dh) // 2
        dialog.move(max(0, x), max(0, y))
        dialog.show()

    def _handle_spy_agent_click(self):
        if self.browser_manager.is_ready():
            self.status_panel.log_browser_event("Closing existing browser for Spy Agent...")
            self.browser_manager.close()

        self._spy_session_active = True
        self.status_panel.log_browser_event("🕵️ Launching Spy Agent - Shopee Marketplace...")
        self.stacked_widget.setCurrentWidget(self.chat_widget)

        self.chat_widget.clear_chat()
        self.chat_widget.set_context_header("Spy Agent - Market Research")

        # Launch browser immediately to shopee.co.id
        self.browser_manager.launch_browser(target_url="https://shopee.co.id")
        self.chat_widget.set_spy_mode(True)

        # Show category picker for context (browser already running behind it)
        self.chat_widget.add_user_message(
            "🕵️ **Spy Agent - Market Research**\n\n"
            "Browser sudah terbuka ke shopee.co.id.\n\n"
            "Pilih kategori produk yang ingin di-scan dan dianalisa,\n"
            "lalu gunakan tombol aksi di atas untuk mulai analisis."
        )
        self.chat_widget.show_category_picker()

    def _on_spy_action(self, action: str):
        cat = self._spy_category or ""
        cat_ctx = f"\n\nPRODUCT CATEGORY: {cat}. Focus exclusively on products in the '{cat}' category." if cat else ""

        if action == "scan_market":
            self.status_panel.log_browser_event("🕵️ Starting Market Scan...")
            self.chat_widget.add_user_message(f"📡 **Scanning Shopee Marketplace — {cat}**\n\nExtracting all products with structured DOM extraction...")
            self.crew_executor.execute_spy_task(
                task_description=f"Use scan_shopee_market to extract ALL product data from the current search results. Use extract_structured=True for accurate JSON data.{cat_ctx}",
                page=self.browser_manager.get_page()
            )
        elif action == "review_mine":
            self.status_panel.log_browser_event("🕵️ Starting Review Mining...")
            self.chat_widget.add_user_message(f"💬 **Mining Customer Reviews — {cat}**\n\nExtracting pain points & strengths from reviews...\n\nNavigate to a product page first, then click the button.")
            self.crew_executor.execute_spy_task(
                task_description=f"Navigate to a top-selling product page, click the Reviews tab, then use mine_product_reviews to extract customer sentiment. Identify pain points (1-2 stars) and strengths (4-5 stars).{cat_ctx}",
                page=self.browser_manager.get_page()
            )
        elif action == "store_profile":
            self.status_panel.log_browser_event("🕵️ Starting Store Profiling...")
            self.chat_widget.add_user_message(f"🏪 **Analyzing Competitor Store — {cat}**\n\nExtracting store metrics, rating, followers, badges...\n\nNavigate to a store page first, then click the button.")
            self.crew_executor.execute_spy_task(
                task_description=f"Use profile_shopee_store on the current store page. Extract name, rating, followers, product count, badges, and official status. Then use scan_shopee_market to scan the store's products.{cat_ctx}",
                page=self.browser_manager.get_page()
            )
        elif action == "full_report":
            self.status_panel.log_browser_event("🕵️ Starting Full Market Intelligence...")
            self.chat_widget.add_user_message(f"🎯 **Full Market Intelligence Report — {cat}**\n\nRunning complete analysis pipeline:\n1. 📡 Market Scan\n2. 📊 Competitor Analysis\n3. 📈 Trend Detection\n4. 💬 Review Mining\n5. 🎯 Strategy Synthesis\n\nThis may take 5-8 minutes...")
            self.crew_executor.execute_spy_task(
                task_description=f"Run COMPLETE market intelligence for the '{cat}' category: 1) scan_shopee_market for ALL products, 2) analyze_market_gaps for opportunities, 3) Navigate to top 3 competitor product pages and mine_product_reviews, 4) Generate comprehensive strategy report with Executive Summary, Competitor Landscape, Gap Opportunities, Customer Pain Points, Keyword Recommendations, Pricing Strategy, and Risk Assessment.{cat_ctx}",
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


class SelfSizingTextEdit(QTextEdit):
    """QTextEdit that auto-sizes its height to show all content without scrollbars.

    Uses document layout geometry so the QScrollArea parent allocates the full
    content height.  Reports a minimum width derived from the text-width basin
    so the bubble never collapses narrower than the wrapping column.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text_width = 410
        self._margin = 28  # CSS padding + border overhead
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.document().contentsChanged.connect(self._on_content)

    def set_text_width(self, width: int):
        self._text_width = width

    def _on_content(self):
        self.updateGeometry()

    def sizeHint(self) -> QSize:
        doc = self.document()
        doc.setTextWidth(self._text_width)
        # idealWidth can be small for short text → clamp to text_width basin
        width = max(self._text_width + 20, int(doc.idealWidth()) + 10)
        height = int(doc.size().height()) + self._margin
        return QSize(width, height)

    def minimumSizeHint(self) -> QSize:
        return QSize(200, 36)


class ChatWidget(QFrame):
    send_message = pyqtSignal(str)
    message_ready = pyqtSignal(str)
    category_selected = pyqtSignal(str)  # emitted when user picks a Shopee category

    def __init__(self, parent=None):
        super().__init__(parent)
        self._spy_mode = False
        self._spy_start_btn = None
        self._chat_header_label = None
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border-radius: 8px;
            }}
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QLabel("ShopeeAgent")
        header.setStyleSheet(f"""
            QLabel {{
                background-color: {SIDEBAR};
                color: white;
                padding: 14px 16px;
                font-size: 14px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        header.setFixedHeight(46)
        layout.addWidget(header)

        self._chat_header_label = QLabel("")
        self._chat_header_label.setStyleSheet(f"""
            QLabel {{
                background-color: {ACCENT};
                color: white;
                padding: 5px 16px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        self._chat_header_label.setFixedHeight(0)
        self._chat_header_label.hide()
        layout.addWidget(self._chat_header_label)

        # SpyAgent Action Bar
        self._spy_action_bar = QWidget()
        self._spy_action_bar.setStyleSheet(f"background-color: #EEF4FB; border-bottom: 1px solid {BORDER};")
        spy_action_layout = QHBoxLayout(self._spy_action_bar)
        spy_action_layout.setContentsMargins(8, 6, 8, 6)
        spy_action_layout.setSpacing(6)

        actions = [
            ("Scan", "scan_market", "Extract product data from current search"),
            ("Reviews", "review_mine", "Mine customer reviews for insights"),
            ("Store", "store_profile", "Profile competitor store"),
            ("Full Report", "full_report", "Complete market intelligence report"),
        ]

        for label, action_id, tooltip in actions:
            btn = QPushButton(f" {label} ")
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ACCENT};
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 5px 12px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: {ACCENT_H}; }}
            """)
            btn.clicked.connect(lambda checked, a=action_id: self.send_message.emit(f"__SPY_ACTION__:{a}"))
            spy_action_layout.addWidget(btn)

        spy_action_layout.addStretch()
        self._spy_action_bar.hide()
        layout.addWidget(self._spy_action_bar)

        # ── loading indicator (pinned ABOVE scroll area, always visible) ──
        self._loading = LoadingWidget()
        self._loading.hide()
        layout.addWidget(self._loading)

        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {PAGE_BG};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {PAGE_BG};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {BORDER};
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {TEXT_SUB};
            }}
        """)
        # ── chat scroll content ─────────────────────────────────
        self.chat_content = QWidget()
        self.chat_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setContentsMargins(8, 8, 8, 8)
        self.chat_layout.setSpacing(4)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # category picker (shown during spy setup) — inside scroll so it can be long
        self._category_picker = self._build_category_picker()
        self._category_picker.hide()
        self.chat_layout.addWidget(self._category_picker)

        self.chat_area.setWidget(self.chat_content)
        layout.addWidget(self.chat_area, stretch=1)

        input_layout = QHBoxLayout()
        self._input_layout = input_layout  # stored for spy_start_btn insertion
        input_layout.setContentsMargins(12, 10, 12, 12)
        input_layout.setSpacing(8)

        from PyQt6.QtWidgets import QLineEdit
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a command...")
        self.message_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {PAGE_BG};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 10px 16px;
                color: {TEXT};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border: 1px solid {ACCENT};
            }}
        """)
        self.message_input.returnPressed.connect(self.on_send_clicked)
        input_layout.addWidget(self.message_input)

        send_btn = QPushButton("Send")
        send_btn.setFixedSize(70, 38)
        send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        send_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {ACCENT_H}; }}
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
        # Container with stretch → pushes bubble to the right
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(24, 4, 8, 4)
        container_layout.addStretch()

        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        bubble.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        bubble.setMaximumWidth(420)
        bubble.setMinimumWidth(60)
        bubble.setStyleSheet(f"""
            QLabel {{
                color: white;
                background-color: {ACCENT};
                padding: 10px 14px;
                border-radius: 14px;
                border-bottom-right-radius: 4px;
                font-size: 12px;
            }}
        """)
        container_layout.addWidget(bubble)
        self.chat_layout.addWidget(container)

    def add_agent_message(self, message: str):
        html_content = markdown.markdown(
            f"{message}",
            extensions=['tables', 'fenced_code', 'nl2br']
        )

        styled_html = f"""
        <html><head><style>
        body {{
            color: {TEXT}; background-color: {PAGE_BG};
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px; line-height: 1.5;
            padding: 14px; margin: 0;
        }}
        h1, h2, h3 {{ color: {TEXT}; margin: 10px 0 6px 0; font-size: 15px; }}
        p {{ margin: 6px 0; }}
        strong {{ color: {TEXT}; }}
        code {{
            background-color: {CARD_BG}; padding: 2px 6px; border-radius: 4px;
            font-family: 'Consolas', monospace; font-size: 12px;
            color: {ACCENT}; border: 1px solid {BORDER};
        }}
        pre {{
            background-color: {CARD_BG}; padding: 10px; border-radius: 6px;
            border: 1px solid {BORDER}; overflow-x: auto; margin: 8px 0;
        }}
        pre code {{ background-color: transparent; border: none; padding: 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
        th, td {{ border: 1px solid {BORDER}; padding: 6px 10px; text-align: left; font-size: 12px; }}
        th {{ background-color: {SIDEBAR}; color: white; }}
        tr:nth-child(even) {{ background-color: {PAGE_BG}; }}
        a {{ color: {ACCENT}; text-decoration: none; }}
        ul, ol {{ margin: 6px 0; padding-left: 22px; }}
        li {{ margin: 2px 0; }}
        blockquote {{ border-left: 3px solid {ACCENT}; margin: 8px 0; padding: 6px 14px; background: {CARD_BG}; color: {TEXT_MUTED}; }}
        </style></head>
        <body>{html_content}</body></html>
        """

        # Container with stretch → pushes bubble to the left
        container = QWidget()
        clayout = QHBoxLayout(container)
        clayout.setContentsMargins(8, 4, 16, 4)

        msg_widget = SelfSizingTextEdit()
        msg_widget.setReadOnly(True)
        msg_widget.setHtml(styled_html)
        msg_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msg_widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msg_widget.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        msg_widget.set_text_width(410)
        msg_widget.setMaximumWidth(480)

        msg_widget.setStyleSheet(f"""
            QTextEdit {{
                background-color: {PAGE_BG};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)

        clayout.addWidget(msg_widget)
        clayout.addStretch()  # keeps bubble left-aligned
        self.chat_layout.addWidget(container)
        # auto-scroll to latest message
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )

    def set_spy_mode(self, active: bool):
        if active:
            self._spy_mode = True
            self._spy_action_bar.show()
            self.message_input.setPlaceholderText("Type command or use action buttons above...")
            if hasattr(self, '_spy_start_btn') and self._spy_start_btn:
                pass
            else:
                self._spy_start_btn = QPushButton("Start Analysis")
                self._spy_start_btn.setFixedSize(130, 38)
                self._spy_start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                self._spy_start_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {SUCCESS}; color: white;
                        border: none; border-radius: 8px;
                        font-weight: bold; font-size: 12px;
                    }}
                    QPushButton:hover {{ background-color: #43A047; }}
                """)
                self._spy_start_btn.clicked.connect(self._on_spy_start)
            if hasattr(self, '_input_layout') and self._input_layout:
                input_layout = self._input_layout
                if self._spy_start_btn not in [input_layout.itemAt(i).widget() for i in range(input_layout.count())]:
                    insert_idx = input_layout.count() - 1
                    input_layout.insertWidget(insert_idx, self._spy_start_btn)
        else:
            self._spy_mode = False
            self._spy_action_bar.hide()
            self.message_input.setPlaceholderText("Type a command...")
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
            w = item.widget()
            if w:
                w.hide()
                w.deleteLater()
        # re-insert category widget
        self._category_picker.hide()
        self.chat_layout.insertWidget(0, self._category_picker)

    def set_context_header(self, text: str):
        if hasattr(self, '_chat_header_label') and self._chat_header_label:
            self._chat_header_label.setText(f"  {text}")
            self._chat_header_label.setFixedHeight(26)
            self._chat_header_label.show()

    # ── category picker ─────────────────────────────────────────
    def _build_category_picker(self) -> QWidget:
        """Build the category selection panel shown during spy agent setup."""
        panel = QWidget()
        panel.setStyleSheet(f"""
            QWidget {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(8)

        title_lbl = QLabel("Select Product Category")
        title_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT}; border: none;")
        layout.addWidget(title_lbl)

        desc = QLabel("Choose the Shopee category you want to analyze. The spy agent will scrape and analyze products in this category.")
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; border: none;")
        layout.addWidget(desc)

        # category buttons in a flow layout (using QGridLayout)
        grid = QGridLayout()
        grid.setSpacing(6)
        cols = 3
        for i, (emoji_label, cat_name) in enumerate(SHOPEE_CATEGORIES):
            btn = QPushButton(emoji_label)
            btn.setToolTip(f"Analyze {cat_name}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {PAGE_BG};
                    color: {TEXT};
                    border: 1px solid {BORDER};
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{ background-color: #EEF4FB; border-color: {ACCENT}; }}
            """)
            btn.clicked.connect(lambda checked, c=cat_name: self.category_selected.emit(c))
            grid.addWidget(btn, i // cols, i % cols)
        layout.addLayout(grid)

        # custom input row
        custom_row = QHBoxLayout()
        custom_row.setSpacing(6)
        self._custom_cat_input = QLineEdit()
        self._custom_cat_input.setPlaceholderText("Or type a custom category...")
        self._custom_cat_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {PAGE_BG};
                border: 1px solid {BORDER};
                border-radius: 6px;
                padding: 6px 10px;
                color: {TEXT};
                font-size: 11px;
            }}
            QLineEdit:focus {{ border-color: {ACCENT}; }}
        """)
        self._custom_cat_input.returnPressed.connect(self._on_custom_category)
        custom_row.addWidget(self._custom_cat_input)

        custom_btn = QPushButton("Go")
        custom_btn.setFixedSize(44, 30)
        custom_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        custom_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT}; color: white;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {ACCENT_H}; }}
        """)
        custom_btn.clicked.connect(self._on_custom_category)
        custom_row.addWidget(custom_btn)
        layout.addLayout(custom_row)

        return panel

    def _on_custom_category(self):
        text = self._custom_cat_input.text().strip()
        if text:
            self.category_selected.emit(text)
            self._custom_cat_input.clear()

    def show_category_picker(self):
        self._category_picker.show()

    def hide_category_picker(self):
        self._category_picker.hide()

    # ── loading indicator helpers ────────────────────────────────
    def show_loading(self, text: str = "AI agent is working..."):
        self._loading.start(text)

    def hide_loading(self):
        self._loading.stop()
