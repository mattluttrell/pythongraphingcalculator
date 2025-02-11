# AI-Generated Graphing Calculator

This project showcases an interesting experiment where an AI (Claude) wrote a fully functional graphing calculator in just two minutes. While the code has undergone minor refinements, the core implementation was entirely AI-generated, demonstrating the capabilities of modern AI in rapidly producing practical software solutions.

## Features

- Interactive function plotting with real-time updates
- Support for common mathematical functions (sin, cos, tan, exp, log, sqrt, abs)
- Mathematical constants (pi, e)
- Dynamic X and Y range controls via sliders
- Robust error handling and domain validation
- Grid display with coordinate axes
- Support for both 'x' and 'theta' variable notation

## Developer Tools

This project was developed using a modern AI-assisted development stack:

- **Claude AI**: Used both through direct API access and OpenRouter, depending on load and cost efficiency
- **Cline**: A specialized development environment optimized for AI pair programming
- **VS Code**: Primary code editor with integrated AI assistance

The combination of Claude's direct API and OpenRouter provides flexibility in managing costs and response times, though optimal cost efficiency between the two can vary.

## Installation

1. Ensure you have Python 3.x installed
2. Clone this repository
3. Install required dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- numpy
- PySide6
- matplotlib

## Running the Application

To start the graphing calculator:

```bash
python main.py
```

## Usage

1. Enter a mathematical function in the input field (e.g., "sin(x)", "x^2", "2*theta + 1")
2. Use the X Range slider to adjust the visible domain
3. Use the Y Scale slider to adjust the visible range
4. Press Enter to plot the function

The calculator supports various mathematical expressions and will provide helpful error messages for invalid inputs or domain errors.
