from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea,
    QFrame, QListWidget, QListWidgetItem,
    QTextEdit, QGroupBox, QFormLayout,
    QComboBox, QLineEdit, QSpinBox,
    QCheckBox, QProgressBar, QTableWidget,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont


class CrewPanel(QFrame):
    crew_status_update = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-radius: 8px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("🤖 Crew Configuration")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #4EC9B0;")
        layout.addWidget(title)

        crew_info_group = QGroupBox("Crew Structure")
        crew_info_group.setStyleSheet("""
            QGroupBox {
                color: #888;
                border: 1px solid #333;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        crew_layout = QVBoxLayout()

        self.process_label = QLabel("Process: Hierarchical (Manager Agent)")
        self.process_label.setStyleSheet("color: #CCC; font-size: 12px;")
        crew_layout.addWidget(self.process_label)

        agents_label = QLabel("Agents:")
        agents_label.setStyleSheet("color: #888; font-size: 11px; font-weight: bold;")
        crew_layout.addWidget(agents_label)

        agent_list = QListWidget()
        agent_list.setStyleSheet("""
            QListWidget {
                background-color: #252526;
                border: none;
                color: #CCC;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #094771;
            }
        """)
        agents = [
            ("Navigator", "🌐", "Navigates and interacts with web pages", "Active"),
            ("Scraper", "📥", "Extracts structured data from pages", "Active"),
            ("Analyst", "📊", "Analyzes and provides insights", "Active"),
            ("Manager (Auto)", "👔", "Orchestrates task delegation", "Running"),
        ]
        for name, icon, desc, status in agents:
            item = QListWidgetItem(f"{icon} {name} — {desc} [{status}]")
            agent_list.addItem(item)
        agent_list.setMaximumHeight(140)
        crew_layout.addWidget(agent_list)
        crew_info_group.setLayout(crew_layout)
        layout.addWidget(crew_info_group)

        status_group = QGroupBox("Live Status")
        status_group.setStyleSheet(crew_info_group.styleSheet())
        status_layout = QFormLayout()

        self.crew_status = QLabel("Idle")
        self.crew_status.setStyleSheet("color: #4EC9B0; font-weight: bold;")
        status_layout.addRow("Status:", self.crew_status)

        self.current_task = QLabel("None")
        self.current_task.setStyleSheet("color: #DCDCAA;")
        status_layout.addRow("Current Task:", self.current_task)

        self.tasks_completed = QLabel("0")
        self.tasks_completed.setStyleSheet("color: #CCC;")
        status_layout.addRow("Tasks Completed:", self.tasks_completed)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        layout.addStretch()

    def update_status(self, status: str, task: str = ""):
        status_colors = {
            "idle": "#4EC9B0",
            "working": "#DCDCAA",
            "ready": "#4EC9B0",
            "error": "#F14C4C"
        }
        self.crew_status.setStyleSheet(f"color: {status_colors.get(status, '#CCC')}; font-weight: bold;")
        self.crew_status.setText(status.upper())
        if task:
            self.current_task.setText(task[:50] + "..." if len(task) > 50 else task)


class AnalyticsPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border-radius: 8px;
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
        title.setStyleSheet("color: #4EC9B0;")
        layout.addWidget(title)

        metrics_group = QGroupBox("Performance Metrics")
        metrics_group.setStyleSheet("""
            QGroupBox {
                color: #888;
                border: 1px solid #333;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
        """)
        metrics_layout = QVBoxLayout()

        tasks_row = QHBoxLayout()
        tasks_label = QLabel("Tasks Executed:")
        tasks_label.setStyleSheet("color: #888;")
        self.tasks_count = QLabel("0")
        self.tasks_count.setStyleSheet("color: #CCC; font-size: 20px; font-weight: bold;")
        tasks_row.addWidget(tasks_label)
        tasks_row.addStretch()
        tasks_row.addWidget(self.tasks_count)
        metrics_layout.addLayout(tasks_row)

        errors_row = QHBoxLayout()
        errors_label = QLabel("Errors:")
        errors_label.setStyleSheet("color: #888;")
        self.errors_count = QLabel("0")
        self.errors_count.setStyleSheet("color: #F14C4C; font-size: 20px; font-weight: bold;")
        errors_row.addWidget(errors_label)
        errors_row.addStretch()
        errors_row.addWidget(self.errors_count)
        metrics_layout.addLayout(errors_row)

        tokens_row = QHBoxLayout()
        tokens_label = QLabel("Est. Tokens Used:")
        tokens_label.setStyleSheet("color: #888;")
        self.tokens_count = QLabel("~0")
        self.tokens_count.setStyleSheet("color: #CCC; font-size: 20px; font-weight: bold;")
        tokens_row.addWidget(tokens_label)
        tokens_row.addStretch()
        tokens_row.addWidget(self.tokens_count)
        metrics_layout.addLayout(tokens_row)

        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)

        history_label = QLabel("📋 Task History")
        history_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        history_label.setStyleSheet("color: #888;")
        layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #252526;
                border: 1px solid #333;
                color: #CCC;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 6px;
            }
        """)
        layout.addWidget(self.history_list, stretch=1)

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
                background-color: #1E1E1E;
                border-radius: 8px;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #4EC9B0;")
        layout.addWidget(title)

        llm_group = QGroupBox("LLM Configuration")
        llm_group.setStyleSheet("""
            QGroupBox {
                color: #888;
                border: 1px solid #333;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
            }
        """)
        llm_layout = QFormLayout()

        provider_label = QLabel("Provider:")
        provider_label.setStyleSheet("color: #CCC;")
        self.provider_combo = QComboBox()
        self.provider_combo.addItems([
            "SumoPod AI",
            "Official OpenAI"
        ])
        self.provider_combo.setCurrentText("SumoPod AI")
        self.provider_combo.setStyleSheet("""
            QComboBox {
                background-color: #3C3C3C;
                color: #CCC;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        llm_layout.addRow(provider_label, self.provider_combo)

        model_label = QLabel("Model:")
        model_label.setStyleSheet("color: #CCC;")
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "deepseek-v4-pro",
            "gpt-4o-mini",
            "gpt-4o",
            "claude-3-opus"
        ])
        self.model_combo.setCurrentText("deepseek-v4-pro")
        self.model_combo.setStyleSheet("""
            QComboBox {
                background-color: #3C3C3C;
                color: #CCC;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        llm_layout.addRow(model_label, self.model_combo)

        max_iter_label = QLabel("Max Iterations:")
        max_iter_label.setStyleSheet("color: #CCC;")
        self.max_iter_spin = QSpinBox()
        self.max_iter_spin.setRange(1, 50)
        self.max_iter_spin.setValue(10)
        self.max_iter_spin.setStyleSheet("""
            QSpinBox {
                background-color: #3C3C3C;
                color: #CCC;
                border: none;
                padding: 5px;
                border-radius: 4px;
            }
        """)
        llm_layout.addRow(max_iter_label, self.max_iter_spin)

        max_time_label = QLabel("Max Exec Time (s):")
        max_time_label.setStyleSheet("color: #CCC;")
        self.max_time_spin = QSpinBox()
        self.max_time_spin.setRange(30, 600)
        self.max_time_spin.setValue(120)
        self.max_time_spin.setStyleSheet(self.max_iter_spin.styleSheet())
        llm_layout.addRow(max_time_label, self.max_time_spin)

        llm_group.setLayout(llm_layout)
        layout.addWidget(llm_group)

        browser_group = QGroupBox("Browser Settings")
        browser_group.setStyleSheet(llm_group.styleSheet())
        browser_layout = QFormLayout()

        self.headless_check = QCheckBox("Headless Mode")
        self.headless_check.setStyleSheet("""
            QCheckBox {
                color: #CCC;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
        """)
        browser_layout.addRow(self.headless_check)

        self.humanize_check = QCheckBox("Humanize Mouse Movement")
        self.humanize_check.setChecked(True)
        self.humanize_check.setStyleSheet(self.headless_check.styleSheet())
        browser_layout.addRow(self.humanize_check)

        browser_group.setLayout(browser_layout)
        layout.addWidget(browser_group)

        crew_group = QGroupBox("CrewAI Advanced Settings")
        crew_group.setStyleSheet(llm_group.styleSheet())
        crew_layout = QFormLayout()

        self.memory_check = QCheckBox("Enable Memory (Requires OpenAI Embeddings)")
        self.memory_check.setChecked(False)
        self.memory_check.setStyleSheet(self.headless_check.styleSheet())
        crew_layout.addRow(self.memory_check)

        self.planning_check = QCheckBox("Enable Planning (Enhances Task Accuracy)")
        self.planning_check.setChecked(False)
        self.planning_check.setStyleSheet(self.headless_check.styleSheet())
        crew_layout.addRow(self.planning_check)

        self.openai_warning = QLabel("⚠️ Memory and Planning are disabled. They require the Official OpenAI provider to use OpenAI Embeddings.")
        self.openai_warning.setStyleSheet("color: #E5B567; font-size: 11px; font-style: italic;")
        self.openai_warning.setWordWrap(True)
        crew_layout.addRow(self.openai_warning)
        
        crew_group.setLayout(crew_layout)
        layout.addWidget(crew_group)

        api_group = QGroupBox("API Status")
        api_group.setStyleSheet(llm_group.styleSheet())
        api_layout = QVBoxLayout()

        api_row = QHBoxLayout()
        self.api_status_label = QLabel("Provider Status:")
        self.api_status_label.setStyleSheet("color: #888;")
        self.api_status = QLabel("🟢 Connected")
        self.api_status.setStyleSheet("color: #4EC9B0; font-weight: bold;")
        api_row.addWidget(self.api_status_label)
        api_row.addStretch()
        api_row.addWidget(self.api_status)
        api_layout.addLayout(api_row)

        self.base_url_label = QLabel("Base URL: ai.sumopod.com/v1")
        self.base_url_label.setStyleSheet("color: #666; font-size: 11px;")
        api_layout.addWidget(self.base_url_label)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        save_btn = QPushButton("💾 Apply Settings")
        save_btn.setFixedHeight(40)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0E639C;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177BB;
            }
        """)
        save_btn.clicked.connect(self.on_save)
        layout.addWidget(save_btn)

        layout.addStretch()
        
        # Initialize provider state
        self.on_provider_changed(self.provider_combo.currentText())

    def on_provider_changed(self, provider: str):
        if provider == "SumoPod AI":
            self.memory_check.setChecked(False)
            self.planning_check.setChecked(False)
            self.memory_check.setEnabled(False)
            self.planning_check.setEnabled(False)
            self.openai_warning.setVisible(True)
            if hasattr(self, 'base_url_label'):
                self.api_status.setText("🟢 SumoPod Active")
                self.base_url_label.setText("Base URL: ai.sumopod.com/v1")
        else:
            self.memory_check.setEnabled(True)
            self.planning_check.setEnabled(True)
            self.openai_warning.setVisible(False)
            if hasattr(self, 'base_url_label'):
                self.api_status.setText("🟢 OpenAI Active")
                self.base_url_label.setText("Base URL: api.openai.com/v1")

    def on_save(self):
        settings = {
            "provider": self.provider_combo.currentText(),
            "model": self.model_combo.currentText(),
            "max_iter": self.max_iter_spin.value(),
            "max_time": self.max_time_spin.value(),
            "headless": self.headless_check.isChecked(),
            "humanize": self.humanize_check.isChecked(),
            "memory": self.memory_check.isChecked(),
            "planning": self.planning_check.isChecked()
        }
        self.settings_changed.emit(settings)
