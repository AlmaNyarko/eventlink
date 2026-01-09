import tkinter as tk
from tkinter import ttk, messagebox

# --- Design Constants (Based on your screenshots) ---
COLOR_BG_MAIN = "#f3f4f6"       # Light gray background
COLOR_BG_SIDEBAR = "#ffffff"    # White sidebar
COLOR_CARD = "#ffffff"          # White card background
COLOR_PRIMARY = "#2563eb"       # The "EventLink" Blue
COLOR_TEXT_MAIN = "#111827"     # Dark text
COLOR_TEXT_MUTED = "#6b7280"    # Grey text
FONT_HEADER = ("Helvetica", 20, "bold")
FONT_SUBHEADER = ("Helvetica", 14, "bold")
FONT_BODY = ("Helvetica", 10)

class EventLinkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EventLink")
        self.geometry("1000x700")
        self.configure(bg=COLOR_BG_MAIN)
        
        # Initialize the main container
        self.container = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.container.pack(fill="both", expand=True)
        
        # Start with the Login Screen
        self.show_login_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ==========================
    # SCREEN 1: LOGIN (Matches IMG_5009)
    # ==========================
    def show_login_screen(self):
        self.clear_screen()
        
        # Center Box
        login_card = tk.Frame(self.container, bg=COLOR_CARD, padx=40, pady=40)
        login_card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=500)
        
        # Logo / Brand
        tk.Label(login_card, text="✨ EventLink", font=("Helvetica", 16, "bold"), fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(pady=(0, 20))
        
        # Header
        tk.Label(login_card, text="Welcome back", font=FONT_HEADER, fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(anchor="w")
        tk.Label(login_card, text="Sign in to your account to continue", font=FONT_BODY, fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w", pady=(0, 20))
        
        # Inputs
        tk.Label(login_card, text="Email address", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.email_entry = tk.Entry(login_card, font=FONT_BODY, highlightthickness=1, relief="flat", bg="#f9fafb")
        self.email_entry.pack(fill="x", pady=(5, 15), ipady=5)
        
        tk.Label(login_card, text="Password", font=("Helvetica", 9, "bold"), bg=COLOR_CARD, fg=COLOR_TEXT_MAIN).pack(anchor="w")
        self.pass_entry = tk.Entry(login_card, show="*", font=FONT_BODY, highlightthickness=1, relief="flat", bg="#f9fafb")
        self.pass_entry.pack(fill="x", pady=(5, 20), ipady=5)
        
        # Primary Button (Using tk.Button for color control)
        # Note: On Mac, background colors on buttons are restricted by the OS. On Windows/Linux, this will be Blue.
        btn = tk.Button(login_card, text="Sign in  →", bg=COLOR_PRIMARY, fg="white", font=("Helvetica", 10, "bold"), 
                        relief="flat", command=self.show_dashboard_screen)
        btn.pack(fill="x", ipady=8)
        
        # Footer
        tk.Label(login_card, text="Don't have an account? Sign up", font=("Helvetica", 9), fg=COLOR_PRIMARY, bg=COLOR_CARD).pack(pady=20)

    # ==========================
    # SCREEN 2: DASHBOARD (Matches IMG_5011/5010)
    # ==========================
    def show_dashboard_screen(self):
        self.clear_screen()
        
        # --- Sidebar (Left) ---
        sidebar = tk.Frame(self.container, bg=COLOR_BG_SIDEBAR, width=250)
        sidebar.pack(side="left", fill="y")
        
        # Sidebar Logo
        tk.Label(sidebar, text="✨ EventLink", font=("Helvetica", 16, "bold"), fg=COLOR_PRIMARY, bg=COLOR_BG_SIDEBAR).pack(pady=30, padx=20, anchor="w")
        
        # Sidebar Menu Items
        menu_items = ["🏠  Home", "📅  My Events", "💳  Payments", "👤  Profile", "⚙️  Settings"]
        for item in menu_items:
            btn = tk.Button(sidebar, text=item, font=("Helvetica", 11), bg=COLOR_BG_SIDEBAR, fg=COLOR_TEXT_MAIN, 
                            relief="flat", anchor="w", padx=20, borderwidth=0)
            btn.pack(fill="x", pady=5, ipady=5)

        # --- Main Content Area (Right) ---
        main_area = tk.Frame(self.container, bg=COLOR_BG_MAIN)
        main_area.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        # Top Bar
        top_frame = tk.Frame(main_area, bg=COLOR_BG_MAIN)
        top_frame.pack(fill="x", pady=(0, 20))
        tk.Label(top_frame, text="Dashboard", font=FONT_HEADER, bg=COLOR_BG_MAIN, fg=COLOR_TEXT_MAIN).pack(side="left")
        tk.Button(top_frame, text="+ Create Event", bg=COLOR_PRIMARY, fg="white", relief="flat", font=("Helvetica", 10, "bold")).pack(side="right", padx=10)

        # Dashboard Logic: Stats Cards
        stats_frame = tk.Frame(main_area, bg=COLOR_BG_MAIN)
        stats_frame.pack(fill="x", pady=20)
        
        self.create_stat_card(stats_frame, "Total Events", "12", "+3 this month")
        self.create_stat_card(stats_frame, "Total Attendees", "8,450", "+1,250 this month")
        self.create_stat_card(stats_frame, "Total Revenue", "$425,000", "+$85k this month")

        # Upcoming Events Section (Matches IMG_5011)
        tk.Label(main_area, text="Your Upcoming Events", font=FONT_SUBHEADER, bg=COLOR_BG_MAIN, fg=COLOR_TEXT_MAIN).pack(anchor="w", pady=(20, 10))
        
        events_list = tk.Frame(main_area, bg=COLOR_BG_MAIN)
        events_list.pack(fill="both", expand=True)
        
        # Event 1
        self.create_event_row(events_list, "Summer Music Festival 2025", "Jul 15, 2025 • 2,500 attendees", "$112,500")
        # Event 2
        self.create_event_row(events_list, "Tech Innovation Summit", "Aug 05, 2025 • 1,200 attendees", "$144,000")
        # Event 3
        self.create_event_row(events_list, "Jazz Night Under the Stars", "Sep 28, 2025 • 300 attendees", "$15,400")

    def create_stat_card(self, parent, title, value, subtext):
        card = tk.Frame(parent, bg=COLOR_CARD, padx=20, pady=20)
        card.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        tk.Label(card, text=title, font=("Helvetica", 10), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w")
        tk.Label(card, text=value, font=("Helvetica", 20, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(anchor="w", pady=5)
        tk.Label(card, text=subtext, font=("Helvetica", 9), fg="green", bg=COLOR_CARD).pack(anchor="w")

    def create_event_row(self, parent, name, details, revenue):
        row = tk.Frame(parent, bg=COLOR_CARD, padx=20, pady=15)
        row.pack(fill="x", pady=5)
        
        # Left: Info
        info_frame = tk.Frame(row, bg=COLOR_CARD)
        info_frame.pack(side="left")
        tk.Label(info_frame, text=name, font=("Helvetica", 11, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(anchor="w")
        tk.Label(info_frame, text=details, font=("Helvetica", 9), fg=COLOR_TEXT_MUTED, bg=COLOR_CARD).pack(anchor="w")
        
        # Right: Revenue & Action
        tk.Button(row, text="View", bg="white", fg=COLOR_TEXT_MAIN, relief="solid", borderwidth=1).pack(side="right", padx=10)
        tk.Label(row, text=revenue, font=("Helvetica", 11, "bold"), fg=COLOR_TEXT_MAIN, bg=COLOR_CARD).pack(side="right", padx=20)

if __name__ == "__main__":
    app = EventLinkApp()
    app.mainloop()