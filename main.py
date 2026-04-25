import customtkinter as ctk
from ui.home_view import HomeView
from ui.lead_gen import LeadGenView
from ui.inquiry import InquiryView
from ui.settings_view import SettingsView
from core.ai_service import AIService

class SalesAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Global Style Configuration ---
        ctk.set_appearance_mode("dark")  # Default to dark mode
        ctk.set_default_color_theme("blue")  # Modern blue theme
        
        self.title("Sales AI Assistant Pro")
        self.geometry("1100x750")
        self.configure(fg_color=("#F2F2F2", "#1A1A1A"))

        # Initialize AI Service
        self.ai_service = AIService()

        # Grid Layout (Sidebar | Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=("#EBEBEB", "#242424"), border_width=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Logo / Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Sales AI", font=ctk.CTkFont(size=24, weight="bold", family="Helvetica"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        # Navigation Buttons
        self.nav_buttons = []
        self.btn_home = self.create_nav_button("🏠 홈 대시보드", self.show_home, 1)
        self.btn_lead = self.create_nav_button("🎯 리드 발굴", self.show_lead_gen, 2)
        self.btn_inquiry = self.create_nav_button("💬 문의 답변", self.show_inquiry, 3)
        self.btn_settings = self.create_nav_button("⚙️ 회사 설정", self.show_settings, 4)

        # Appearance Mode
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", font=ctk.CTkFont(size=11))
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],
                                                                       command=self.change_appearance_mode,
                                                                       height=28)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Main Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Initialize Views
        self.views = {}
        self.views["home"] = HomeView(self.content_frame)
        self.views["lead_gen"] = LeadGenView(self.content_frame, self.ai_service)
        self.views["inquiry"] = InquiryView(self.content_frame, self.ai_service)
        self.views["settings"] = SettingsView(self.content_frame)

        # Default View
        self.show_home()

    def create_nav_button(self, text, command, row):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, 
                            command=command, 
                            height=45, 
                            font=ctk.CTkFont(size=14, weight="bold"),
                            anchor="w",
                            fg_color="transparent",
                            text_color=("#333333", "#D1D1D1"),
                            hover_color=("#DBDBDB", "#2B2B2B"),
                            corner_radius=8)
        btn.grid(row=row, column=0, padx=15, pady=5, sticky="ew")
        self.nav_buttons.append(btn)
        return btn

    def update_nav_styles(self, active_button):
        for btn in self.nav_buttons:
            if btn == active_button:
                btn.configure(fg_color=("#3B8ED0", "#1F538D"), text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("#333333", "#D1D1D1"))

    def show_view(self, view_name, active_button):
        for view in self.views.values():
            view.grid_forget()
        
        # Reload views if they need refreshing (like Home)
        if view_name == "home":
             self.views["home"] = HomeView(self.content_frame)
             
        self.views[view_name].grid(row=0, column=0, sticky="nsew")
        self.update_nav_styles(active_button)

    def show_home(self):
        self.show_view("home", self.btn_home)

    def show_lead_gen(self):
        self.show_view("lead_gen", self.btn_lead)

    def show_inquiry(self):
        self.show_view("inquiry", self.btn_inquiry)

    def show_settings(self):
        self.show_view("settings", self.btn_settings)

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = SalesAIApp()
    app.mainloop()
