import customtkinter as ctk
from core.config import load_settings

class HomeView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Header
        self.title_label = ctk.CTkLabel(self, text="🚀 Sales AI Dashboard", font=ctk.CTkFont(size=32, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(0, 40), sticky="w")

        # Stats Cards
        self.settings = load_settings()
        stats = self.settings.get("stats", {"leads": 0, "inquiries": 0, "notion_syncs": 0})

        self.create_stat_card("🎯 발굴된 리드", stats["leads"], 0)
        self.create_stat_card("💬 생성된 답변", stats["inquiries"], 1)
        self.create_stat_card("📔 Notion 연동", stats["notion_syncs"], 2)

        # AI Token Usage Visualization
        self.usage_frame = ctk.CTkFrame(self, corner_radius=15, border_width=1)
        self.usage_frame.grid(row=2, column=0, columnspan=3, padx=0, pady=(40, 0), sticky="ew")
        self.usage_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.usage_frame, text="📊 AI 토큰 사용량 시각화", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 15), sticky="w")
        
        token_usage = self.settings.get("token_usage", {"OpenAI": 0, "Anthropic": 0, "Gemini": 0})
        
        # Calculate max for scaling (or use a fixed budget if defined)
        max_usage = max(token_usage.values()) if any(token_usage.values()) else 1000
        # If max_usage is too low, set a reasonable default for visualization
        if max_usage < 1000: max_usage = 1000
        
        providers = [("OpenAI", "#3B8ED0"), ("Anthropic", "#D08E3B"), ("Gemini", "#8ED03B")]
        for i, (provider, color) in enumerate(providers):
            tokens = token_usage.get(provider, 0)
            percentage = min(tokens / max_usage, 1.0)
            
            ctk.CTkLabel(self.usage_frame, text=f"{provider}: {tokens:,} tokens", font=ctk.CTkFont(size=13)).grid(row=i+1, column=0, padx=(20, 10), pady=10, sticky="w")
            
            progress = ctk.CTkProgressBar(self.usage_frame, height=15, progress_color=color)
            progress.grid(row=i+1, column=1, padx=(0, 20), pady=10, sticky="ew")
            progress.set(percentage)

        # Welcome Message
        self.welcome_card = ctk.CTkFrame(self, corner_radius=15, border_width=1)
        self.welcome_card.grid(row=3, column=0, columnspan=3, padx=0, pady=40, sticky="ew")
        
        msg = f"""반갑습니다, {self.settings.get('contact_name', '사용자')}님!
오늘도 Sales AI와 함께 스마트한 영업을 시작해 보세요.

왼쪽 메뉴에서 리드 발굴을 시작하거나 고객 문의에 대응할 수 있습니다."""
        
        ctk.CTkLabel(self.welcome_card, text=msg, font=ctk.CTkFont(size=16), justify="left").pack(padx=30, pady=30)

    def create_stat_card(self, title, value, col):
        card = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color=("#DBDBDB", "#333333"))
        card.grid(row=1, column=col, padx=10, pady=0, sticky="nsew")
        
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=36, weight="bold"), text_color=("#3B8ED0", "#1F538D")).pack(pady=(0, 20))

    def refresh_stats(self):
        self.settings = load_settings()
        # (상세 구현 생략: 화면 전환 시 다시 호출됨)
