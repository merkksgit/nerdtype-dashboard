# NerdType Dashboard

Data visualization dashboard for analyzing your typing performance from NerdType. This Streamlit application provides insights into your typing speed, accuracy, and overall performance.

## App URL

[NerdType Dashboard](https://nerdtype-dashboard.streamlit.app/)

## Test data file

The repository includes a test data file: game-data-test.json, you can download it with:

```
wget https://raw.githubusercontent.com/merkksgit/nerdtype-dashboard/refs/heads/main/game-data-test.json
```

## Installation

1. Clone this repository:

```bash
git clone git@github.com:merkksgit/nerdtype-dashboard.git
cd nerdtype-dashboard
```

2. Set up a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
.venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source .venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run nerdtype_dashboard.py
```

5. When you're done, deactivate the virtual environment:

```bash
deactivate
```

## Usage

1. Export your typing data from NerdType as a JSON file
2. Launch the dashboard and upload your JSON file
3. Explore your typing performance metrics and trends

## Requirements

See the [requirements.txt](requirements.txt) file for a complete list of dependencies.
