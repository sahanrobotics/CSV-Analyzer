# Modern CSV Data Plotter Pro
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
                              

## Technical Overview
Modern CSV Data Plotter Pro is an advanced desktop application engineered for high-performance visualization of complex datasets. Developed using Python, the application leverages the CustomTkinter framework for a hardware-accelerated, modern user interface and Matplotlib for publication-quality graphical rendering. The tool is specifically designed to handle multivariate time-series data, categorical state analysis, and large-scale CSV processing with efficiency and precision.

---

## Core Features

### Advanced Graphical Interface
*   **Dynamic UI Scaling:** Utilizing CustomTkinter to ensure high-DPI support and consistent rendering across Windows, macOS, and Linux.
*   **Multivariate Variable Selection:** A scrollable selection architecture that allows users to manage datasets with hundreds of columns without UI degradation.
*   **Asynchronous Plotting:** Decoupled data processing and rendering logic to maintain UI responsiveness during complex calculations.

### Data Engineering and Handling
*   **Encoding Resilience:** Automated fallback mechanism transitioning from UTF-8 to Latin-1 to ensure data integrity when encountering non-standard characters.
*   **Categorical State Detection:** Proprietary logic to identify non-numeric variables and visualize them as shaded background regions (state-space representation).
*   **Optimized Memory Management:** Efficient utilization of Pandas DataFrames for rapid indexing and slicing of large datasets.

### Visualization Specifications
*   **Multi-Type Rendering:** Native support for Line, Scatter, Area, and Step plots.
*   **Statistical Themes:** Integration of Seaborn, ggplot, and Dark Background stylesheets for varied analytical contexts.
*   **Interactive Toolset:** Real-time zoom, pan, and subplot configuration provided through the integrated Matplotlib Navigation Toolbar.
*   **Export Capabilities:** Support for high-resolution vector (SVG, PDF) and raster (PNG) formats.

---

## Technical Architecture

### Software Stack
*   **Programming Language:** Python 3.8+
*   **GUI Framework:** CustomTkinter
*   **Data Manipulation:** Pandas, NumPy
*   **Visualization Engine:** Matplotlib
*   **Packaging:** Standardized project structure for modularity and scalability.

### Directory Structure
```text
modern-csv-plotter/
├── main.py                 # Application entry point and controller
├── requirements.txt        # Dependency management
├── LICENSE                 # MIT License documentation
├── README.md               # Technical documentation
├── src/
│   ├── ui/                 # Custom UI components and styling
│   ├── plotting/           # Graph rendering logic and backends
│   ├── data_processing/    # CSV parsing and encoding management
│   └── utils/              # Mathematical helpers and file IO
└── screenshots/            # Documentation assets
```

---

## Installation Procedures

### Prerequisites
Ensure Python 3.8 or higher is installed on the host system.

### Deployment Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Username/Modern-CSV-Plotter-Pro.git
   cd Modern-CSV-Plotter-Pro
   ```

2. Initialize a virtual environment:
   ```bash
   python -m venv venv
   # Activation for Windows:
   venv\Scripts\activate
   # Activation for Unix/macOS:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Operational Workflow

1.  **Data Ingestion:** Use the "Load CSV File" interface to import local datasets.
2.  **Axis Configuration:** Select the primary independent variable (X-Axis) from the drop-down menu.
3.  **Variable Correlation:** Check multiple dependent variables (Y-Axes) in the right-side panel for overlay comparison.
4.  **Styling Configuration:** Adjust plot type, logarithmic scaling, and color themes via the sidebar settings.
5.  **Interactive Analysis:** Utilize the mouse wheel for zooming and the toolbar for precise data windowing.
6.  **Data Export:** Save the finalized visualization using the disk icon in the navigation toolbar.

---

## Roadmap and Future Developments
*   **GPU Acceleration:** Implementation of OpenGL backends for rendering datasets exceeding 10 million rows.
*   **Real-Time Data Streaming:** Support for live socket-based data ingestion and dynamic plot updating.
*   **Advanced Analytics:** Integration of Scipy for on-the-fly FFT (Fast Fourier Transform) and curve fitting.
*   **Configuration Serialization:** Exporting and importing UI states and plot configurations via JSON.

---

## Contribution Guidelines
Contributions to this project are managed via Pull Requests. Ensure that any code contributions adhere to PEP 8 standards and include updated documentation for new features. 

1. Fork the repository.
2. Create a feature branch (git checkout -b feature/Optimization).
3. Commit changes (git commit -m 'Optimization of data parsing').
4. Push to the branch (git push origin feature/Optimization).
5. Open a Pull Request for review.

---

## License
This project is licensed under the MIT License. This allows for both personal and commercial use with minimal restrictions. See the LICENSE file for full legal text.