import customtkinter as ctk
from models.user import User

# React Colors
C_BG_BASE = '#0A0E27'
C_BG_CARD = '#0F172A'
C_PRIMARY = '#0EA5E9'
C_PRIMARY_HOVER = '#0284C7'
C_TEXT_PRIMARY = '#F1F5F9'
C_TEXT_MUTED = '#94A3B8'
C_BORDER_GLOW = '#38BDF8'
C_ERROR = '#EF4444'

class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clinic Management - Login")
        self.geometry("450x500")
        self.resizable(False, False)
        self.configure(fg_color=C_BG_BASE)
        
        # Center the window on screen
        self.update_idletasks()
        try:
            self.eval('tk::PlaceWindow . center')
        except Exception:
            pass 

        self.is_authenticated = False
        self.logged_in_user = None
        self.logged_in_role = None

        # Build UI
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Glassmorphism Card
        self.frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        self.frame.grid(row=0, column=0, padx=40, pady=50, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.lbl_title = ctk.CTkLabel(self.frame, text="Welcome Back", font=ctk.CTkFont(size=28, weight="bold"), text_color=C_TEXT_PRIMARY)
        self.lbl_title.grid(row=1, column=0, pady=(30, 30))

        self.entry_username = ctk.CTkEntry(self.frame, placeholder_text="Username", width=250, height=45, 
                                           fg_color=C_BG_BASE, border_color="#1E293B", text_color=C_TEXT_PRIMARY, placeholder_text_color=C_TEXT_MUTED)
        self.entry_username.grid(row=2, column=0, pady=10)
        self.entry_username.bind("<Return>", lambda e: self.login())

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Password", show="•", width=250, height=45,
                                           fg_color=C_BG_BASE, border_color="#1E293B", text_color=C_TEXT_PRIMARY, placeholder_text_color=C_TEXT_MUTED)
        self.entry_password.grid(row=3, column=0, pady=10)
        self.entry_password.bind("<Return>", lambda e: self.login())

        self.btn_login = ctk.CTkButton(self.frame, text="Sign In", command=self.login, width=250, height=45, 
                                       font=ctk.CTkFont(size=15, weight="bold"), fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER)
        self.btn_login.grid(row=4, column=0, pady=30)

        self.lbl_error = ctk.CTkLabel(self.frame, text="", text_color=C_ERROR, font=ctk.CTkFont(size=13))
        self.lbl_error.grid(row=5, column=0, sticky="n")

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            self.lbl_error.configure(text="Please enter both fields.")
            return

        user_data = User.authenticate(username, password)
        if user_data:
            self.is_authenticated = True
            self.logged_in_user = user_data['username']
            self.logged_in_role = user_data['role']
            self.destroy()
        else:
            self.lbl_error.configure(text="Invalid credentials.")
