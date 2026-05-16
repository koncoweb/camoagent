from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea,
    QFrame, QListWidget, QListWidgetItem,
    QTextEdit, QGroupBox, QFormLayout,
    QComboBox, QLineEdit, QSpinBox,
    QCheckBox, QProgressBar, QTableWidget,
    QTableWidgetItem, QTabWidget, QWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
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
    crew_status_update = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFF8F5;
                border-radius: 12px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("🤖 AI Crew Configuration")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #EE4D2D;")
        layout.addWidget(title)

        crew_info_group = QGroupBox("👥 Crew Structure")
        crew_info_group.setStyleSheet("""
            QGroupBox {
                color: #EE4D2D;
                border: 2px solid #F5A623;
                border-radius: 8px;
                margin-top: 12px;
                font-weight: bold;
                background-color: #FFFFFF;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
            }
        """)
        crew_layout = QVBoxLayout()

        process_row = QHBoxLayout()
        process_row.addWidget(QLabel("Process:"))
        self.process_label = QLabel("Sequential (Shopee Ads Workflow)")
        self.process_label.setStyleSheet("color: #333; font-weight: bold;")
        process_row.addWidget(self.process_label)
        process_row.addStretch()
        crew_layout.addLayout(process_row)

        crew_layout.addWidget(QLabel("<b>Agents:</b>"))

        agent_list = QListWidget()
        agent_list.setStyleSheet("""
            QListWidget {
                background-color: #FFF8F5;
                border: 1px solid #F5A623;
                border-radius: 8px;
                color: #333;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #FFE0CC;
            }
            QListWidget::item:selected {
                background-color: #EE4D2D;
                color: white;
            }
        """)
        agents = [
            ("🛒 ShopeeNavigator", "Navigates & extracts data from Shopee pages", "Active"),
            ("📊 FinancialAnalyst", "Calculates ROAS, Break-Even, Max CPC", "Active"),
            ("🎯 AdsOptimizer", "Generates bid optimization recommendations", "Active"),
        ]
        for name, desc, status in agents:
            item = QListWidgetItem(f"{name}\n   {desc} [{status}]")
            agent_list.addItem(item)
        agent_list.setMaximumHeight(130)
        crew_layout.addWidget(agent_list)
        crew_info_group.setLayout(crew_layout)
        layout.addWidget(crew_info_group)

        status_group = QGroupBox("📈 Live Status")
        status_group.setStyleSheet(crew_info_group.styleSheet())
        status_layout = QFormLayout()
        status_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)

        self.crew_status = QLabel("Idle")
        self.crew_status.setStyleSheet("color: #28A745; font-weight: bold; font-size: 14px;")
        status_layout.addRow("Status:", self.crew_status)

        self.current_task = QLabel("None")
        self.current_task.setStyleSheet("color: #666;")
        status_layout.addRow("Current Task:", self.current_task)

        self.tasks_completed = QLabel("0")
        self.tasks_completed.setStyleSheet("color: #EE4D2D; font-weight: bold; font-size: 14px;")
        status_layout.addRow("Tasks Done:", self.tasks_completed)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        layout.addStretch()

    def update_status(self, status: str, task: str = ""):
        status_colors = {
            "idle": "#28A745",
            "working": "#F5A623",
            "ready": "#28A745",
            "error": "#DC3545",
            "Shopee Crew": "#EE4D2D"
        }
        color = status_colors.get(status, "#666")
        self.crew_status.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        self.crew_status.setText(status.upper())
        if task:
            self.current_task.setText(task[:50] + "..." if len(task) > 50 else task)


class AnalyticsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFF8F5;
                border-radius: 12px;
            }
        """)
        self.task_history = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("📊 Analytics Dashboard")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #EE4D2D;")
        layout.addWidget(title)

        metrics_group = QGroupBox("📈 Performance Metrics")
        metrics_group.setStyleSheet("""
            QGroupBox {
                color: #EE4D2D;
                border: 2px solid #F5A623;
                border-radius: 8px;
                margin-top: 12px;
                font-weight: bold;
                background-color: #FFFFFF;
            }
        """)
        metrics_layout = QVBoxLayout()
        metrics_layout.setSpacing(12)

        tasks_row = self._create_metric_row("📋 Tasks Executed:", "0", "#EE4D2D")
        self.tasks_count = tasks_row[1]
        metrics_layout.addLayout(tasks_row[2])

        errors_row = self._create_metric_row("❌ Errors:", "0", "#DC3545")
        self.errors_count = errors_row[1]
        metrics_layout.addLayout(errors_row[2])

        tokens_row = self._create_metric_row("🔢 Est. Tokens:", "~0", "#666")
        self.tokens_count = tokens_row[1]
        metrics_layout.addLayout(tokens_row[2])

        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)

        history_label = QLabel("📋 Task History")
        history_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        history_label.setStyleSheet("color: #EE4D2D;")
        layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #FFFFFF;
                border: 2px solid #F5A623;
                border-radius: 8px;
                color: #333;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 8px;
            }
            QListWidget::item:selected {
                background-color: #EE4D2D;
                color: white;
            }
        """)
        layout.addWidget(self.history_list, stretch=1)

    def _create_metric_row(self, label_text: str, initial_value: str, color: str):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setStyleSheet("color: #666;")
        value_label = QLabel(initial_value)
        value_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")
        row.addWidget(label)
        row.addStretch()
        row.addWidget(value_label)
        return (label, value_label, row)

    def add_task(self, task: str, status: str = "success"):
        self.task_history.append({"task": task, "status": status})
        self.tasks_count.setText(str(len(self.task_history)))
        
        error_count = sum(1 for t in self.task_history if t["status"] == "error")
        self.errors_count.setText(str(error_count))
        
        est_tokens = len(self.task_history) * 1500
        self.tokens_count.setText(f"~{est_tokens:,}")
        
        status_icon = "✅" if status == "success" else "❌"
        item = QListWidgetItem(f"{status_icon} {task[:60]}...")
        self.history_list.addItem(item)
        self.history_list.scrollToBottom()


class SettingsPanel(QFrame):
    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFF8F5;
                border-radius: 12px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15)

        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #EE4D2D;")
        content_layout.addWidget(title)

        llm_group = QGroupBox("🤖 LLM Configuration")
        llm_group.setStyleSheet("""
            QGroupBox {
                color: #EE4D2D;
                border: 2px solid #F5A623;
                border-radius: 8px;
                margin-top: 12px;
                font-weight: bold;
                background-color: #FFFFFF;
            }
        """)
        llm_layout = QFormLayout()
        llm_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        llm_layout.setSpacing(10)

        provider_label = QLabel("Provider:")
        provider_label.setStyleSheet("color: #333; font-weight: normal;")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([
            "SumoPod AI",
            "Official OpenAI"
        ])
        self.provider_combo.setCurrentText("SumoPod AI")
        self.provider_combo.setStyleSheet(self._combobox_style())
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        llm_layout.addRow(provider_label, self.provider_combo)

        model_label = QLabel("Model:")
        model_label.setStyleSheet("color: #333; font-weight: normal;")
        self.model_combo = QComboBox()
        self._update_model_combo("SumoPod AI")
        self.model_combo.setStyleSheet(self._combobox_style())
        llm_layout.addRow(model_label, self.model_combo)

        max_iter_label = QLabel("Max Iterations:")
        max_iter_label.setStyleSheet("color: #333; font-weight: normal;")
        self.max_iter_spin = QSpinBox()
        self.max_iter_spin.setRange(1, 50)
        self.max_iter_spin.setValue(10)
        self.max_iter_spin.setStyleSheet(self._spinbox_style())
        llm_layout.addRow(max_iter_label, self.max_iter_spin)

        max_time_label = QLabel("Max Exec Time (s):")
        max_time_label.setStyleSheet("color: #333; font-weight: normal;")
        self.max_time_spin = QSpinBox()
        self.max_time_spin.setRange(30, 600)
        self.max_time_spin.setValue(120)
        self.max_time_spin.setStyleSheet(self._spinbox_style())
        llm_layout.addRow(max_time_label, self.max_time_spin)

        llm_group.setLayout(llm_layout)
        content_layout.addWidget(llm_group)

        browser_group = QGroupBox("🌐 Browser Settings")
        browser_group.setStyleSheet(llm_group.styleSheet())
        browser_layout = QFormLayout()
        browser_layout.setSpacing(10)

        self.headless_check = self._create_checkbox("Headless Mode")
        browser_layout.addRow(self.headless_check)

        self.humanize_check = self._create_checkbox("Humanize Mouse Movement")
        self.humanize_check.setChecked(True)
        browser_layout.addRow(self.humanize_check)

        browser_group.setLayout(browser_layout)
        content_layout.addWidget(browser_group)

        crew_group = QGroupBox("🔧 CrewAI Advanced")
        crew_group.setStyleSheet(llm_group.styleSheet())
        crew_layout = QFormLayout()
        crew_layout.setSpacing(10)

        self.memory_check = self._create_checkbox("Enable Memory (Requires OpenAI)")
        crew_layout.addRow(self.memory_check)

        self.planning_check = self._create_checkbox("Enable Planning (Requires OpenAI)")
        crew_layout.addRow(self.planning_check)

        self.openai_warning = QLabel("⚠️ Memory and Planning require Official OpenAI provider")
        self.openai_warning.setStyleSheet("color: #F5A623; font-size: 11px; font-style: italic; padding: 5px;")
        self.openai_warning.setWordWrap(True)
        crew_layout.addRow("", self.openai_warning)

        crew_group.setLayout(crew_layout)
        content_layout.addWidget(crew_group)

        api_group = QGroupBox("🔑 API Keys")
        api_group.setStyleSheet(llm_group.styleSheet())
        api_layout = QFormLayout()
        api_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        api_layout.setSpacing(10)

        sumpod_key_label = QLabel("SumoPod API Key:")
        sumpod_key_label.setStyleSheet("color: #333; font-weight: normal;")
        self.sumpod_key_input = QLineEdit()
        self.sumpod_key_input.setPlaceholderText("Enter your SumoPod API key...")
        self.sumpod_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.sumpod_key_input.setStyleSheet(self._lineedit_style())
        self._load_api_key("SUMOPOD_API_KEY", self.sumpod_key_input)
        api_layout.addRow(sumpod_key_label, self.sumpod_key_input)

        openai_key_label = QLabel("OpenAI API Key:")
        openai_key_label.setStyleSheet("color: #333; font-weight: normal;")
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText("Enter your OpenAI API key...")
        self.openai_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_input.setStyleSheet(self._lineedit_style())
        self._load_api_key("OPENAI_API_KEY", self.openai_key_input)
        api_layout.addRow(openai_key_label, self.openai_key_input)

        self.api_note = QLabel("💡 API keys entered here are used temporarily. For persistent storage, edit the .env file.")
        self.api_note.setStyleSheet("color: #F5A623; font-size: 10px; font-style: italic; padding: 5px;")
        self.api_note.setWordWrap(True)
        api_layout.addRow("", self.api_note)

        api_group.setLayout(api_layout)
        content_layout.addWidget(api_group)

        save_btn = QPushButton("💾 Apply Settings")
        save_btn.setFixedHeight(45)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #EE4D2D;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FF6347;
            }
            QPushButton:pressed {
                background-color: #CC3D1D;
            }
        """)
        save_btn.clicked.connect(self.on_save)
        content_layout.addWidget(save_btn)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.on_provider_changed("SumoPod AI")

    def _combobox_style(self) -> str:
        return """
            QComboBox {
                background-color: #FFF8F5;
                color: #333;
                border: 2px solid #F5A623;
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #EE4D2D;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                color: #333;
                border: 1px solid #F5A623;
                selection-background-color: #EE4D2D;
            }
        """

    def _spinbox_style(self) -> str:
        return """
            QSpinBox {
                background-color: #FFF8F5;
                color: #333;
                border: 2px solid #F5A623;
                border-radius: 6px;
                padding: 6px 10px;
                min-width: 80px;
            }
            QSpinBox:hover {
                border-color: #EE4D2D;
            }
        """

    def _lineedit_style(self) -> str:
        return """
            QLineEdit {
                background-color: #FFFFFF;
                color: #333;
                border: 2px solid #F5A623;
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 200px;
            }
            QLineEdit:hover {
                border-color: #EE4D2D;
            }
            QLineEdit:focus {
                border-color: #EE4D2D;
            }
        """

    def _load_api_key(self, key_name: str, input_field: QLineEdit):
        load_dotenv()
        api_key = os.environ.get(key_name, "")
        if api_key:
            input_field.setText(api_key)
            input_field.setPlaceholderText(f"Loaded from .env (change here to override)")

    def _create_checkbox(self, text: str) -> QCheckBox:
        cb = QCheckBox(text)
        cb.setStyleSheet("""
            QCheckBox {
                color: #333;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #F5A623;
                border-radius: 4px;
                background-color: #FFFFFF;
            }
            QCheckBox::indicator:checked {
                background-color: #EE4D2D;
                border-color: #EE4D2D;
            }
            QCheckBox::indicator:hover {
                border-color: #EE4D2D;
            }
        """)
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

        if provider == "SumoPod AI":
            self.memory_check.setChecked(False)
            self.memory_check.setEnabled(False)
            self.planning_check.setChecked(False)
            self.planning_check.setEnabled(False)
            self.openai_warning.setVisible(True)
        else:
            self.memory_check.setEnabled(True)
            self.planning_check.setEnabled(True)
            self.openai_warning.setVisible(False)

    def on_save(self):
        sumpod_key = self.sumpod_key_input.text().strip()
        openai_key = self.openai_key_input.text().strip()
        
        if sumpod_key:
            os.environ["SUMOPOD_API_KEY"] = sumpod_key
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        settings = {
            "provider": self.provider_combo.currentText(),
            "model": self.model_combo.currentText(),
            "max_iter": self.max_iter_spin.value(),
            "max_time": self.max_time_spin.value(),
            "headless": self.headless_check.isChecked(),
            "humanize": self.humanize_check.isChecked(),
            "memory": self.memory_check.isChecked(),
            "planning": self.planning_check.isChecked(),
            "sumpod_api_key": sumpod_key if sumpod_key else os.environ.get("SUMOPOD_API_KEY", ""),
            "openai_api_key": openai_key if openai_key else os.environ.get("OPENAI_API_KEY", "")
        }
        self.settings_changed.emit(settings)
