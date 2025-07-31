import customtkinter as ctk
import tkinter as tk

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Determine background color properly for the canvas
        appearance_mode = ctk.get_appearance_mode()
        fg_color = self.cget("fg_color")
        if isinstance(fg_color, (tuple, list)):
            if appearance_mode == "dark":
                bg_color = fg_color[1]
            else:
                bg_color = fg_color[0]
        else:
            bg_color = fg_color

        # Create the canvas with correct background color
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=bg_color)

        self.v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color=self.cget("fg_color"))

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Update scrollregion when the scrollable frame changes size
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Update canvas window width to the content's width (horizontal resizing)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width)
        )

        # Bind mouse wheel to vertical scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
