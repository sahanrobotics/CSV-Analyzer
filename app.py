import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import MaxNLocator, FuncFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Set modern theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ModernCSVPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Data Plotter Pro - Smart Interactive Mode")
        self.root.geometry("1300x800")

        self.df = None
        self.y_vars = []

        # Tracking variables for interactive marking
        self.annotations = []
        self.is_x_string = False
        self.X_labels = None

        # Memory variables for Snapping Logic
        self.plot_data = None
        self.X_plot = None
        self.numeric_y_cols = []

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # --- Left Panel ---
        self.left_panel = ctk.CTkFrame(self.root, width=350, corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.grid_rowconfigure(1, weight=1)

        self.logo_label = ctk.CTkLabel(self.left_panel, text="Data Plotter Pro",
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tabs
        self.tabview = ctk.CTkTabview(self.left_panel, width=300)
        self.tabview.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.tab_data = self.tabview.add("Data")
        self.tab_settings = self.tabview.add("Settings")

        self.setup_data_tab()
        self.setup_settings_tab()

        self.btn_plot = ctk.CTkButton(self.left_panel, text="Generate Plot", height=40, font=ctk.CTkFont(weight="bold"),
                                      command=self.generate_plot)
        self.btn_plot.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")

        # --- INTERACTIVE TOOLS SECTION ---
        self.tools_frame = ctk.CTkFrame(self.left_panel, corner_radius=10)
        self.tools_frame.grid(row=3, column=0, padx=20, pady=(5, 20), sticky="ew")

        ctk.CTkLabel(self.tools_frame, text="Interactive Tools", font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))

        self.switch_mark = ctk.CTkSwitch(self.tools_frame, text="Mark Points (Click on Graph)")
        self.switch_mark.pack(pady=5, padx=10, anchor="w")

        self.btn_clear_marks = ctk.CTkButton(self.tools_frame, text="Clear Marks", fg_color="#E74C3C",
                                             hover_color="#C0392B", command=self.clear_markers)
        self.btn_clear_marks.pack(pady=(5, 10), padx=10, fill="x")

        # --- Right Panel ---
        self.plot_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.plot_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.create_plot_canvas()

    def setup_data_tab(self):
        self.btn_load = ctk.CTkButton(self.tab_data, text="Load CSV File", fg_color="transparent", border_width=2,
                                      text_color=("gray10", "#DCE4EE"), command=self.load_csv)
        self.btn_load.pack(fill="x", pady=(10, 5), padx=10)

        self.lbl_file = ctk.CTkLabel(self.tab_data, text="No file selected", text_color="gray",
                                     font=ctk.CTkFont(size=12))
        self.lbl_file.pack(fill="x", pady=(0, 20), padx=10)

        ctk.CTkLabel(self.tab_data, text="X-Axis Column:", anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x",
                                                                                                             padx=10)
        self.combo_x = ctk.CTkOptionMenu(self.tab_data, values=["Select File First"])
        self.combo_x.pack(fill="x", pady=(5, 20), padx=10)

        ctk.CTkLabel(self.tab_data, text="Y-Axis Column(s):", anchor="w", font=ctk.CTkFont(weight="bold")).pack(
            fill="x", padx=10)

        self.scroll_y = ctk.CTkScrollableFrame(self.tab_data, height=200)
        self.scroll_y.pack(fill="both", expand=True, padx=10, pady=5)

        ctk.CTkLabel(self.scroll_y, text="Load data to see options", text_color="gray").pack(pady=20)

    def setup_settings_tab(self):
        settings_scroll = ctk.CTkScrollableFrame(self.tab_settings)
        settings_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.ls_map = {"Solid": "-", "Dashed": "--", "Dash-Dot": "-.", "Dotted": ":", "None": ""}
        self.mk_map = {"None": "", "Circle": "o", "Square": "s", "Triangle": "^", "Cross": "x"}

        ctk.CTkLabel(settings_scroll, text="Theme:", anchor="w").pack(fill="x", pady=(5, 0))
        self.combo_theme = ctk.CTkOptionMenu(settings_scroll,
                                             values=["default", "seaborn", "ggplot", "dark_background"])
        self.combo_theme.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(settings_scroll, text="Numeric Plot Type:", anchor="w").pack(fill="x")
        self.combo_type = ctk.CTkOptionMenu(settings_scroll, values=["Line", "Scatter", "Step", "Area"])
        self.combo_type.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(settings_scroll, text="Line Style:", anchor="w").pack(fill="x")
        self.combo_ls = ctk.CTkOptionMenu(settings_scroll, values=list(self.ls_map.keys()))
        self.combo_ls.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(settings_scroll, text="Marker:", anchor="w").pack(fill="x")
        self.combo_mk = ctk.CTkOptionMenu(settings_scroll, values=list(self.mk_map.keys()))
        self.combo_mk.pack(fill="x", pady=(0, 10))

        self.switch_log_x = ctk.CTkSwitch(settings_scroll, text="Log Scale (X-Axis)")
        self.switch_log_x.pack(anchor="w", pady=5)

        self.switch_log_y = ctk.CTkSwitch(settings_scroll, text="Log Scale (Y-Axis)")
        self.switch_log_y.pack(anchor="w", pady=5)

        self.switch_grid = ctk.CTkSwitch(settings_scroll, text="Show Grid")
        self.switch_grid.select()
        self.switch_grid.pack(anchor="w", pady=5)

        ctk.CTkLabel(settings_scroll, text="Custom Title:", anchor="w").pack(fill="x", pady=(15, 0))
        self.ent_title = ctk.CTkEntry(settings_scroll, placeholder_text="Leave blank for auto")
        self.ent_title.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(settings_scroll, text="Custom X Label:", anchor="w").pack(fill="x")
        self.ent_x = ctk.CTkEntry(settings_scroll, placeholder_text="Leave blank for auto")
        self.ent_x.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(settings_scroll, text="Custom Y Label:", anchor="w").pack(fill="x")
        self.ent_y = ctk.CTkEntry(settings_scroll, placeholder_text="Leave blank for auto")
        self.ent_y.pack(fill="x", pady=(0, 10))

    def create_plot_canvas(self):
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.figure.subplots_adjust(bottom=0.2, left=0.1, right=0.95)
        self.ax1 = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Bind Mouse Click Event for marking points
        self.canvas.mpl_connect('button_press_event', self.on_click)

    def load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath: return

        try:
            try:
                self.df = pd.read_csv(filepath, encoding='utf-8')
            except UnicodeDecodeError:
                self.df = pd.read_csv(filepath, encoding='latin1')

            columns = list(self.df.columns)

            filename = filepath.split("/")[-1]
            if len(filename) > 30: filename = filename[:27] + "..."
            self.lbl_file.configure(text=filename, text_color="white")

            self.combo_x.configure(values=columns)
            if columns: self.combo_x.set(columns[0])

            for widget in self.scroll_y.winfo_children():
                widget.destroy()
            self.y_vars.clear()

            for col in columns:
                var = ctk.StringVar(value="")
                cb = ctk.CTkCheckBox(self.scroll_y, text=col, variable=var, onvalue=col, offvalue="")
                cb.pack(pady=5, padx=5, anchor="w")
                self.y_vars.append(var)

            self.ax1.clear()
            self.canvas.draw()
            self.tabview.set("Data")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV:\n{str(e)}")

    def generate_plot(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please load a CSV file first.")
            return

        x_col = self.combo_x.get()
        y_cols = [var.get() for var in self.y_vars if var.get() != ""]

        if not x_col or not y_cols:
            messagebox.showwarning("Warning", "Please select an X column and at least one Y column.")
            return

        try:
            plt.style.use(self.combo_theme.get())
            self.figure.clear()
            self.ax1 = self.figure.add_subplot(111)
            self.annotations.clear()

            plot_type = self.combo_type.get()
            ls = self.ls_map[self.combo_ls.get()]
            mk = self.mk_map[self.combo_mk.get()]

            # Save to class memory for clicking logic
            self.plot_data = self.df[[x_col] + y_cols].dropna().reset_index(drop=True)
            self.X_labels = self.plot_data[x_col]
            self.numeric_y_cols = []

            self.is_x_string = pd.api.types.is_string_dtype(self.X_labels) or pd.api.types.is_object_dtype(
                self.X_labels)
            if self.is_x_string:
                self.X_plot = np.arange(len(self.X_labels))
            else:
                self.X_plot = self.X_labels.values

            legend_handles, legend_labels = [], []
            cmap = plt.get_cmap("tab10")
            color_index = 0

            for y_col in y_cols:
                Y = self.plot_data[y_col]
                is_y_numeric = pd.api.types.is_numeric_dtype(Y)

                if is_y_numeric:
                    self.numeric_y_cols.append(y_col)  # Remember this curve for snapping

                    line = None
                    if plot_type == "Line":
                        line = self.ax1.plot(self.X_plot, Y, linestyle=ls, marker=mk, linewidth=2)[0]
                    elif plot_type == "Scatter":
                        line = self.ax1.scatter(self.X_plot, Y, marker=mk if mk else "o")
                    elif plot_type == "Step":
                        line = self.ax1.step(self.X_plot, Y, linestyle=ls, marker=mk, linewidth=2)[0]
                    elif plot_type == "Area":
                        self.ax1.fill_between(self.X_plot, Y, alpha=0.3)
                        line = self.ax1.plot(self.X_plot, Y, linestyle=ls, marker=mk, linewidth=1.5, alpha=1.0)[0]

                    if line:
                        legend_handles.append(line)
                        legend_labels.append(y_col)
                else:
                    # Categorical / Background highlighting
                    unique_states = Y.unique()
                    state_colors = {}
                    for state in unique_states:
                        state_colors[state] = cmap(color_index % 10)
                        color_index += 1

                    Y_list = Y.tolist()
                    start_x = self.X_plot[0]
                    current_state = Y_list[0]

                    for i in range(1, len(Y_list)):
                        if Y_list[i] != current_state:
                            end_x = self.X_plot[i]
                            self.ax1.axvspan(start_x, end_x, color=state_colors[current_state], alpha=0.25, lw=0)
                            start_x = end_x
                            current_state = Y_list[i]

                    self.ax1.axvspan(start_x, self.X_plot[-1], color=state_colors[current_state], alpha=0.25, lw=0)

                    for state, color in state_colors.items():
                        patch = mpatches.Patch(color=color, alpha=0.4)
                        legend_handles.append(patch)
                        legend_labels.append(f"{y_col}: {state}")

            self.ax1.xaxis.set_major_locator(MaxNLocator(nbins=10))
            if self.is_x_string:
                def format_fn(tick_val, tick_pos):
                    idx = int(tick_val)
                    if 0 <= idx < len(self.X_labels):
                        return str(self.X_labels.iloc[idx])
                    return ""

                self.ax1.xaxis.set_major_formatter(FuncFormatter(format_fn))

            if self.switch_log_x.get() and not self.is_x_string: self.ax1.set_xscale('log')
            if self.switch_log_y.get(): self.ax1.set_yscale('log')

            if self.switch_grid.get():
                self.ax1.grid(True, linestyle='--', alpha=0.6)
            else:
                self.ax1.grid(False)

            self.ax1.legend(legend_handles, legend_labels, loc='upper right', bbox_to_anchor=(1, 1), framealpha=0.8)

            c_title = self.ent_title.get().strip()
            c_x = self.ent_x.get().strip()
            c_y = self.ent_y.get().strip()

            self.ax1.set_title(c_title if c_title else "Data Plot", fontweight='bold', pad=15)
            self.ax1.set_xlabel(c_x if c_x else x_col, fontweight='bold')
            self.ax1.set_ylabel(c_y if c_y else "Values", fontweight='bold')

            self.figure.autofmt_xdate(rotation=45)
            self.figure.tight_layout(pad=2.0)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Plot Error", f"Plot generation failed.\n\nDetails: {str(e)}")

    # --- SMART SNAPPING ON_CLICK ---
    def on_click(self, event):
        # Ensure marking mode is ON, and click is within the plot area
        if not self.switch_mark.get() or event.inaxes is not self.ax1:
            return

        # Ensure zooming/panning is not active
        if self.toolbar.mode != '':
            return

        # Ensure we have data loaded
        if self.plot_data is None or len(self.numeric_y_cols) == 0:
            return

        click_x = event.xdata
        click_y = event.ydata

        # 1. Find the absolute closest X data point to where they clicked
        idx = (np.abs(self.X_plot - click_x)).argmin()
        actual_x = self.X_plot[idx]

        # 2. Find the closest Y curve at that specific X point
        min_dist = float('inf')
        best_col = None
        best_y = None

        for col in self.numeric_y_cols:
            actual_y = self.plot_data[col].iloc[idx]
            dist = abs(actual_y - click_y)  # Vertical distance

            if dist < min_dist:
                min_dist = dist
                best_col = col
                best_y = actual_y

        # If we failed to find a valid point, exit
        if best_col is None:
            return

        # 3. Format the display string (Specific Name: Specific Value)
        display_text = f"{best_col}: {best_y:.2f}"

        # 4. SNAP! Draw the point at the exact (actual_x, actual_y) of the closest curve
        point, = self.ax1.plot(actual_x, best_y, 'ro', markersize=6, zorder=5)

        # Draw a professional call-out box pointing to the snapped location
        anno = self.ax1.annotate(
            display_text,
            xy=(actual_x, best_y),
            xytext=(15, 15),  # Offset text slightly up and to the right
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color="red"),
            bbox=dict(boxstyle="round,pad=0.4", fc="#FFF9C4", ec="red", lw=1.5, alpha=0.9),  # Yellow box
            color="black",
            fontweight="bold",
            zorder=5
        )

        # Save to memory so we can clear them later
        self.annotations.append((point, anno))
        self.canvas.draw()

    def clear_markers(self):
        # Remove all stored markers and annotations from the plot
        for point, anno in self.annotations:
            try:
                point.remove()
                anno.remove()
            except:
                pass
        self.annotations.clear()
        self.canvas.draw()


if __name__ == "__main__":
    app = ctk.CTk()
    gui = ModernCSVPlotterApp(app)
    app.mainloop()