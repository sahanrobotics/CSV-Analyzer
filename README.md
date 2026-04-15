# 📈 Modern CSV Data Plotter Pro

A professional, dark-mode desktop application built with Python that allows users to easily load CSV files, select multiple variables, and generate beautiful, highly customizable, interactive graphs.

Whether you are plotting standard numeric data (like Voltage or Temperature) or analyzing categorical states (like "Charging" vs "Discharging"), this tool intelligently handles your data to produce publication-ready visualizations.

## ✨ Key Features

### 🖥️ Modern User Interface
* **Sleek UI:** Built using `customtkinter` for a beautiful, modern, dark-themed interface.
* **Scrollable Data Selection:** Easily select one X-axis and *unlimited* Y-axes using an intuitive checkbox list.
* **Pro Settings Tab:** Change Matplotlib themes (`seaborn`, `ggplot`, `dark_background`), plot types (Line, Scatter, Area, Step), line styles, markers, transparency, and log scales.

### 🧠 Smart Data Handling
* **Categorical State Shading:** If you plot a text/string column (e.g., Battery Mode: "Charging", "Rest"), the app automatically detects it and draws **transparent, colored background blocks** to highlight states without cluttering your line graphs.
* **X-Axis Optimization:** Automatically handles massive datasets by calculating and limiting the X-axis to exactly 10 visible labels, preventing text overlap and freezing.
* **Auto-Fallback Encodings:** Smartly falls back to `latin1` if it encounters special characters (like `°` or `€`) that would normally crash standard `utf-8` readers.

### 🖱️ Interactive Graphing
* **Smart Curve-Snapping:** Click anywhere on the graph, and the algorithm automatically calculates the closest data point, **snaps** a marker onto that specific curve, and displays a professional call-out box with the specific curve's name and exact Y-value.
* **Built-in Toolbar:** Zoom, pan, configure subplots, and save your generated plots directly to PNG, PDF, or SVG.

---

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/YourUsername/YourRepositoryName.git
cd YourRepositoryName
