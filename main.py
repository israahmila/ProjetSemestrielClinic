import customtkinter as ctk
import sys
import os

# Ensure the app can import modules properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.patients_view import PatientsView
from views.doctors_view import DoctorsView
from views.appointments_view import AppointmentsView
from views.prescriptions_view import PrescriptionsView

# Set application appearance
ctk.set_appearance_mode("Dark")

# Colors from React theme
C_BG_BASE = '#0A0E27'
C_BG_CARD = '#0F172A'
C_PRIMARY = '#0EA5E9'
C_PRIMARY_HOVER = '#0284C7'
C_TEXT_PRIMARY = '#F1F5F9'
C_TEXT_MUTED = '#94A3B8'
C_BORDER = '#1E293B'

class App(ctk.CTk):
    def __init__(self, username, role):
        super().__init__()
        self.title("Clinic Management System")
        self.geometry("1100x750")
        self.minsize(1100, 750)
        self.configure(fg_color=C_BG_BASE)
        
        self.username = username
        self.role = role
        self.active_button = None
        
        # Grid layout (1 row, 2 columns)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1) # push spacer
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="🏥 Clinic Admin", font=ctk.CTkFont(size=22, weight="bold"), text_color=C_TEXT_PRIMARY)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(24, 24))
        
        # Sidebar Buttons
        self.buttons = {}
        
        self.btn_dashboard = self.create_nav_button("📊 Dashboard", "dashboard")
        self.btn_dashboard.grid(row=1, column=0, padx=15, pady=5)
        
        self.btn_patients = self.create_nav_button("👥 Patients", "patients")
        self.btn_patients.grid(row=2, column=0, padx=15, pady=5)
        
        self.btn_doctors = self.create_nav_button("👨‍⚕️ Doctors", "doctors")
        self.btn_doctors.grid(row=3, column=0, padx=15, pady=5)
        
        self.btn_appointments = self.create_nav_button("📅 Appointments", "appointments")
        self.btn_appointments.grid(row=4, column=0, padx=15, pady=5)
        
        self.btn_prescriptions = self.create_nav_button("💊 Prescriptions", "prescriptions")
        self.btn_prescriptions.grid(row=5, column=0, padx=15, pady=5)
        
        self.user_label = ctk.CTkLabel(self.sidebar, text=f"Logged in as:\n{self.username} ({self.role})", font=ctk.CTkFont(size=12), text_color=C_TEXT_MUTED)
        self.user_label.grid(row=7, column=0, padx=20, pady=20, sticky="s")
        
        self.btn_logout = ctk.CTkButton(self.sidebar, text="🚪 Logout", command=self.logout, fg_color="transparent", 
                                        border_width=1, border_color=C_PRIMARY, text_color=C_PRIMARY, hover_color=C_BG_BASE)
        self.btn_logout.grid(row=8, column=0, padx=20, pady=24)
        
        # Main Frame area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=24, pady=24)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Dictionary to store views
        self.views = {}
        
        # Initialize views
        self.views["dashboard"] = DashboardView(self.main_frame, self)
        self.views["patients"] = PatientsView(self.main_frame, self)
        self.views["doctors"] = DoctorsView(self.main_frame, self)
        self.views["appointments"] = AppointmentsView(self.main_frame, self)
        self.views["prescriptions"] = PrescriptionsView(self.main_frame, self)
        
        # Place all views in the same grid spot
        for view in self.views.values():
            view.grid(row=0, column=0, sticky="nsew")
            
        self.show_view("dashboard")

    def create_nav_button(self, text, view_name):
        btn = ctk.CTkButton(self.sidebar, text=text, anchor="w", fg_color="transparent", 
                            text_color=C_TEXT_MUTED, hover_color=C_BG_BASE,
                            height=40, font=ctk.CTkFont(size=14, weight="normal"),
                            command=lambda: self.show_view(view_name))
        self.buttons[view_name] = btn
        return btn

    def show_view(self, name):
        # Update active button styles
        for v_name, btn in self.buttons.items():
            if v_name == name:
                btn.configure(fg_color=C_PRIMARY, text_color=C_TEXT_PRIMARY, hover_color=C_PRIMARY_HOVER)
            else:
                btn.configure(fg_color="transparent", text_color=C_TEXT_MUTED, hover_color=C_BG_BASE)
                
        # Refresh data when showing view
        view = self.views[name]
        if hasattr(view, "refresh_data"):
            view.refresh_data()
        view.tkraise()
    
    def logout(self):
        self.destroy()
        start_login()

def start_login():
    login_window = LoginView()
    login_window.mainloop()
    
    if login_window.is_authenticated:
        app = App(login_window.logged_in_user, login_window.logged_in_role)
        app.mainloop()

if __name__ == "__main__":
    start_login()
