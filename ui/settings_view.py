import customtkinter as ctk
from core.config import load_settings, save_settings
from tkinter import messagebox

class SettingsView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=0, pady=(0, 20), sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="⚙️ 서비스 환경 설정 (Settings)", 
                                        font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(side="left", anchor="nw")

        # Load current settings
        self.settings = load_settings()

        # Scrollable container for settings
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.scroll_frame.columnconfigure(0, weight=1)

        # 1. AI Configuration Card
        self.api_card = self.create_card(self.scroll_frame, "🤖 AI 엔진 및 API 설정")
        self.api_card.grid(row=0, column=0, padx=0, pady=(0, 20), sticky="ew")
        
        ctk.CTkLabel(self.api_card, text="주요 AI 제공자 선택", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=25, pady=(10, 5))
        self.provider_menu = ctk.CTkOptionMenu(self.api_card, values=["OpenAI", "Anthropic", "Gemini"], height=40)
        self.provider_menu.set(self.settings.get("ai_provider", "OpenAI"))
        self.provider_menu.pack(fill="x", padx=25, pady=(0, 15))

        self.openai_key_entry = self.create_input(self.api_card, "OpenAI API Key (GPT-4o)", 
                                               placeholder="sk-...", show="*", 
                                               value=self.settings.get("openai_api_key", ""))
        
        self.anthropic_key_entry = self.create_input(self.api_card, "Anthropic API Key (Claude 3.5)", 
                                               placeholder="sk-ant-...", show="*", 
                                               value=self.settings.get("anthropic_api_key", ""))

        self.google_key_entry = self.create_input(self.api_card, "Google API Key (Gemini 2.0 Flash)", 
                                               placeholder="AIza...", show="*", 
                                               value=self.settings.get("google_api_key", ""))

        # 2. Company Information Card
        self.company_card = self.create_card(self.scroll_frame, "🏢 회사 및 담당자 정보")
        self.company_card.grid(row=1, column=0, padx=0, pady=(0, 20), sticky="ew")
        
        self.company_entry = self.create_input(self.company_card, "회사명", 
                                               value=self.settings.get("company_name", ""))
        self.contact_entry = self.create_input(self.company_card, "담당자 이름", 
                                               value=self.settings.get("contact_name", ""))
        
        ctk.CTkLabel(self.company_card, text="주요 제품/서비스 설명", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=25, pady=(10, 5))
        self.desc_text = ctk.CTkTextbox(self.company_card, height=120, border_width=1)
        self.desc_text.insert("1.0", self.settings.get("product_description", ""))
        self.desc_text.pack(fill="x", padx=25, pady=(0, 25))

        # 3. Notion Integration Card
        self.notion_card = self.create_card(self.scroll_frame, "📔 Notion 연동 설정")
        self.notion_card.grid(row=2, column=0, padx=0, pady=0, sticky="ew")
        
        self.notion_api_key = self.create_input(self.notion_card, "Notion API Key (Internal Integration Token)", 
                                               placeholder="secret_...", show="*", 
                                               value=self.settings.get("notion_api_key", ""))
        self.notion_db_id = self.create_input(self.notion_card, "Notion Database ID", 
                                               placeholder="32자리 ID", 
                                               value=self.settings.get("notion_database_id", ""))

        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=0, pady=(20, 0), sticky="ew")
        
        self.save_button = ctk.CTkButton(self.btn_frame, text="💾 설정 저장하기", 
                                         command=self.save_settings,
                                         height=50,
                                         font=ctk.CTkFont(size=16, weight="bold"))
        self.save_button.pack(fill="x")

    def create_card(self, master, title):
        card = ctk.CTkFrame(master, corner_radius=15, border_width=1, border_color=("#DBDBDB", "#333333"))
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(20, 10))
        return card

    def create_input(self, master, label, placeholder="", show=None, value=""):
        ctk.CTkLabel(master, text=label, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=25, pady=(10, 5))
        entry = ctk.CTkEntry(master, placeholder_text=placeholder, show=show, height=40)
        entry.insert(0, value)
        entry.pack(fill="x", padx=25, pady=(0, 15))
        return entry

    def save_settings(self):
        new_settings = {
            "ai_provider": self.provider_menu.get(),
            "openai_api_key": self.openai_key_entry.get(),
            "anthropic_api_key": self.anthropic_key_entry.get(),
            "google_api_key": self.google_key_entry.get(),
            "company_name": self.company_entry.get(),
            "contact_name": self.contact_entry.get(),
            "product_description": self.desc_text.get("1.0", "end-1c"),
            "notion_api_key": self.notion_api_key.get(),
            "notion_database_id": self.notion_db_id.get(),
            "stats": self.settings.get("stats", {"leads": 0, "inquiries": 0, "notion_syncs": 0})
        }
        save_settings(new_settings)
        messagebox.showinfo("저장 완료", "설정이 안전하게 저장되었습니다.")

