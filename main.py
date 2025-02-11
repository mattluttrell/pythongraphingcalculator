import sys
import numpy as np
import warnings
warnings.filterwarnings('ignore')  # Suppress numpy warnings
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLineEdit, QLabel, QSlider, QMessageBox)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)
        
        # Set stylesheet to suppress button height warnings
        QApplication.instance().setStyleSheet("""
            QPushButton {
                min-height: 24px;
                max-height: 24px;
            }
        """)

        # Create the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas)

        # Create function input
        function_label = QLabel("Y = ")
        layout.addWidget(function_label)
        self.function_input = QLineEdit()
        self.function_input.setPlaceholderText("Enter function (e.g., sin(x), theta**2, 2x + 1)")
        self.function_input.returnPressed.connect(self.update_plot)
        layout.addWidget(self.function_input)

        # Create X range slider
        x_label = QLabel("X Range (-100 to 100):")
        layout.addWidget(x_label)
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setMinimum(1)
        self.x_slider.setMaximum(100)
        self.x_slider.setValue(10)
        layout.addWidget(self.x_slider)

        # Create Y range slider
        y_label = QLabel("Y Scale (-100 to 100):")
        layout.addWidget(y_label)
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setMinimum(1)
        self.y_slider.setMaximum(100)
        self.y_slider.setValue(10)
        layout.addWidget(self.y_slider)

        # Connect sliders after initialization
        self.x_slider.valueChanged.connect(self.on_slider_change)
        self.y_slider.valueChanged.connect(self.on_slider_change)

        # Initial plot setup
        self.last_valid_function = ""
        self.setup_plot()

    def setup_plot(self):
        """Initial plot setup with axes and grid"""
        self.ax.clear()
        self.ax.grid(True)
        self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        x_range = self.x_slider.value()
        y_range = self.y_slider.value()
        self.ax.set_xlim(-x_range, x_range)
        self.ax.set_ylim(-y_range, y_range)
        self.canvas.draw()

    def on_slider_change(self):
        """Handle slider value changes"""
        if self.last_valid_function:
            self.plot_function(self.last_valid_function)
        else:
            self.setup_plot()

    def update_plot(self):
        """Handle function input changes"""
        func_str = self.function_input.text().strip()
        if not func_str:
            self.last_valid_function = ""
            self.setup_plot()
            return
        
        self.plot_function(func_str)

    def plot_function(self, func_str):
        """Plot the given function"""
        try:
            # Create x values based on slider
            x_range = self.x_slider.value()
            x = np.linspace(-x_range, x_range, 1000)

            # Replace ^ with ** for exponentiation
            func_str = func_str.replace('^', '**')
            
            # Preprocess the function string to handle implicit multiplication
            import re
            # Handle coefficient before x or theta (e.g., 2x -> 2*x, 2theta -> 2*theta)
            func_str = re.sub(r'(\d+)([x]|theta)', r'\1*\2', func_str)
            # Handle coefficient before parentheses (e.g., 2(x+1) -> 2*(x+1))
            func_str = re.sub(r'(\d+)(\()', r'\1*\2', func_str)
            # Handle coefficient before functions (e.g., 2sin(x) -> 2*sin(x))
            func_str = re.sub(r'(\d+)(sin|cos|tan|log|sqrt)', r'\1*\2', func_str)
            # Handle coefficients inside trig functions (e.g., sin(2x) -> sin(2*x), sin(2theta) -> sin(2*theta))
            func_str = re.sub(r'(sin|cos|tan)\((\d+)([x]|theta)', r'\1(\2*\3', func_str)
            
            # Create safe versions of math functions that handle domain errors
            def safe_sqrt(x):
                with np.errstate(invalid='ignore'):
                    result = np.sqrt(x)
                    if np.any(np.isnan(result)):
                        raise ValueError("sqrt domain error: cannot compute square root of negative numbers")
                    return result

            def safe_log(x):
                with np.errstate(invalid='ignore', divide='ignore'):
                    result = np.log(x)
                    if np.any(np.isnan(result)) or np.any(np.isinf(result)):
                        raise ValueError("log domain error: input must be positive")
                    return result

            # Create a safe dictionary of allowed names with common math functions
            safe_dict = {
                "x": x,
                "theta": x,  # Allow theta as an alternative to x
                "np": np,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "log": safe_log,
                "sqrt": safe_sqrt,
                "abs": np.abs,
                "pi": np.pi,
                "e": np.e
            }
            
            # Evaluate the function
            y = eval(func_str, {"__builtins__": None}, safe_dict)

            if isinstance(y, np.ndarray) and len(y) == len(x):
                self.last_valid_function = func_str
                
                # Update the plot
                self.ax.clear()
                self.ax.grid(True)
                self.ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
                self.ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
                
                # Set axis limits
                y_scale = self.y_slider.value()
                self.ax.set_xlim(-x_range, x_range)
                self.ax.set_ylim(-y_scale, y_scale)
                
                # Plot the function
                self.ax.plot(x, y)
                
                # Refresh the canvas
                self.canvas.draw()
        except Exception as e:
            error_msg = str(e)
            if "domain error" in error_msg:
                QMessageBox.warning(self, "Domain Error", f"{error_msg}")
            else:
                QMessageBox.warning(self, "Error", f"Error plotting function: {error_msg}\n\nTip: Available functions include: sin, cos, tan, exp, log, sqrt, abs\nConstants: pi, e")
            return

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
