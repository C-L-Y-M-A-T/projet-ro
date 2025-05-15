modern_table_style = """
    /* Table Widget Styles */
    QTableWidget {
        background-color: white;
        alternate-background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        gridline-color: #e5e7eb;
        selection-background-color: #e0e7ff;
        selection-color: #1f2937;
    }
    
    QTableWidget::item {
        padding: 8px;
        border-bottom: 1px solid #f3f4f6;
    }
    
    QTableWidget::item:selected {
        background-color: #e0e7ff;
        color: #1f2937;
    }
    
    QTableWidget::item:hover:!selected {
        background-color: #f1f5f9;
    }
    
    QHeaderView::section {
        background-color: #f3f4f6;
        color: #4b5563;
        font-weight: bold;
        padding: 10px;
        border: none;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
    }
    
    QHeaderView::section:first {
        border-top-left-radius: 8px;
    }
    
    QHeaderView::section:last {
        border-top-right-radius: 8px;
        border-right: none;
    }
    
    QHeaderView::section:hover {
        background-color: #e5e7eb;
    }
    
    QTableCornerButton::section {
        background-color: #f3f4f6;
        border: none;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
    }
"""
