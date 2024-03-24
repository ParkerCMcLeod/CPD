# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Scale, HORIZONTAL, Entry, Label, Button, filedialog, messagebox
import sys
import Rbeast as rb

# Set constants for the GUI sliders
MOMENTUM_SLIDER_START, MOMENTUM_SLIDER_END = 1, 30
MA_SLIDER_START, MA_SLIDER_END = 1, 30
REVERSION_THRESHOLD_SLIDER_START, REVERSION_THRESHOLD_SLIDER_END = 0, 1000

# Initialize global variables
analysis_mode = "classic"  # Default analysis mode
df = pd.DataFrame()  # Dataframe to hold financial data
prices = pd.Series(dtype=float)  # Series to hold closing prices

def load_data(filepath):
    """Loads financial data from an Excel file and preprocesses it."""
    global df, prices
    try:
        # Load data
        df = pd.read_excel(filepath)
        # Convert Date and Time to string, then combine and convert to datetime
        df['Date'] = df['Date'].astype(str)
        df['Time'] = df['Time'].astype(str)
        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
        # Drop rows with invalid dates
        df.dropna(subset=['DateTime'], inplace=True)
        # Set DateTime as index
        df.set_index('DateTime', inplace=True)
        if 'Close' in df.columns:
            prices = df['Close']
            # Determine and display the date range of the data
            first_date = df.index.min()
            last_date_in_first_month = first_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)
            last_date = df.index.max()
            date_range_label.config(text=f"Avalible Range: {first_date} to {last_date}")
            populate_date_range(first_date, last_date_in_first_month) 
            # Update GUI to reflect available data
            update_plot()
        else:
            messagebox.showerror("Error", "Excel file does not contain a 'Close' column.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

def populate_date_range(start_datetime, end_datetime):
    """Updates GUI with the available date range for analysis."""
    start_datetime_entry.delete(0, "end")
    end_datetime_entry.delete(0, "end")
    start_datetime_entry.insert(0, start_datetime.strftime('%Y-%m-%d %H:%M:%S'))
    end_datetime_entry.insert(0, end_datetime.strftime('%Y-%m-%d %H:%M:%S'))

def calculate_momentum(prices, n_samples):
    """Calculates momentum as the difference between current and past prices."""
    return prices - prices.shift(n_samples)

def calculate_reversion(prices, m_samples):
    """Calculates price reversion from the moving average."""
    moving_average = prices.rolling(window=m_samples).mean()
    return prices - moving_average

def detect_change_points(prices, n_samples, m_samples, reversion_threshold):
    """Identifies change points in the price data based on momentum and reversion criteria."""
    momentum = calculate_momentum(prices, n_samples)
    reversion = calculate_reversion(prices, m_samples)
    momentum_change_points = (np.sign(momentum.shift(1)) != np.sign(momentum)) & (momentum.shift(1) != 0)
    reversion_change_points = reversion.abs() > reversion_threshold
    return momentum_change_points | reversion_change_points

def update_plot(event=None):
    """Updates the plot based on the selected analysis mode and parameters."""
    global prices, analysis_mode, fig, ax, canvas
    if df.empty or prices.empty:
        messagebox.showinfo("Info", "No data to display. Please load a file and ensure it has the correct format.")
        return
    try:
        # Filter data based on selected date range
        start_date = pd.to_datetime(start_datetime_entry.get())
        end_date = pd.to_datetime(end_datetime_entry.get())
        filtered_prices = prices[start_date:end_date]
        # Clear and update plot
        ax.clear()
        if analysis_mode == "classic":
            # Classic analysis mode: plot change points based on momentum and reversion
            n_samples = momentum_slider.get()
            m_samples = ma_slider.get()
            reversion_threshold = reversion_threshold_slider.get()
            change_points = detect_change_points(filtered_prices, n_samples, m_samples, reversion_threshold)
            ax.plot(filtered_prices.index, filtered_prices, label='Close Price', color='blue')
            change_points_dates = filtered_prices.index[change_points]
            ax.scatter(change_points_dates, filtered_prices[change_points], color='red', label='Change Points', zorder=5)
            ax.legend()
            canvas.draw()
        else:
            beast_result = rb.beast(filtered_prices.values, distribution='t', niter=15000, nBurnin=2000)

            # Plotting the results with a title indicating it's financial data
            rb.plot(beast_result, title='Enhanced Financial Data Analysis with RBeast')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update plot: {e}")

def open_file_dialog():
    """Opens a file dialog to select an Excel file for loading financial data."""
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if filepath:
        load_data(filepath)

def on_closing():
    """Handles the GUI window closing event."""
    window.destroy()
    sys.exit()

def setup_gui(window):
    """Sets up the GUI components for the application."""
    global start_datetime_entry, end_datetime_entry, momentum_slider, ma_slider, reversion_threshold_slider, date_range_label, fig, ax, canvas
    # Create and arrange GUI components
    Button(window, text="Open File", command=open_file_dialog).pack(pady=10)
    Label(window, text="Start Date and Time (YYYY-MM-DD HH:MM:SS):").pack()
    start_datetime_entry = Entry(window)
    start_datetime_entry.pack(pady=5)
    Label(window, text="End Date and Time (YYYY-MM-DD HH:MM:SS):").pack()
    end_datetime_entry = Entry(window)
    end_datetime_entry.pack(pady=5)
    date_range_label = Label(window, text="Available Date Range: N/A")
    date_range_label.pack(pady=5)
    Button(window, text="Apply Date and Time Range", command=update_plot).pack(pady=10)
    Button(window, text="Analyze with RBeast", command=analyze_with_rbeast).pack(pady=5)
    # Initialize matplotlib figure and canvas for plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    # Configure sliders for analysis parameters
    momentum_slider = Scale(window, from_=MOMENTUM_SLIDER_START, to=MOMENTUM_SLIDER_END, orient=HORIZONTAL, label="Momentum (Samples)")
    ma_slider = Scale(window, from_=MA_SLIDER_START, to=MA_SLIDER_END, orient=HORIZONTAL, label="Moving Average (Samples)")
    reversion_threshold_slider = Scale(window, from_=REVERSION_THRESHOLD_SLIDER_START, to=REVERSION_THRESHOLD_SLIDER_END, orient=HORIZONTAL, label="Reversion Threshold")
    momentum_slider.pack(fill='x', padx=50, pady=5)
    ma_slider.pack(fill='x', padx=50, pady=5)
    reversion_threshold_slider.pack(fill='x', padx=50, pady=5)
    # Bind sliders to the update plot function
    momentum_slider.bind("<ButtonRelease-1>", update_plot)
    ma_slider.bind("<ButtonRelease-1>", update_plot)
    reversion_threshold_slider.bind("<ButtonRelease-1>", update_plot)

def analyze_with_rbeast():
    """Performs advanced time series analysis using RBeast on the selected data."""
    global prices
    if df.empty or prices.empty:
        messagebox.showinfo("Info", "No data to display. Please load a file and ensure it has the correct format.")
        return
    try:
        # Filter data based on selected date range and perform RBeast analysis
        start_date = pd.to_datetime(start_datetime_entry.get())
        end_date = pd.to_datetime(end_datetime_entry.get())
        filtered_prices = prices[start_date:end_date]
        beast_result = rb.beast(filtered_prices.values, seasonality=1, distribution='Normal', niter=11000, nBurnin=1000)
        rb.plot(beast_result, title='Financial Data Analysis with RBeast')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to perform RBeast analysis: {e}")

if __name__ == "__main__":
    # Main entry point of the application
    window = Tk()
    setup_gui(window)
    window.mainloop()