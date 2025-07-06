# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based data visualization dashboard for analyzing typing performance data from NerdType. The application is a single-file Python application that provides comprehensive insights into typing speed, accuracy, and performance trends.

## Development Commands

### Running the Application
```bash
# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run nerdtype_dashboard.py
```

### Dependencies Management
- All dependencies are listed in `requirements.txt`
- Main dependencies: Streamlit, Pandas, NumPy, Plotly, Pillow, SciPy, StatsModels
- No package.json or build system - this is a pure Python project

## Architecture

### Single-File Application Structure
The entire application is contained in `nerdtype_dashboard.py` with the following main components:

1. **Theme Configuration** (lines 14-32): Custom color scheme and styling constants
2. **CSS Styling** (lines 34-155): Extensive custom CSS for UI theming
3. **Data Processing** (lines 170-194): `load_data()` function for JSON parsing and DataFrame preparation
4. **Visualization Components**: Multiple chart types using Plotly
   - Performance trends over time
   - WPM vs Accuracy scatter plots
   - Daily activity heatmaps
   - Learning curve analysis
   - Score progression tracking
   - Performance consistency analysis

### Data Flow
1. User uploads JSON file containing typing game data
2. `load_data()` processes the JSON into a Pandas DataFrame
3. Data is cleaned and prepared (date parsing, accuracy conversion, missing field handling)
4. Multiple visualization components render different aspects of the data
5. All charts use the custom theme for consistent styling

### Key Features
- **Multi-mode Support**: Handles different game modes including "Zen Mode" which has different data structure
- **Responsive Design**: Uses Streamlit columns for layout
- **Interactive Charts**: All visualizations are interactive Plotly charts
- **Performance Analytics**: Includes advanced metrics like score efficiency and consistency analysis
- **Time Series Analysis**: Tracks performance trends with moving averages and trend lines

## File Structure
```
├── nerdtype_dashboard.py     # Main application file
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── game-data-test.json      # Sample data file
└── images/                  # Logo and branding assets
    ├── logo-no-keyboard-blue-bg-32x32.png
    ├── logo-text-link.png
    └── nt-logo-text-link.png
```

## Working with the Code

### Adding New Visualizations
- All charts follow the same pattern: data preparation → Plotly figure creation → theme application → layout updates
- Use the `theme` dictionary for consistent colors
- Apply `paper_bgcolor`, `plot_bgcolor`, and `font` styling to all charts
- Update grid colors using `update_xaxes()` and `update_yaxes()`

### Data Handling
- The app expects JSON data with specific fields: `wpm`, `accuracy`, `date`, `mode`, `wordList`, `score`
- Handle missing fields gracefully (see `timeLeft` and `totalTime` handling)
- Always sort by date for time-series analysis
- Use `pd.to_datetime()` for date parsing with the format `"%d/%m/%Y, %H:%M:%S"`

### Styling
- All custom CSS is defined in a single `st.markdown()` block
- Use CSS classes like `.main-header`, `.sub-header`, `.metric-card` for consistent styling
- Theme colors are referenced from the `theme` dictionary
- Streamlit components are styled using data-testid selectors

## Testing
- No automated tests are present in this repository
- Testing is done manually by running the application and uploading sample data
- Use `game-data-test.json` for testing functionality

## Deployment
- The app is deployed on Streamlit Cloud at: https://nerdtype-dashboard.streamlit.app/
- No build process required - Streamlit handles deployment directly from the repository