import tkinter as tk
from tkinter import messagebox, ttk
import math

# -------------------------------
# Represents an item location in the warehouse
# -------------------------------
class Location:
    def _init(self, name, x, y):  # <-- FIXED: __init_
        self.name = name
        self.x = x
        self.y = y

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def _str(self):  # <-- FIXED: __str_
        return f"{self.name} ({self.x}, {self.y})"


# -------------------------------
# Handles route optimization logic
# -------------------------------
class RouteOptimizer:
    @staticmethod
    def find_shortest_route(locations):
        if not locations:
            return []

        route = [locations[0]]
        visited = {locations[0]}
        current = locations[0]

        while len(route) < len(locations):
            nearest = min(
                (loc for loc in locations if loc not in visited),
                key=lambda loc: current.distance_to(loc),
            )
            route.append(nearest)
            visited.add(nearest)
            current = nearest

        return route

    @staticmethod
    def calculate_total_distance(route):
        return sum(route[i].distance_to(route[i + 1]) for i in range(len(route) - 1))


# -------------------------------
# Main GUI Application
# -------------------------------
class WarehousePickerApp:
    def _init(self, root):  # <-- FIXED: __init_
        self.root = root
        self.root.title("🏭 Warehouse Picker Route Optimizer")
        self.root.geometry("700x600")
        self.root.config(bg="#2C2F33")

        # Warehouse items and coordinates
        self.warehouse_map = {
            "Item A": Location("Item A", 2, 3),
            "Item B": Location("Item B", 5, 5),
            "Item C": Location("Item C", 1, 6),
            "Item D": Location("Item D", 7, 1),
            "Item E": Location("Item E", 4, 2),
        }

        self.selected_items = []
        self.setup_gui()

    # -------------------------------
    # GUI Layout Setup
    # -------------------------------
    def setup_gui(self):
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        style.configure("TLabel", background="#2C2F33", foreground="white", font=("Arial", 10, "bold"))

        # Title
        tk.Label(
            self.root,
            text="Warehouse Picker Route Optimizer",
            font=("Helvetica", 18, "bold"),
            bg="#23272A",
            fg="white",
            pady=10
        ).pack(fill="x")

        # Frame for available items
        frame_items = tk.LabelFrame(
            self.root, text="Available Items and Coordinates", bg="#2C2F33", fg="white", font=("Arial", 12, "bold")
        )
        frame_items.pack(padx=10, pady=10, fill="both")

        self.item_list_text = tk.Text(frame_items, height=6, width=60, bg="#23272A", fg="white", font=("Consolas", 10))
        self.item_list_text.pack(padx=10, pady=10)
        self.item_list_text.insert(tk.END, "\n".join(str(loc) for loc in self.warehouse_map.values()))
        self.item_list_text.config(state=tk.DISABLED)

        # Frame for input
        frame_input = tk.LabelFrame(
            self.root, text="Add Items to Pick List", bg="#2C2F33", fg="white", font=("Arial", 12, "bold")
        )
        frame_input.pack(padx=10, pady=10, fill="x")

        tk.Label(frame_input, text="Enter item name (e.g., Item A):", bg="#2C2F33", fg="white").pack(pady=5)
        self.item_name_entry = ttk.Entry(frame_input, width=30)
        self.item_name_entry.pack(pady=5)

        ttk.Button(frame_input, text="➕ Add to Pick List", command=self.add_item).pack(pady=5)

        # Frame for output
        frame_output = tk.LabelFrame(
            self.root, text="Output", bg="#2C2F33", fg="white", font=("Arial", 12, "bold")
        )
        frame_output.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_text = tk.Text(frame_output, height=15, width=80, bg="#23272A", fg="#00FF9F", font=("Consolas", 10))
        self.output_text.pack(padx=10, pady=10)

        ttk.Button(self.root, text="🚀 Calculate Route", command=self.calculate_route).pack(pady=10)

    # -------------------------------
    # Add Item to Pick List
    # -------------------------------
    def add_item(self):
        name = self.item_name_entry.get().strip()
        location = self.warehouse_map.get(name)

        if location:
            if location not in self.selected_items:
                self.selected_items.append(location)
                self.output_text.insert(tk.END, f"✅ Added: {location}\n")
            else:
                messagebox.showinfo("Info", "Item already added!")
            self.item_name_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Item not found!")

    # -------------------------------
    # Calculate and Display Route
    # -------------------------------
    def calculate_route(self):
        if len(self.selected_items) < 2:
            messagebox.showwarning("Warning", "Add at least two items before calculating route.")
            return

        self.output_text.insert(tk.END, "\n🚚 Calculating optimized route...\n")

        route = RouteOptimizer.find_shortest_route(self.selected_items)
        total_distance = RouteOptimizer.calculate_total_distance(route)

        self.output_text.insert(tk.END, "📦 Optimized Route:\n")
        for i, loc in enumerate(route, start=1):
            self.output_text.insert(tk.END, f"{i}. {loc}\n")

        self.output_text.insert(tk.END, f"📏 Total Distance: {total_distance:.2f} units\n")
        self.output_text.insert(tk.END, "-------------------------------------------\n\n")

        self.selected_items.clear()


# -------------------------------
# Entry Point
# -------------------------------
if _name_ == "_main":  # <-- FIXED: __name, __main_
    root = tk.Tk()
    app = WarehousePickerApp(root)
    root.mainloop()