import tkinter as tk
import threading
import random
import time

color_shades = {
    "pink": ["#FFB6C1", "#FF69B4"],  # Light Pink, Hot Pink
    "blue": ["#ADD8E6", "#4682B4"],  # Light Blue, Steel Blue
    "green": ["#90EE90", "#228B22"],  # Light Green, Forest Green
    "purple": ["#D8BFD8", "#800080"],  # Thistle, Purple
    "yellow": ["#FFFACD", "#FFD700"],  # Lemon Chiffon, Gold
    "orange": ["#FFDAB9", "#FF8C00"],  # Peach Puff, Dark Orange
    "red": ["#FF9999", "#B22222"],  # Light Coral, Firebrick
    "teal": ["#AFEEEE", "#008080"],  # Pale Turquoise, Teal
    "brown": ["#D2B48C", "#8B4513"],  # Tan, Saddle Brown
}

# Default Theme
BG_COLOR = "#ADD8E6"
TEXT_COLOR = "black"
FONT = ("Sans serif", 13)

class PagingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Paging Algorithm Visualizer")
        self.root.configure(bg=BG_COLOR)

        # UI Elements
        tk.Label(root, text="Number of Pages:", fg=TEXT_COLOR, bg=BG_COLOR, font=FONT).grid(row=0, column=0)
        self.pages_entry = tk.Entry(root, font=FONT)
        self.pages_entry.grid(row=0, column=1)

        tk.Label(root, text="Number of Frames:", fg=TEXT_COLOR, bg=BG_COLOR, font=FONT).grid(row=1, column=0)
        self.frames_entry = tk.Entry(root, font=FONT)
        self.frames_entry.grid(row=1, column=1)

        tk.Label(root, text="Reference String (comma-separated):", fg=TEXT_COLOR, bg=BG_COLOR, font=FONT).grid(row=2, column=0)
        self.ref_entry = tk.Entry(root, font=FONT, width=30)
        self.ref_entry.grid(row=2, column=1)

        self.random_button = tk.Button(root, text="Randomize", font=FONT, command=self.generate_random)
        self.random_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.start_button = tk.Button(root, text="Run All", font=FONT, command=self.run_all)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Themes Button
        self.theme_button = tk.Button(root, text="Themes", font=FONT, command=self.open_theme_window)
        self.theme_button.grid(row=0, column=2, padx=10, pady=5, sticky="E")
       
        # Create separate frames for each algorithm
        self.algorithms = ["FIFO", "LRU", "Second Chance", "Optimal"]
        self.canvas_frames = {}
        self.page_fault_labels = {}

        for i, algo in enumerate(self.algorithms):
            tk.Label(root, text=algo, fg=TEXT_COLOR, bg=BG_COLOR, font=FONT).grid(row=5, column=i)
            self.canvas_frames[algo] = tk.Canvas(root, width=200, height=500, bg="#4682B4")
            self.canvas_frames[algo].grid(row=6, column=i, padx=10, pady=10)
            self.page_fault_labels[algo] = tk.Label(root, text=f"Page Faults: 0", fg=TEXT_COLOR, bg=BG_COLOR, font=FONT)
            self.page_fault_labels[algo].grid(row=7, column=i)

            # Replay button for each algorithm
            tk.Button(root, text=f"Replay {algo}", font=FONT, command=lambda a=algo: self.run_algorithm(a)).grid(row=8, column=i, pady=5)

        self.frames = {algo: [] for algo in self.algorithms}
        self.page_faults = {algo: 0 for algo in self.algorithms}

    def generate_random(self):
        num_pages = int(self.pages_entry.get()) if self.pages_entry.get().isdigit() else 10
        self.ref_entry.delete(0, tk.END)
        self.ref_entry.insert(0, ",".join(str(random.randint(0, 9)) for _ in range(num_pages)))

    def get_pages(self):
        return list(map(int, self.ref_entry.get().split(',')))

    def get_frames(self):
        return int(self.frames_entry.get()) if self.frames_entry.get().isdigit() else 3

    def draw_frames(self, algo, frame_list, fault=False):
        canvas = self.canvas_frames[algo]
        canvas.delete("all")
        for i, page in enumerate(frame_list):
            color = FAULT_COLOR if fault and i == len(frame_list) - 1 else FRAME_COLOR
            canvas.create_rectangle(50, 50 + i * 40, 150, 90 + i * 40, fill=color)
            canvas.create_text(100, 70 + i * 40, text=str(page), font=FONT, fill="black")

        self.root.update()
        if fault:
            time.sleep(0.5)
   
    def open_theme_window(self):
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Select Theme")
        theme_window.configure(bg="white")

        tk.Label(theme_window, text="Choose a Theme:", font=FONT, bg="white").pack(pady=5)

        for color_name, shades in color_shades.items():
            theme_button = tk.Button(theme_window, text=color_name.capitalize(), font=FONT, bg=shades[0],
                                     command=lambda cn=color_name: self.apply_theme(cn))
            theme_button.pack(fill="x", padx=10, pady=2)

    def apply_theme(self, color_name):
        global BG_COLOR  # Update global variable
        BG_COLOR = color_shades[color_name][0]  # Light color for BG

        self.root.configure(bg=BG_COLOR)

        # Update all text labels to match new theme
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=BG_COLOR)

        # Update canvas backgrounds
        for algo in self.algorithms:
            self.canvas_frames[algo].configure(bg=color_shades[color_name][1])  # Darker shade for canvas

    def fifo_algorithm(self, pages, num_frames):
        algo = "FIFO"
        self.page_faults[algo] = 0
        self.frames[algo] = []
       
        for page in pages:
            if page not in self.frames[algo]:  # Page fault occurs
                if len(self.frames[algo]) < num_frames:
                    self.frames[algo].append(page)
                else:
                    self.frames[algo].pop(0)  # Remove oldest page (FIFO)
                    self.frames[algo].append(page)
   
                self.page_faults[algo] += 1  # Count page fault
                self.draw_frames(algo, self.frames[algo], fault=True)
            else:
                self.draw_frames(algo, self.frames[algo])  # No fault, just visualize
   
            time.sleep(0.5)
   
        self.page_fault_labels[algo].config(text=f"Page Faults: {self.page_faults[algo]}")


    def lru_algorithm(self, pages, num_frames):
        algo = "LRU"
        self.page_faults[algo] = 0
        self.frames[algo] = []
        history = []  # Track page usage order
   
        for page in pages:
            if page not in self.frames[algo]:  # Page fault occurs
                if len(self.frames[algo]) < num_frames:
                    self.frames[algo].append(page)
                else:
                    # Safely find the least recently used page and replace it
                    lru_page = history.pop(0) if history else self.frames[algo][0]
                    if lru_page in self.frames[algo]:
                        self.frames[algo][self.frames[algo].index(lru_page)] = page
   
                self.page_faults[algo] += 1  # Count page fault
                self.draw_frames(algo, self.frames[algo], fault=True)
            else:
                self.draw_frames(algo, self.frames[algo])  # No fault, just visualize
   
            # Update history safely
            if page in history:
                history.remove(page)
            history.append(page)
   
            time.sleep(0.5)
   
        self.page_fault_labels[algo].config(text=f"Page Faults: {self.page_faults[algo]}")

    def second_chance_algorithm(self, pages, num_frames):
        algo = "Second Chance"
        self.page_faults[algo] = 0
        self.frames[algo] = []
        ref_bits = {}
        pointer = 0
        for page in pages:
            if page not in self.frames[algo]:
                if len(self.frames[algo]) < num_frames:
                    self.frames[algo].append(page)
                    ref_bits[page] = 1
                else:
                    while ref_bits[self.frames[algo][pointer]] == 1:
                        ref_bits[self.frames[algo][pointer]] = 0
                        pointer = (pointer + 1) % num_frames
                    ref_bits.pop(self.frames[algo][pointer])
                    self.frames[algo][pointer] = page
                    ref_bits[page] = 1
                    pointer = (pointer + 1) % num_frames
                self.page_faults[algo] += 1
                self.draw_frames(algo, self.frames[algo], fault=True)
            else:
                ref_bits[page] = 1
                self.draw_frames(algo, self.frames[algo])
            time.sleep(0.5)
        self.page_fault_labels[algo].config(text=f"Page Faults: {self.page_faults[algo]}")

    def optimal_algorithm(self, pages, num_frames):
        algo = "Optimal"
        self.page_faults[algo] = 0
        self.frames[algo] = []
        for i, page in enumerate(pages):
            if page not in self.frames[algo]:
                if len(self.frames[algo]) < num_frames:
                    self.frames[algo].append(page)
                else:
                    future_uses = {p: pages[i+1:].index(p) if p in pages[i+1:] else float('inf') for p in self.frames[algo]}
                    to_replace = max(future_uses, key=future_uses.get)
                    self.frames[algo][self.frames[algo].index(to_replace)] = page
                self.page_faults[algo] += 1
                self.draw_frames(algo, self.frames[algo], fault=True)
            else:
                self.draw_frames(algo, self.frames[algo])
            time.sleep(0.5)
        self.page_fault_labels[algo].config(text=f"Page Faults: {self.page_faults[algo]}")

    def run_algorithm(self, algo):
        threading.Thread(target=getattr(self, f"{algo.lower().replace(' ', '_')}_algorithm"), args=(self.get_pages(), self.get_frames())).start()

    def run_all(self):
        for algo in self.algorithms:
            self.run_algorithm(algo)

if __name__ == "__main__":
    root = tk.Tk()
    app = PagingGUI(root)
    root.mainloop()
