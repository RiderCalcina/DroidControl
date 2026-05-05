import customtkinter as ctk
import tkinter as tk

class CTKTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        
        # Binds para widgets de customtkinter
        self.widget.bind("<Enter>", self.show_tooltip, add="+")
        self.widget.bind("<Leave>", self.hide_tooltip, add="+")

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
            
        # Posición
        x = self.widget.winfo_rootx() + (self.widget.winfo_width() // 2)
        y = self.widget.winfo_rooty() - 25
        
        # Crear ventana de tooltip
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{int(x)}+{int(y)}")
        self.tooltip_window.attributes("-topmost", True)
        self.tooltip_window.configure(bg="#1A1C1E")
        
        label = tk.Label(
            self.tooltip_window, text=self.text, bg="#1A1C1E", fg="#FFFFFF",
            font=("Inter", 8, "bold"), padx=6, pady=3,
            highlightthickness=1, highlightbackground="#3A3F44"
        )
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
