import customtkinter as ctk
from tkinter import messagebox
import hashlib
import json
import uuid
from datetime import datetime
from PIL import Image
import os

# --- SET THEME ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue") 

COLOR_BSU_RED = "#D32F2F"
COLOR_WHITE = "#FFFFFF"

class LostAndFoundApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Batangas State University - Lost and Found")
        self.geometry("1200x800")
        self.configure(fg_color=COLOR_WHITE)

        self.current_user = None
        self.listings = self.load_listings()

        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_login()

    # --- DATA LOGIC (Integrated from your auth.py and listings.py) ---
    def load_listings(self):
        try:
            if os.path.exists("listings.json"):
                with open("listings.json", "r") as f:
                    content = f.read().strip()
                    return json.loads(content) if content else []
            return []
        except: return []

    def save_listings(self):
        with open("listings.json", "w") as f:
            json.dump(self.listings, f, indent=4)

    def check_auth(self, username, password):
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if not os.path.exists('users.txt'): return False
        with open('users.txt', 'r') as f:
            for line in f:
                fields = line.strip().split(',')
                if len(fields) >= 3:
                    if fields[0] == username.lower() and fields[2] == hashed_input:
                        return True
        return False

    # --- NAVIGATION & SCREENS ---
    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="LOST & FOUND SYSTEM", font=("Arial", 24, "bold"), text_color=COLOR_BSU_RED).pack(pady=20)
        u_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=300)
        u_entry.pack(pady=10)
        p_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300)
        p_entry.pack(pady=10)

        def login_cmd():
            if self.check_auth(u_entry.get(), p_entry.get()):
                self.current_user = u_entry.get().lower()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Username or Password")

        ctk.CTkButton(frame, text="Login", fg_color=COLOR_BSU_RED, command=login_cmd).pack(pady=10)
        ctk.CTkButton(frame, text="Register New Account", fg_color="gray", command=self.show_register).pack()

    def show_register(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="CREATE ACCOUNT", font=("Arial", 24, "bold"), text_color=COLOR_BSU_RED).pack(pady=20)
        u_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=300)
        u_entry.pack(pady=5)
        e_entry = ctk.CTkEntry(frame, placeholder_text="GSuite Email", width=300)
        e_entry.pack(pady=5)
        p_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300)
        p_entry.pack(pady=5)

        def reg_cmd():
            u, e, p = u_entry.get().lower(), e_entry.get(), p_entry.get()
            if u and e and p:
                hashed = hashlib.sha256(p.encode()).hexdigest()
                with open('users.txt', 'a') as f:
                    f.write(f"{u},{e},{hashed}\n")
                messagebox.showinfo("Success", "Registration Successful!")
                self.show_login()
            else:
                messagebox.showwarning("Warning", "Fields cannot be empty")

        ctk.CTkButton(frame, text="Register", fg_color=COLOR_BSU_RED, command=reg_cmd).pack(pady=10)
        ctk.CTkButton(frame, text="Back to Login", fg_color="gray", command=self.show_login).pack()

    def show_dashboard(self):
        self.clear_screen()
        
        # 1. SIDEBAR
        self.sidebar = ctk.CTkFrame(self, fg_color=COLOR_BSU_RED, corner_radius=0, width=280)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        try:
            logo_img = ctk.CTkImage(light_image=Image.open("logo.png"), size=(130, 120))
            ctk.CTkLabel(self.sidebar, image=logo_img, text="").pack(pady=30)
        except:
            ctk.CTkLabel(self.sidebar, text="BSU LOGO", text_color="white", font=("Arial", 20, "bold")).pack(pady=30)

        # Sidebar Buttons
        btn_opts = {"fg_color": "transparent", "text_color": "white", "anchor": "w", "font": ("Arial", 14, "bold"), "height": 50}
        
        ctk.CTkButton(self.sidebar, text="⊕ CREATE A POST", fg_color="white", text_color=COLOR_BSU_RED, corner_radius=25, font=("Arial", 14, "bold"), command=self.open_create_post).pack(padx=20, pady=20, fill="x")
        ctk.CTkButton(self.sidebar, text="🔍  VIEW ALL LISTINGS", command=lambda: self.render_listings("all"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="🔍  LOST ITEM LISTINGS", command=lambda: self.render_listings("Lost"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="🔍  FOUND ITEM LISTINGS", command=lambda: self.render_listings("Found"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(self.sidebar, text="📑  MY LISTINGS", command=lambda: self.render_listings("mine"), **btn_opts).pack(fill="x", padx=10)

        # 2. MAIN AREA
        self.main_container = ctk.CTkFrame(self, fg_color="#F9F9F9", corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew")

        # Header
        header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 10))
        ctk.CTkLabel(header, text="LOST AND FOUND LISTING SYSTEM", font=("Arial", 28, "bold"), text_color=COLOR_BSU_RED).pack(side="left")
        
        # User Display
        user_display = ctk.CTkFrame(header, fg_color="transparent")
        user_display.pack(side="right")
        ctk.CTkLabel(user_display, text=f"{self.current_user.upper()}\nStudent", font=("Arial", 10), justify="right").pack(side="left", padx=10)
        ctk.CTkLabel(user_display, text="👤", font=("Arial", 30), text_color=COLOR_BSU_RED).pack(side="right")

        # Search Bar
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_listings("all"))
        self.search_bar = ctk.CTkEntry(self.main_container, textvariable=self.search_var, placeholder_text="🔍 search by item name", height=45, corner_radius=25, fg_color="#EEEEEE", border_width=0)
        self.search_bar.pack(fill="x", padx=40, pady=10)
 
        # Scroll Feed
        self.scroll_feed = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.scroll_feed.pack(fill="both", expand=True, padx=40, pady=10)

        # 3. RIGHT PANEL
        self.guide_panel = ctk.CTkFrame(self, fg_color=COLOR_WHITE, width=220, corner_radius=0)
        self.guide_panel.grid(row=0, column=2, sticky="nsew")
        ctk.CTkLabel(self.guide_panel, text="LISTING GUIDELINES", font=("Arial", 12, "bold"), text_color=COLOR_BSU_RED).pack(pady=(40, 10))
        
        guide_text = "• Be specific\n• Identify colors\n• State location\n• Mention markings\n• Withhold secret detail\n• Professional language"
        ctk.CTkLabel(self.guide_panel, text=guide_text, justify="left", font=("Arial", 11)).pack(padx=20)

        self.render_listings("all")

    def render_listings(self, filter_type):
        for widget in self.scroll_feed.winfo_children():
            widget.destroy()

        query = self.search_var.get().lower()

        for item in self.listings:
            # Filters
            if filter_type == "Lost" and item['status'] != "Lost": continue
            if filter_type == "Found" and item['status'] != "Found": continue
            if filter_type == "mine" and item['user'] != self.current_user: continue
            if query and query not in item['name'].lower(): continue

            card = ctk.CTkFrame(self.scroll_feed, fg_color=COLOR_WHITE, corner_radius=10, border_width=1, border_color="#DDDDDD")
            card.pack(fill="x", pady=10, padx=5)

            title_f = ctk.CTkFrame(card, fg_color="transparent")
            title_f.pack(fill="x", padx=15, pady=10)
            ctk.CTkLabel(title_f, text="👤", font=("Arial", 25), text_color=COLOR_BSU_RED).pack(side="left")
            ctk.CTkLabel(title_f, text=f"{item['user'].upper()}\n{item['date']}", font=("Arial", 11, "bold"), justify="left").pack(side="left", padx=10)

            details = (f"Item ID: {item['id']}\nItem name: {item['name']}\nDescription: {item['description']}\n"
                       f"Location: {item['location']}\nContact: {item['contact']}\nStatus = {item['status']}")
            ctk.CTkLabel(card, text=details, font=("Arial", 12), justify="left").pack(padx=55, pady=(0, 15), anchor="w")

    def open_create_post(self):
        win = ctk.CTkToplevel(self)
        win.title("Create New Post")
        win.geometry("400x600")
        win.attributes('-topmost', True) # Keep window in front

        ctk.CTkLabel(win, text="POST AN ITEM", font=("Arial", 18, "bold"), text_color=COLOR_BSU_RED).pack(pady=20)
        
        name_e = ctk.CTkEntry(win, placeholder_text="Item Name", width=300); name_e.pack(pady=5)
        status_c = ctk.CTkComboBox(win, values=["Lost", "Found"], width=300); status_c.pack(pady=5)
        desc_e = ctk.CTkEntry(win, placeholder_text="Description", width=300); desc_e.pack(pady=5)
        loc_e = ctk.CTkEntry(win, placeholder_text="Location", width=300); loc_e.pack(pady=5)
        cont_e = ctk.CTkEntry(win, placeholder_text="Contact Details", width=300); cont_e.pack(pady=5)

        def submit():
            if not name_e.get(): return
            new_item = {
                "user": self.current_user,
                "status": status_c.get(),
                "id": str(uuid.uuid4().hex[:6].upper()),
                "name": name_e.get(),
                "description": desc_e.get(),
                "location": loc_e.get(),
                "date": datetime.now().strftime("%B %d, %Y"),
                "contact": cont_e.get()
            }
            self.listings.append(new_item)
            self.save_listings()
            win.destroy()
            self.render_listings("all")

        ctk.CTkButton(win, text="Submit Post", fg_color=COLOR_BSU_RED, command=submit).pack(pady=30)

if __name__ == "__main__":
    app = LostAndFoundApp()
    app.mainloop()