from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea,
    QFrame, QListWidget, QListWidgetItem,
    QTextEdit, QGroupBox, QFormLayout,
    QComboBox, QLineEdit, QSpinBox,
    QCheckBox, QProgressBar, QTableWidget,
    QTableWidgetItem, QTabWidget, QWidget, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor
import os
from dotenv import load_dotenv


SUMOPOD_MODELS = [
    "deepseek-v4-pro",
    "MiniMax-M2.7-highspeed",
    "MiniMax-Text-01",
    "abab6.5s-chat",
    "abab6.5g-chat",
    "abab5.5g-chat",
]

OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

ALL_MODELS = SUMOPOD_MODELS + OPENAI_MODELS


class CrewPanel(QFrame):
    """Crew management: shows all 3 crews (Browser, Ads, Spy) and Camoufox status."""

    crew_status_update = pyqtSignal(str, str)

    # ── palette ─────────────────────────────────────────────────
    ACCENT   = "#4A90D9"
    SUCCESS  = "#4CAF50"
    TEXT     = "#1A1A1A"
    TEXT_MUTED="#666666"
    TEXT_SUB  ="#999999"
    BORDER   = "#E0E0E0"
    PAGE_BG  = "#F5F5F5"
    CARD_BG  = "#FFFFFF"

    CREW_CARD_STYLE = f"""
        QFrame#crewCard {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 0px;
        }}
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QFrame#crewPanel { background-color: #F5F5F5; border-radius: 8px; }")
        self.setObjectName("crewPanel")
        self._crew_status_data = {}
        self.setup_ui()

    # ── crew definitions ───────────────────────────────────────
    @staticmethod
    def _crew_defs():
        return [
            {
                "id": "browser",
                "name": "BrowserCrew",
                "icon": "🌐",
                "desc": "Otomasi browser & ekstraksi data halaman",
                "process": "Hierarchical",
                "memory": False,
                "planning": False,
                "agents": [
                    ("Navigator", "Navigasi & interaksi halaman Shopee", "11 browser tools"),
                    ("Scraper",   "Ekstraksi konten & data dari DOM",    "11 browser tools"),
                    ("Analyst",   "Analisis data & sintesis laporan",    "—"),
                ],
            },
            {
                "id": "ads",
                "name": "ShopeeCrew",
                "icon": "📢",
                "desc": "Analisis & optimasi iklan Shopee Seller Center",
                "process": "Sequential",
                "memory": False,
                "planning": False,
                "agents": [
                    ("ShopeeNavigator", "Ekstrak metrik iklan dari Seller Center", "3 ads tools + 11 browser"),
                    ("FinancialAnalyst", "Hitung ROAS, Break-Even, Net Profit",     "3 ads tools"),
                    ("AdsOptimizer",     "Rekomendasi bid & optimasi iklan",         "3 ads tools"),
                ],
            },
            {
                "id": "spy",
                "name": "SpyCrew",
                "icon": "🕵️",
                "desc": "Market intelligence & analisis kompetitor Shopee marketplace",
                "process": "Sequential",
                "memory": True,
                "planning": True,
                "agents": [
                    ("MarketScanner",       "DOM extraction 16-field structured JSON",  "5 spy + 11 browser"),
                    ("CompetitorProfiler",   "Analisis toko, harga, gap opportunities", "5 spy tools"),
                    ("TrendDetector",        "Best-seller, review mining, tren pasar",  "5 spy + 11 browser"),
                    ("StrategySynthesizer",  "Laporan market intelligence 7 section",   "—"),
                ],
            },
        ]

    # ── ui ──────────────────────────────────────────────────────
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("Crew Management")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1A1A1A; padding-bottom: 2px;")
        layout.addWidget(title)

        subtitle = QLabel("CrewAI multi-agent orchestration — 3 crews, 10 agents, 19 tools")
        subtitle.setStyleSheet("color: #555555; font-size: 12px; padding-bottom: 4px;")
        layout.addWidget(subtitle)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # ── Camoufox status card ────────────────────────────────
        content_layout.addWidget(self._build_camoufox_card())

        # ── crew cards ──────────────────────────────────────────
        for crew_def in self._crew_defs():
            content_layout.addWidget(self._build_crew_card(crew_def))

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    # ── Camoufox card ───────────────────────────────────────────
    def _build_camoufox_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("crewCard")
        card.setStyleSheet(self.CREW_CARD_STYLE)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(14, 10, 14, 10)
        cl.setSpacing(8)

        header = QHBoxLayout()
        hdr = QLabel("  Camoufox Browser")
        hdr.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        hdr.setStyleSheet(f"color: {self.TEXT}; border: none;")
        header.addWidget(hdr)
        header.addStretch()

        self._fox_status = QLabel("Disconnected")
        self._fox_status.setStyleSheet(
            f"color: {self.TEXT_SUB}; font-size: 11px; font-weight: bold; padding: 2px 8px; "
            f"background: {self.PAGE_BG}; border-radius: 10px; border: none;")
        header.addWidget(self._fox_status)
        cl.addLayout(header)

        info = QHBoxLayout()
        info.setSpacing(16)
        for label, value in [
            ("Engine", "Firefox (Gecko)"),
            ("Stealth", "BrowserForge + anti-detect"),
            ("Proxy", "None (direct)"),
            ("Locale", "id-ID (Indonesia)"),
        ]:
            box = QVBoxLayout()
            box.setSpacing(2)
            l = QLabel(label)
            l.setStyleSheet(f"color: {self.TEXT_SUB}; font-size: 10px; border: none;")
            v = QLabel(value)
            v.setStyleSheet(f"color: {self.TEXT}; font-size: 11px; font-weight: bold; border: none;")
            box.addWidget(l)
            box.addWidget(v)
            info.addLayout(box)
        info.addStretch()
        cl.addLayout(info)

        self._session_label = QLabel("Session: —")
        self._session_label.setStyleSheet(f"color: {self.TEXT_SUB}; font-size: 11px; border: none;")
        cl.addWidget(self._session_label)

        return card

    # ── single crew card ────────────────────────────────────────
    def _build_crew_card(self, crew_def: dict) -> QFrame:
        card = QFrame()
        card.setObjectName("crewCard")
        card.setStyleSheet(self.CREW_CARD_STYLE)

        cl = QVBoxLayout(card)
        cl.setContentsMargins(14, 10, 14, 10)
        cl.setSpacing(6)

        header = QHBoxLayout()
        hdr = QLabel(f"{crew_def['icon']}  {crew_def['name']}")
        hdr.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        hdr.setStyleSheet(f"color: {self.TEXT}; border: none;")
        header.addWidget(hdr)
        header.addStretch()

        # badges — semua pakai warna biru aksen
        badges = [crew_def['process']]
        if crew_def['memory']:
            badges.append("Memory")
        if crew_def['planning']:
            badges.append("Planning")
        for badge in badges:
            b = QLabel(badge)
            b.setStyleSheet(
                f"color: {self.ACCENT}; font-size: 10px; font-weight: bold; padding: 2px 7px; "
                f"background: {self.PAGE_BG}; border: 1px solid {self.BORDER}; border-radius: 8px;")
            header.addWidget(b)
        cl.addLayout(header)

        desc = QLabel(crew_def['desc'])
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {self.TEXT_MUTED}; font-size: 11px; border: none; margin-bottom: 2px;")
        cl.addWidget(desc)

        for agent_name, agent_desc, agent_tools in crew_def['agents']:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)

            name_lbl = QLabel(agent_name)
            name_lbl.setStyleSheet(f"color: {self.TEXT}; font-size: 12px; font-weight: bold; border: none;")
            name_lbl.setFixedWidth(140)
            row.addWidget(name_lbl)

            desc_lbl = QLabel(agent_desc)
            desc_lbl.setStyleSheet(f"color: {self.TEXT_MUTED}; font-size: 11px; border: none;")
            row.addWidget(desc_lbl, stretch=1)

            tools_lbl = QLabel(agent_tools)
            tools_lbl.setStyleSheet(f"color: {self.TEXT_SUB}; font-size: 10px; border: none;")
            tools_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            row.addWidget(tools_lbl)

            cl.addLayout(row)

        return card

    # ── public api ──────────────────────────────────────────────
    def update_fox_status(self, connected: bool, session: str = ""):
        if connected:
            self._fox_status.setText("Connected")
            self._fox_status.setStyleSheet(
                f"color: {self.SUCCESS}; font-size: 11px; font-weight: bold; padding: 2px 8px; "
                f"background: #E8F5E9; border-radius: 10px; border: none;")
            self._session_label.setText(f"Session: {session}" if session else "Session: active")
        else:
            self._fox_status.setText("Disconnected")
            self._fox_status.setStyleSheet(
                f"color: {self.TEXT_SUB}; font-size: 11px; font-weight: bold; padding: 2px 8px; "
                f"background: {self.PAGE_BG}; border-radius: 10px; border: none;")
            self._session_label.setText("Session: —")

    def update_status(self, status: str, task: str = ""):
        pass


class AnalyticsPanel(QFrame):
    """Analytics dashboard with card-style metrics."""

    LABEL    = "#1A1A1A"
    MUTED    = "#666666"
    ACCENT   = "#4A90D9"
    SUCCESS  = "#4CAF50"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame#analyticsPanel { background-color: #F5F5F5; border-radius: 8px; }
        """)
        self.setObjectName("analyticsPanel")
        self.task_history = []
        self.setup_ui()

    # ── ui ──────────────────────────────────────────────────────
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # title
        title = QLabel("Analytics Dashboard")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.LABEL}; padding-bottom: 4px;")
        layout.addWidget(title)

        # ── metric cards row ────────────────────────────────────
        cards = QHBoxLayout()
        cards.setSpacing(12)

        self.tasks_card  = self._make_metric_card("Tasks", "0", self.ACCENT)
        self.errors_card = self._make_metric_card("Errors", "0", "#C62828")
        self.tokens_card = self._make_metric_card("Est. Tokens", "~0", self.MUTED)

        cards.addWidget(self.tasks_card)
        cards.addWidget(self.errors_card)
        cards.addWidget(self.tokens_card)
        layout.addLayout(cards)

        # ── task history list ───────────────────────────────────
        history_header = QLabel("Task History")
        history_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        history_header.setStyleSheet(f"color: {self.LABEL}; padding-top: 6px;")
        layout.addWidget(history_header)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #FFFFFF;
                border: 1px solid #D0D0D0;
                border-radius: 6px;
                color: #1A1A1A;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-bottom: 1px solid #EEEEEE;
            }
            QListWidget::item:last { border-bottom: none; }
            QListWidget::item:selected {
                background-color: #4A90D9;
                color: white;
            }
        """)
        layout.addWidget(self.history_list, stretch=1)

    # ── metric card factory ─────────────────────────────────────
    def _make_metric_card(self, label: str, initial: str, accent: str) -> QFrame:
        card = QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
            }}
        """)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(14, 10, 14, 10)
        cl.setSpacing(4)

        lbl = QLabel(label)
        lbl.setFont(QFont("Segoe UI", 10))
        lbl.setStyleSheet(f"color: {self.MUTED}; border: none;")

        val = QLabel(initial)
        val.setObjectName(f"_metric_val_{label.replace(' ', '_')}")
        val.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        val.setStyleSheet(f"color: {accent}; border: none;")

        cl.addWidget(lbl)
        cl.addWidget(val)
        cl.addStretch()
        return card

    def _get_card_value_label(self, card: QFrame) -> QLabel:
        """Return the value QLabel inside a metric card."""
        for ch in card.findChildren(QLabel):
            if ch.objectName().startswith("_metric_val_"):
                return ch
        return QLabel("?")

    # ── public api ──────────────────────────────────────────────
    def add_task(self, task: str, status: str = "success"):
        self.task_history.append({"task": task, "status": status})
        n = len(self.task_history)

        self._get_card_value_label(self.tasks_card).setText(str(n))

        error_count = sum(1 for t in self.task_history if t["status"] == "error")
        self._get_card_value_label(self.errors_card).setText(str(error_count))

        est = n * 1500
        self._get_card_value_label(self.tokens_card).setText(f"~{est:,}")

        icon = "✓" if status == "success" else "✗"
        item = QListWidgetItem(f"  {icon}  {task[:70]}")
        if status == "error":
            item.setForeground(QColor("#C62828"))
        self.history_list.insertItem(0, item)


class SettingsPanel(QDialog):
    """Settings dialog with consistent dark labels and proper form spacing."""

    settings_changed = pyqtSignal(dict)

    # ── constants ──────────────────────────────────────────────
    LABEL_COLOR = "#1A1A1A"
    ACCENT      = "#4A90D9"
    GROUP_STYLE = """
        QGroupBox {
            color: #1A1A1A;
            border: 1px solid #D0D0D0;
            border-radius: 6px;
            margin-top: 14px;
            padding: 18px 12px 12px 12px;
            font-weight: bold;
            background-color: #FAFAFA;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 6px;
            background-color: #FAFAFA;
        }
    """

    # ── widget style helpers ────────────────────────────────────
    @staticmethod
    def _combobox_style() -> str:
        return """
            QComboBox {
                background-color: #FFFFFF;
                color: #1A1A1A;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 10px;
                min-width: 180px;
                font-size: 13px;
            }
            QComboBox:hover { border-color: #4A90D9; }
            QComboBox:focus { border-color: #4A90D9; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #1A1A1A;
                border: 1px solid #CCCCCC;
                selection-background-color: #4A90D9;
            }
        """

    @staticmethod
    def _spinbox_style() -> str:
        return """
            QSpinBox {
                background-color: #FFFFFF;
                color: #1A1A1A;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 10px;
                min-width: 80px;
                font-size: 13px;
            }
            QSpinBox:hover { border-color: #4A90D9; }
            QSpinBox:focus { border-color: #4A90D9; }
        """

    @staticmethod
    def _lineedit_style() -> str:
        return """
            QLineEdit {
                background-color: #FFFFFF;
                color: #1A1A1A;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 7px 10px;
                font-size: 13px;
            }
            QLineEdit:hover { border-color: #4A90D9; }
            QLineEdit:focus { border-color: #4A90D9; }
        """

    @staticmethod
    def _label_style() -> str:
        return f"color: {SettingsPanel.LABEL_COLOR}; font-size: 13px; padding-right: 8px;"

    # ── init ────────────────────────────────────────────────────
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ShopeeAgent Settings")
        self.resize(480, 620)
        self.setMinimumWidth(440)
        self.setup_ui()

    # ── ui ──────────────────────────────────────────────────────
    def setup_ui(self):
        self.setStyleSheet(f"QDialog {{ background-color: #F5F5F5; color: {self.LABEL_COLOR}; }}")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        # ── title ───────────────────────────────────────────────
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.LABEL_COLOR}; padding-bottom: 4px;")
        content_layout.addWidget(title)

        # ── LLM ─────────────────────────────────────────────────
        content_layout.addWidget(self._build_llm_group())

        # ── Browser ─────────────────────────────────────────────
        content_layout.addWidget(self._build_browser_group())

        # ── CrewAI Advanced ─────────────────────────────────────
        content_layout.addWidget(self._build_crew_group())

        # ── API Keys ────────────────────────────────────────────
        content_layout.addWidget(self._build_api_group())

        # ── Apply button ────────────────────────────────────────
        save_btn = QPushButton("Apply Settings")
        save_btn.setFixedHeight(40)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.ACCENT}; color: white; border: none;
                border-radius: 6px; font-weight: bold; font-size: 14px;
            }}
            QPushButton:hover {{ background-color: #357ABD; }}
            QPushButton:pressed {{ background-color: #2A6AA0; }}
        """)
        save_btn.clicked.connect(self.on_save)
        content_layout.addWidget(save_btn)

        content_layout.addStretch()
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        self.on_provider_changed("SumoPod AI")

    # ── group builders ──────────────────────────────────────────
    def _make_group(self, title: str) -> QGroupBox:
        gb = QGroupBox(title)
        gb.setStyleSheet(self.GROUP_STYLE)
        ly = QFormLayout()
        ly.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ly.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        ly.setHorizontalSpacing(16)
        ly.setVerticalSpacing(12)
        ly.setContentsMargins(0, 4, 0, 0)
        gb.setLayout(ly)
        return gb

    def _build_llm_group(self) -> QGroupBox:
        gb = self._make_group("LLM Configuration")
        ly = gb.layout()

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["SumoPod AI", "Official OpenAI"])
        self.provider_combo.setCurrentText("SumoPod AI")
        self.provider_combo.setStyleSheet(self._combobox_style())
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        lbl = QLabel("Provider"); lbl.setStyleSheet(self._label_style())
        ly.addRow(lbl, self.provider_combo)

        self.model_combo = QComboBox()
        self._update_model_combo("SumoPod AI")
        self.model_combo.setStyleSheet(self._combobox_style())
        lbl2 = QLabel("Model"); lbl2.setStyleSheet(self._label_style())
        ly.addRow(lbl2, self.model_combo)

        self.max_iter_spin = QSpinBox()
        self.max_iter_spin.setRange(1, 50); self.max_iter_spin.setValue(10)
        self.max_iter_spin.setStyleSheet(self._spinbox_style())
        lbl3 = QLabel("Max Iterations"); lbl3.setStyleSheet(self._label_style())
        ly.addRow(lbl3, self.max_iter_spin)

        self.max_time_spin = QSpinBox()
        self.max_time_spin.setRange(30, 600); self.max_time_spin.setValue(120)
        self.max_time_spin.setStyleSheet(self._spinbox_style())
        lbl4 = QLabel("Max Exec Time (s)"); lbl4.setStyleSheet(self._label_style())
        ly.addRow(lbl4, self.max_time_spin)

        return gb

    def _build_browser_group(self) -> QGroupBox:
        gb = self._make_group("Browser Settings")
        ly = gb.layout()

        self.headless_check = self._create_checkbox("Headless mode (no GUI)")
        self.headless_check.setStyleSheet(self._checkbox_style())
        ly.addRow(self.headless_check)

        self.humanize_check = self._create_checkbox("Humanize mouse movement")
        self.humanize_check.setChecked(True)
        self.humanize_check.setStyleSheet(self._checkbox_style())
        ly.addRow(self.humanize_check)

        return gb

    def _build_crew_group(self) -> QGroupBox:
        gb = self._make_group("CrewAI Advanced")
        ly = gb.layout()

        self.memory_check = self._create_checkbox("Enable Memory (requires OpenAI)")
        self.memory_check.setStyleSheet(self._checkbox_style())
        ly.addRow(self.memory_check)

        self.planning_check = self._create_checkbox("Enable Planning (requires OpenAI)")
        self.planning_check.setStyleSheet(self._checkbox_style())
        ly.addRow(self.planning_check)

        self.openai_warning = QLabel("Memory & Planning only work with Official OpenAI provider.")
        self.openai_warning.setStyleSheet(
            "color: #666666; font-size: 11px; font-style: italic; padding: 2px 0;")
        self.openai_warning.setWordWrap(True)
        ly.addRow(self.openai_warning)

        return gb

    def _build_api_group(self) -> QGroupBox:
        gb = self._make_group("API Keys")
        ly = gb.layout()

        self.sumpod_key_input = QLineEdit()
        self.sumpod_key_input.setPlaceholderText("Enter SumoPod API key…")
        self.sumpod_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.sumpod_key_input.setStyleSheet(self._lineedit_style())
        self._load_api_key("SUMOPOD_API_KEY", self.sumpod_key_input)
        lbl = QLabel("SumoPod Key"); lbl.setStyleSheet(self._label_style())
        ly.addRow(lbl, self.sumpod_key_input)

        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText("Enter OpenAI API key…")
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setStyleSheet(self._lineedit_style())
        self._load_api_key("OPENAI_API_KEY", self.openai_key_input)
        lbl2 = QLabel("OpenAI Key"); lbl2.setStyleSheet(self._label_style())
        ly.addRow(lbl2, self.openai_key_input)

        note = QLabel("Keys are saved to .env and persist across restarts.")
        note.setWordWrap(True)
        note.setStyleSheet("color: #666666; font-size: 11px; margin-top: 4px;")
        ly.addRow(note)

        return gb

    # ── checkbox style ─────────────────────────────────────────
    @staticmethod
    def _checkbox_style() -> str:
        return """
            QCheckBox {
                color: #1A1A1A; spacing: 8px; font-size: 13px;
            }
            QCheckBox::indicator {
                width: 18px; height: 18px;
                border: 1px solid #AAAAAA; border-radius: 3px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #4A90D9; border-color: #357ABD;
            }
            QCheckBox::indicator:hover { border-color: #4A90D9; }
        """

    # ── helpers ─────────────────────────────────────────────────
    def _load_api_key(self, key_name: str, input_field: QLineEdit):
        load_dotenv()
        api_key = os.environ.get(key_name, "")
        if api_key:
            input_field.setText(api_key)
            input_field.setPlaceholderText("Loaded from .env (change to override)")

    def _create_checkbox(self, text: str) -> QCheckBox:
        cb = QCheckBox(text)
        return cb

    def _update_model_combo(self, provider: str):
        self.model_combo.clear()
        if provider == "SumoPod AI":
            self.model_combo.addItems(SUMOPOD_MODELS)
            self.model_combo.setCurrentText("MiniMax-M2.7-highspeed")
        else:
            self.model_combo.addItems(OPENAI_MODELS)
            self.model_combo.setCurrentText("gpt-4o-mini")

    def on_provider_changed(self, provider: str):
        self._update_model_combo(provider)
        is_sumopod = (provider == "SumoPod AI")
        self.memory_check.setChecked(False); self.memory_check.setEnabled(not is_sumopod)
        self.planning_check.setChecked(False); self.planning_check.setEnabled(not is_sumopod)
        self.openai_warning.setVisible(is_sumopod)

    def on_save(self):
        sumpod_key = self.sumpod_key_input.text().strip()
        openai_key = self.openai_key_input.text().strip()
        if sumpod_key: os.environ["SUMOPOD_API_KEY"] = sumpod_key
        if openai_key: os.environ["OPENAI_API_KEY"] = openai_key
        self._save_to_env_file(sumpod_key, openai_key)
        self.settings_changed.emit({
            "provider": self.provider_combo.currentText(),
            "model": self.model_combo.currentText(),
            "max_iter": self.max_iter_spin.value(),
            "max_time": self.max_time_spin.value(),
            "headless": self.headless_check.isChecked(),
            "humanize": self.humanize_check.isChecked(),
            "memory": self.memory_check.isChecked(),
            "planning": self.planning_check.isChecked(),
            "sumpod_api_key": sumpod_key if sumpod_key else os.environ.get("SUMOPOD_API_KEY", ""),
            "openai_api_key": openai_key if openai_key else os.environ.get("OPENAI_API_KEY", ""),
        })
        self.accept()

    def _save_to_env_file(self, sumpod_key: str, openai_key: str):
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
        env_lines = {}
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        env_lines[k.strip()] = v.strip()
        if sumpod_key: env_lines["SUMOPOD_API_KEY"] = sumpod_key
        if openai_key: env_lines["OPENAI_API_KEY"] = openai_key
        env_lines.setdefault("SUMOPOD_BASE_URL", "https://ai.sumopod.com/v1")
        env_lines.setdefault("OPENAI_BASE_URL", "https://api.openai.com/v1")
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("# ShopeeAgent Configuration\n# Generated by Settings Panel\n\n")
            for k, v in env_lines.items():
                f.write(f"{k}={v}\n")
