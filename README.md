# Time Series Visualization

This is a Dash app that visualizes correlations between the cyclical components of GDP and different labor transitions rates for various age groups..

## Dataset

The dataset used in this app is stored in the `correlationGDP.csv` file. Make sure to place this file in the same directory as the `app.py` file.

## Installation

To run this app locally, follow these steps:

1. Clone this repository: `git clone <repository-url>`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

The app will be accessible at `http://localhost:8057` in your web browser.

## Usage

1. Select a flow variable from the dropdown menu to visualize the corresponding data.
2. Choose one age groups from the dropdown menu to filter the data.
3. The line chart will update dynamically based on your selections.

Feel free to explore different flow variables and age groups to gain insights from the visualizations.

## Dependencies

This app is built using the following Python libraries:

- Dash: [dash](https://pypi.org/project/dash/)
- Pandas: [pandas](https://pypi.org/project/pandas/)
- Plotly: [plotly](https://pypi.org/project/plotly/)

Make sure to install these dependencies before running the app.

## License

This project is licensed under the [MIT License](LICENSE).

