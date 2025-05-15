modern_style = """
    /* Global Styles */
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
        color: #1f2937;
    }
    
    QMainWindow {
        background-color: #f9fafb;
    }
    
    /* Tab Widget Styles */
    QTabWidget::pane {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        background-color: white;
        top: -1px;
    }
    
    QTabBar::tab {
        background-color: #f3f4f6;
        color: #4b5563;
        border: 1px solid #e5e7eb;
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        padding: 10px 20px;
        margin-right: 4px;
        font-weight: 500;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        color: #4f46e5;
        border-bottom: 2px solid #4f46e5;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #e5e7eb;
    }
    
    /* Button Styles */
    QPushButton {
        background-color: #f3f4f6;
        color: #1f2937;
        border: 1px solid #d1d5db;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: #e5e7eb;
        border-color: #9ca3af;
    }
    
    QPushButton:pressed {
        background-color: #d1d5db;
    }
    
    QPushButton:disabled {
        background-color: #f3f4f6;
        color: #9ca3af;
        border-color: #e5e7eb;
    }
    
    /* Group Box Styles */
    QGroupBox {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        margin-top: 20px;
        padding-top: 25px;
        padding-bottom: 10px;
        padding-left: 10px;
        padding-right: 10px;
        font-weight: bold;
        color: #4f46e5;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 15px;
        padding: 0 5px;
        background-color: white;
    }
    
    /* Form Input Styles */
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
        background-color: white;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        padding: 8px 12px;
        min-height: 20px;
    }
    
    QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {
        border-color: #9ca3af;
    }
    
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
        border-color: #4f46e5;
    }
    
    /* Spin Box Styles */
    QSpinBox, QDoubleSpinBox {
        padding-right: 20px;
    }
    
    QSpinBox::up-button, QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 20px;
        height: 12px;
        border-left: 1px solid #d1d5db;
        border-bottom: 1px solid #d1d5db;
        border-top-right-radius: 5px;
        background-color: #f9fafb;
    }
    
    QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover {
        background-color: #e5e7eb;
    }
    
    QSpinBox::down-button, QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 20px;
        height: 12px;
        border-left: 1px solid #d1d5db;
        border-top: 1px solid #d1d5db;
        border-bottom-right-radius: 5px;
        background-color: #f9fafb;
    }
    
    QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
        background-color: #e5e7eb;
    }
    
    /* Combo Box Styles */
    QComboBox {
        padding-right: 20px;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 20px;
        border-left: 1px solid #d1d5db;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }
    
    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
        image: url(icons/chevron-down.png);
    }
    
    QComboBox QAbstractItemView {
        border: 1px solid #d1d5db;
        border-radius: 6px;
        background-color: white;
        selection-background-color: #e5e7eb;
        selection-color: #1f2937;
    }
    
    /* Scroll Bar Styles */
    QScrollBar:vertical {
        border: none;
        background: #f1f5f9;
        width: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical {
        background: #cbd5e1;
        min-height: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #94a3b8;
    }
    
    QScrollBar::handle:vertical:pressed {
        background: #64748b;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        border: none;
        background: none;
        height: 0px;
    }
    
    QScrollBar:horizontal {
        border: none;
        background: #f1f5f9;
        height: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:horizontal {
        background: #cbd5e1;
        min-width: 20px;
        border-radius: 5px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background: #94a3b8;
    }
    
    QScrollBar::handle:horizontal:pressed {
        background: #64748b;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal,
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        border: none;
        background: none;
        width: 0px;
    }
    
    /* Progress Bar Styles */
    QProgressBar {
        border: none;
        border-radius: 4px;
        background-color: #e5e7eb;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    
    QProgressBar::chunk {
        background-color: #4f46e5;
        border-radius: 4px;
    }
    
    /* Status Bar Styles */
    QStatusBar {
        background-color: white;
        color: #6b7280;
        border-top: 1px solid #e5e7eb;
    }
    
    /* Label Styles */
    QLabel {
        color: #1f2937;
    }
    
    /* Splitter Styles */
    QSplitter::handle {
        background-color: #e5e7eb;
    }
    
    QSplitter::handle:horizontal {
        width: 1px;
    }
    
    QSplitter::handle:vertical {
        height: 1px;
    }
"""
