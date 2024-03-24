Here's a README.md file tailored for your Python script, combining the best aspects of clarity, structure, and explanation:

**README.md**

**Financial Data Analysis Tool**

This Python script provides tools for analyzing financial data and identifying potential trading opportunities based on two analysis modes:

1. **Classic Analysis:** Detects significant change points in price data through momentum and mean reversion calculations.
2. **Advanced Analysis with RBeast:**  Offers sophisticated time series analysis using the RBeast library for detecting trends, seasonality, and change points.

**Prerequisites**

* Python 3 ([https://www.python.org/](https://www.python.org/))
* **Required Libraries:** 
    * numpy
    * pandas
    * matplotlib
    * tkinter
    * Rbeast ([https://github.com/zhaokg/Rbeast](https://github.com/zhaokg/Rbeast)) 

**Installation**

1. Download or clone this repository.
2. Install required libraries using pip:
    ```bash
    pip install numpy pandas matplotlib tkinter Rbeast
    ```

**Usage**

1. **Load Data:** Click the "Open File" button to select an Excel file containing your financial data. The file should have the following columns:
    * **Date:** Date of the data point.
    * **Time:** Time of the data point.
    * **Close:** Closing price of the asset.

2. **Select Date Range:** Enter the desired start and end dates in the "YYYY-MM-DD HH:MM:SS" format and click "Apply Date and Time Range".

3. **Classic Analysis:**
   * **Momentum (Samples):** Adjust the slider to control lookback samples for calculating momentum.
   * **Moving Average (Samples):** Adjust the slider to select the window size for the moving average.
   * **Reversion Threshold:** Adjust the slider to set the threshold for mean reversion detection. 
   * The plot will automatically update to highlight change points.

4. **Advanced Analysis with RBeast:** Click the "Analyze with RBeast" button for in-depth time series analysis. RBeast results will be shown in a separate window.

**GUI Explanation:**

* **Open File Button:** Loads financial data from an Excel file.
* **Start/End Date and Time:** Input fields for specifying the analysis period.
* **Available Date Range:** Label displaying the available date range in the loaded data.
* **Apply Date and Time Range Button:** Filters the data and updates the plot.
* **Analyze with RBeast Button:** Performs advanced analysis with the RBeast library.
* **Sliders:** Adjust parameters for the classic analysis mode.
* **Plot:** Displays the financial data and detected change points (Classic) or RBeast analysis results.

**Example**

```bash
python CPD.py
```