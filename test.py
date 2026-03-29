'''
import tkinter as tk
from tkinter import ttk, messagebox
import os

# File Constants
USERS_FILE = "users.txt"
ITEMS_FILE = "items.txt"

class CampusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Lost and Found System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f2f2f2")
        
        self.current_user = "Guest" # Default
        self.initialize_files()
        self.setup_ui()
        self.view_all_listings() # Load initial data

    def initialize_files(self):
        for f in [USERS_FILE, ITEMS_FILE]:
            if not os.path.exists(f):
                open(f, "w").close()

    def setup_ui(self):
        # =============================
        # SIDEBAR
        # =============================
        self.sidebar = tk.Frame(self.root, bg="#d32f2f", width=220)
        self.sidebar.pack(side="left", fill="y")

        logo = tk.Label(self.sidebar, text="BATANGAS\nSTATE\nUNIVERSITY",
                        bg="#d32f2f", fg="white",
                        font=("Arial", 14, "bold"), justify="center")
        logo.pack(pady=30)

        tk.Button(self.sidebar, text="CREATE A POST  +", bg="white", fg="#d32f2f",
                  font=("Arial", 11, "bold"), relief="flat", padx=10, pady=5,
                  command=self.open_post_window).pack(pady=20)

        # Navigation Labels as clickable buttons
        self.add_nav_btn("🔍  VIEW ALL LISTINGS", self.view_all_listings)
        self.add_nav_btn("📍  LOST ITEMS", lambda: self.view_all_listings("Lost"))
        self.add_nav_btn("📦  FOUND ITEMS", lambda: self.view_all_listings("Found"))
        self.add_nav_btn("👤  MY LISTINGS", lambda: self.view_all_listings(owner_filter=self.current_user))

        # =============================
        # MAIN AREA
        # =============================
        self.main_container = tk.Frame(self.root, bg="#f2f2f2")
        self.main_container.pack(side="left", fill="both", expand=True)

        self.title_label = tk.Label(self.main_container, text="LOST AND FOUND LISTINGS",
                                    font=("Arial", 24, "bold"), fg="#c62828", bg="#f2f2f2")
        self.title_label.pack(pady=20)

        # Search Bar
        search_frame = tk.Frame(self.main_container, bg="#f2f2f2")
        search_frame.pack(pady=10)
        self.search_entry = tk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.pack(side="left", ipady=5)
        tk.Button(search_frame, text="Search", command=self.search_items).pack(side="left", padx=5)

        # Scrollable Area for Cards
        self.canvas = tk.Canvas(self.main_container, bg="#f2f2f2", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f2f2f2")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=40)
        self.scrollbar.pack(side="right", fill="y")

        # =============================
        # RIGHT PANEL
        # =============================
        right_panel = tk.Frame(self.root, bg="#eeeeee", width=260)
        right_panel.pack(side="right", fill="y")

        self.user_display = tk.Label(right_panel, text=f"LOGGED IN AS:\n{self.current_user}",
                                     font=("Arial", 10, "bold"), bg="#eeeeee", pady=20)
        self.user_display.pack()

        tk.Button(right_panel, text="Login / Register", command=self.open_login_window).pack(pady=5)

    def add_nav_btn(self, text, command):
        btn = tk.Button(self.sidebar, text=text, bg="#d32f2f", fg="white", 
                        font=("Arial", 10), relief="flat", anchor="w", 
                        command=command, activebackground="#b71c1c")
        btn.pack(fill="x", padx=20, pady=5)

    # =============================
    # LOGIC FUNCTIONS
    # =============================
    def view_all_listings(self, status_filter=None, owner_filter=None):
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not os.path.exists(ITEMS_FILE): return

        with open(ITEMS_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) < 7: continue
                
                i_id, owner, name, desc, loc, date, status = data
                
                # Apply Filters
                if status_filter and status != status_filter: continue
                if owner_filter and owner != owner_filter: continue

                self.create_card(owner, i_id, name, desc, loc, date, status)

    def create_card(self, user, item_id, name, desc, location, date, status):
        card_color = "#ffffff" if status == "Lost" else "#e8f5e9"
        card = tk.Frame(self.scrollable_frame, bg=card_color, highlightbackground="#cccccc", highlightthickness=1)
        card.pack(fill="x", pady=10, padx=10)

        header = tk.Label(card, text=f"{name.upper()} ({status})", font=("Arial", 12, "bold"), bg=card_color)
        header.pack(anchor="w", padx=10, pady=5)

        details = f"ID: {item_id} | Posted by: {user}\nLocation: {location} | Date: {date}\nDescription: {desc}"
        tk.Label(card, text=details, justify="left", bg=card_color, font=("Arial", 10)).pack(anchor="w", padx=10, pady=5)

    def search_items(self):
        query = self.search_entry.get().lower()
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        with open(ITEMS_FILE, "r") as file:
            for line in file:
                if query in line.lower():
                    data = line.strip().split(",")
                    self.create_card(*data[1:], user=data[1], item_id=data[0]) # Adjusted slice mapping

    def open_post_window(self):
        if self.current_user == "Guest":
            messagebox.showwarning("Login Required", "Please login to post an item.")
            return
            
        win = tk.Toplevel(self.root)
        win.title("Create Post")
        win.geometry("300x400")

        tk.Label(win, text="Item Name:").pack()
        name_ent = tk.Entry(win)
        name_ent.pack()

        tk.Label(win, text="Description:").pack()
        desc_ent = tk.Entry(win)
        desc_ent.pack()

        tk.Label(win, text="Location:").pack()
        loc_ent = tk.Entry(win)
        loc_ent.pack()

        tk.Label(win, text="Status:").pack()
        status_var = tk.StringVar(value="Lost")
        ttk.Combobox(win, textvariable=status_var, values=["Lost", "Found"]).pack()

        def save():
            i_id = str(sum(1 for _ in open(ITEMS_FILE)) + 1)
            with open(ITEMS_FILE, "a") as f:
                f.write(f"{i_id},{self.current_user},{name_ent.get()},{desc_ent.get()},{loc_ent.get()},2026-03-05,{status_var.get()}\n")
            messagebox.showinfo("Success", "Post Created!")
            win.destroy()
            self.view_all_listings()

        tk.Button(win, text="Submit", command=save).pack(pady=20)

    def open_login_window(self):
        win = tk.Toplevel(self.root)
        win.title("Login")
        win.geometry("250x200")

        tk.Label(win, text="Username:").pack()
        u_ent = tk.Entry(win)
        u_ent.pack()
        tk.Label(win, text="Password:").pack()
        p_ent = tk.Entry(win, show="*")
        p_ent.pack()

        def login():
            with open(USERS_FILE, "r") as f:
                for line in f:
                    u, p = line.strip().split(",")
                    if u == u_ent.get() and p == p_ent.get():
                        self.current_user = u
                        self.user_display.config(text=f"LOGGED IN AS:\n{self.current_user}")
                        messagebox.showinfo("Success", f"Welcome {u}!")
                        win.destroy()
                        return
            messagebox.showerror("Error", "Invalid Credentials")

        tk.Button(win, text="Login", command=login).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusApp(root)
    root.mainloop()
    '''