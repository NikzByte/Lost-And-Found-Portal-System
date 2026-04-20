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
    def __init__(window):
        super().__init__()

        window.title("Batangas State University - Lost and Found")
        window.geometry("1200x800")
        window.configure(fg_color=COLOR_WHITE)

        window.current_user = None
        window.listings = window.load_listings()

        # Grid configuration
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(0, weight=1)

        window.show_login()

    # --- DATA LOGIC ---
    def load_listings(window):
        if not os.path.exists("listings.json") or os.stat("listings.json").st_size == 0:
            return []
        try:
            with open("listings.json", "r") as f:
                return json.load(f)
        except: return []

    def save_listings(window):
        with open("listings.json", "w") as f:
            json.dump(window.listings, f, indent=4)

    def check_auth(window, username, password):
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        
        # Adjusting to read from users.json
        if not os.path.exists('users.json'): return False
        
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
                for user in users:
                    if user['username'] == username.lower() and user['password'] == hashed_input:
                        return True
        except:
            return False
        return False

    # --- NAVIGATION & SCREENS ---
    def clear_screen(window):
        for widget in window.winfo_children():
            widget.destroy()

    def show_login(window):
        window.clear_screen()
        frame = ctk.CTkFrame(window, fg_color="transparent")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="LOST & FOUND SYSTEM", font=("Arial", 24, "bold"), text_color=COLOR_BSU_RED).pack(pady=20)
        u_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=300)
        u_entry.pack(pady=10)
        p_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=300)
        p_entry.pack(pady=10)

        def login_cmd():
            if window.check_auth(u_entry.get(), p_entry.get()):
                window.current_user = u_entry.get().lower()
                window.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid Username or Password")

        ctk.CTkButton(frame, text="Login", fg_color=COLOR_BSU_RED, command=login_cmd).pack(pady=10)
        ctk.CTkButton(frame, text="Register New Account", fg_color="gray", command=window.show_register).pack()

    def show_register(window):
        window.clear_screen()
        frame = ctk.CTkFrame(window, fg_color="transparent")
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
                if not e.endswith("@g.batstate-u.edu.ph"):
                    messagebox.showwarning("Warning", "Use @g.batstate-u.edu.ph email only")
                    return
                
                hashed = hashlib.sha256(p.encode()).hexdigest()
                
                # Load existing users or start new list
                users = []
                if os.path.exists('users.json') and os.stat('users.json').st_size != 0:
                    with open('users.json', 'r') as f:
                        users = json.load(f)
                
                # Check if username exists
                if any(user['username'] == u for user in users):
                    messagebox.showwarning("Warning", "Username already exists!")
                    return

                users.append({"username": u, "email": e, "password": hashed})
                
                with open('users.json', 'w') as f:
                    json.dump(users, f, indent=4)
                    
                messagebox.showinfo("Success", "Registration Successful!")
                window.show_login()
            else:
                messagebox.showwarning("Warning", "Fields cannot be empty")

        ctk.CTkButton(frame, text="Register", fg_color=COLOR_BSU_RED, command=reg_cmd).pack(pady=10)
        ctk.CTkButton(frame, text="Back to Login", fg_color="gray", command=window.show_login).pack()

    def show_dashboard(window):
        window.clear_screen()
        
        # 1. SIDEBAR
        window.sidebar = ctk.CTkFrame(window, fg_color=COLOR_BSU_RED, corner_radius=0, width=280)
        window.sidebar.grid(row=0, column=0, sticky="nsew")

        try:
            logo_img = ctk.CTkImage(light_image=Image.open("logo.png"), size=(130, 120))
            ctk.CTkLabel(window.sidebar, image=logo_img, text="").pack(pady=30)
        except:
            ctk.CTkLabel(window.sidebar, text="BSU LOGO", text_color="white", font=("Arial", 20, "bold")).pack(pady=30)

        # Sidebar Buttons
        btn_opts = {"fg_color": "transparent", "text_color": "white", "anchor": "w", "font": ("Arial", 14, "bold"), "height": 50}
        
        ctk.CTkButton(window.sidebar, text="⊕ CREATE A POST", fg_color="white", text_color=COLOR_BSU_RED, corner_radius=25, font=("Arial", 14, "bold"), command=window.open_create_post).pack(padx=20, pady=20, fill="x")
        ctk.CTkButton(window.sidebar, text="🔍  VIEW ALL LISTINGS", command=lambda: window.render_listings("all"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(window.sidebar, text="🔍  LOST ITEM LISTINGS", command=lambda: window.render_listings("Lost"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(window.sidebar, text="🔍  FOUND ITEM LISTINGS", command=lambda: window.render_listings("Found"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(window.sidebar, text="📑  MY LISTINGS", command=lambda: window.render_listings("mine"), **btn_opts).pack(fill="x", padx=10)
        ctk.CTkButton(window.sidebar, text="Logout", command=window.show_login, **btn_opts).pack(side="bottom", pady=20, fill="x", padx=10)

        # 2. MAIN AREA
        window.main_container = ctk.CTkFrame(window, fg_color="#F9F9F9", corner_radius=0)
        window.main_container.grid(row=0, column=1, sticky="nsew")

        # Header
        header = ctk.CTkFrame(window.main_container, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 10))
        ctk.CTkLabel(header, text="LOST AND FOUND LISTING SYSTEM", font=("Arial", 28, "bold"), text_color=COLOR_BSU_RED).pack(side="left")
        
        # User Display
        user_display = ctk.CTkFrame(header, fg_color="transparent")
        user_display.pack(side="right")
        ctk.CTkLabel(user_display, text=f"{window.current_user.upper()}\nStudent", font=("Arial", 10), justify="right").pack(side="left", padx=10)
        ctk.CTkLabel(user_display, text="👤", font=("Arial", 30), text_color=COLOR_BSU_RED).pack(side="right")

        # Search Bar
        window.search_bar = ctk.CTkEntry(
            window.main_container,
            placeholder_text="🔍 Search by item name",
            height=45,
            corner_radius=25,
            fg_color="#EEEEEE",
            border_width=0
        )
        window.search_bar.pack(fill="x", padx=40, pady=10)
        window.search_bar.bind("<KeyRelease>", lambda e: window.render_listings("all"))
 
        # Scroll Feed
        window.scroll_feed = ctk.CTkScrollableFrame(window.main_container, fg_color="transparent")
        window.scroll_feed.pack(fill="both", expand=True, padx=40, pady=10)

        # 3. RIGHT PANEL
        window.guide_panel = ctk.CTkFrame(window, fg_color=COLOR_WHITE, width=220, corner_radius=0)
        window.guide_panel.grid(row=0, column=2, sticky="nsew")
        ctk.CTkLabel(window.guide_panel, text="LISTING GUIDELINES", font=("Arial", 12, "bold"), text_color=COLOR_BSU_RED).pack(pady=(40, 10))
        
        guide_text = "• Be specific\n• Identify colors\n• State location\n• Mention markings\n• Withhold secret detail\n• Professional language"
        ctk.CTkLabel(window.guide_panel, text=guide_text, justify="left", font=("Arial", 11)).pack(padx=20)

        window.render_listings("all")

    def render_listings(window, filter_type):
        for widget in window.scroll_feed.winfo_children():
            widget.destroy()

        query = window.search_bar.get().lower()

        for item in window.listings:
            if filter_type == "Lost" and item['status'] != "Lost": continue
            if filter_type == "Found" and item['status'] != "Found": continue
            if filter_type == "mine" and item['user'] != window.current_user: continue
            if query and not (query in item['name'].lower() or query in item['description'].lower() or query in item['location'].lower()):
                continue

            card = ctk.CTkFrame(window.scroll_feed, fg_color=COLOR_WHITE, corner_radius=10, border_width=1, border_color="#DDDDDD")
            card.pack(fill="x", pady=10, padx=5)

            title_f = ctk.CTkFrame(card, fg_color="transparent")
            title_f.pack(fill="x", padx=15, pady=10)
            ctk.CTkLabel(title_f, text="👤", font=("Arial", 25), text_color=COLOR_BSU_RED).pack(side="left")
            ctk.CTkLabel(title_f, text=f"{item['user'].upper()}\n{item['date']}", font=("Arial", 11, "bold"), justify="left").pack(side="left", padx=10)

            details = (f"Item ID: {item['id']}\nItem name: {item['name']}\nDescription: {item['description']}\n"
                       f"Location: {item['location']}\nContact: {item['contact']}\nStatus = {item['status']}")
            ctk.CTkLabel(card, text=details, font=("Arial", 12), justify="left").pack(padx=55, pady=(0, 15), anchor="w")
            
            if item['user'] == window.current_user:
                action_frame = ctk.CTkFrame(card, fg_color="transparent")
                action_frame.pack(anchor="e", padx=15, pady=(0, 10))
                ctk.CTkButton(action_frame, text="Edit", width=80, fg_color="gray", command=lambda i=item: window.open_edit_post(i)).pack(side="left", padx=5)
                ctk.CTkButton(action_frame, text="Delete", width=80, fg_color="red", command=lambda i=item: window.delete_post(i)).pack(side="left", padx=5)

    def open_create_post(window):
        win = ctk.CTkToplevel(window)
        win.title("Create New Post")
        win.geometry("400x600")
        win.attributes('-topmost', True)

        ctk.CTkLabel(win, text="POST AN ITEM", font=("Arial", 18, "bold"), text_color=COLOR_BSU_RED).pack(pady=20)
        name_e = ctk.CTkEntry(win, placeholder_text="Item Name", width=300); name_e.pack(pady=5)
        status_c = ctk.CTkComboBox(win, values=["Lost", "Found"], width=300); status_c.pack(pady=5)
        desc_e = ctk.CTkEntry(win, placeholder_text="Description", width=300); desc_e.pack(pady=5)
        loc_e = ctk.CTkEntry(win, placeholder_text="Location", width=300); loc_e.pack(pady=5)
        cont_e = ctk.CTkEntry(win, placeholder_text="Contact Details", width=300); cont_e.pack(pady=5)

        def submit():
            if not name_e.get():
                messagebox.showwarning("Warning", "Item name is required")
                return
            new_item = {
                "user": window.current_user,
                "status": status_c.get(),
                "id": str(uuid.uuid4().hex[:6].upper()),
                "name": name_e.get(),
                "description": desc_e.get(),
                "location": loc_e.get(),
                "date": datetime.now().strftime("%B %d, %Y"),
                "contact": cont_e.get()
            }
            window.listings.append(new_item)
            window.save_listings()
            win.destroy()
            window.render_listings("all")

        ctk.CTkButton(win, text="Submit Post", fg_color=COLOR_BSU_RED, command=submit).pack(pady=30)
        
    def open_edit_post(window, item):
        win = ctk.CTkToplevel(window)
        win.title("Edit Post")
        win.geometry("400x600")
        win.attributes('-topmost', True)
        
        ctk.CTkLabel(win, text="EDIT ITEM", font=("Arial", 18, "bold"), text_color=COLOR_BSU_RED).pack(pady=20)
        name_e = ctk.CTkEntry(win, width=300); name_e.insert(0, item['name']); name_e.pack(pady=5)
        status_c = ctk.CTkComboBox(win, values=["Lost", "Found"], width=300); status_c.set(item['status']); status_c.pack(pady=5)
        desc_e = ctk.CTkEntry(win, width=300); desc_e.insert(0, item['description']); desc_e.pack(pady=5)
        loc_e = ctk.CTkEntry(win, width=300); loc_e.insert(0, item['location']); loc_e.pack(pady=5)
        cont_e = ctk.CTkEntry(win, width=300); cont_e.insert(0, item['contact']); cont_e.pack(pady=5)

        def save_changes():
            item.update({
                'name': name_e.get(),
                'status': status_c.get(),
                'description': desc_e.get(),
                'location': loc_e.get(),
                'contact': cont_e.get()
            })
            window.save_listings()
            win.destroy()
            window.render_listings("all")

        ctk.CTkButton(win, text="Save Changes", fg_color=COLOR_BSU_RED, command=save_changes).pack(pady=30)
        
    def delete_post(window, item):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this listing?"):
            window.listings.remove(item)
            window.save_listings()
            window.render_listings("all")
            
if __name__ == "__main__":
    app = LostAndFoundApp()
    app.mainloop()