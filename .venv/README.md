# Battery Health Monitor

A modern Windows desktop application developed using Python and CustomTkinter.

## Features

- Modern graphical interface with dark theme
- Battery health monitoring dashboard
- Demo Mode with simulated battery information
- Real Mode with battery detection
- Current battery charge monitoring
- Standalone Windows executable

## Technologies

- Python
- CustomTkinter
- psutil
- PyInstaller

## Installation

1. Clone the repository.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Current Limitations

The current Real Mode detects battery availability and charge level, but automatic extraction of battery health and cycle count is not yet implemented.

## Future Improvements

- PowerCFG battery report integration
- Battery health history
- Interactive charts
- SQLite database

## Author

Developed as a personal Python software development portfolio project.