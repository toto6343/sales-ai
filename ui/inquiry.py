import customtkinter as ctk
from core.ai_service import AIService
from core.notion_service import NotionService
import threading
import pyperclip
from tkinter import messagebox, filedialog
import pdfplumber
import pandas as pd
import os

class InquiryView(ctk.CTkFrame):
    def __init__(self, master, ai_service: AIService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.ai_service = ai_service
        self.notion_service = NotionService()
        self.uploaded_content = ""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=0, pady=(0, 20), sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="💬 스마트 문의 답변 (Smart Inquiry)", 
                                        font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(side="left", anchor="nw")

        # File Upload Buttons
        self.upload_btn = ctk.CTkButton(self.header_frame, text="📄 관련 서류 첨부", 
                                        command=self.upload_file, width=150, height=35,
                                        fg_color=("#2FA572", "#217346"))
        self.upload_btn.pack(side="right")

        # TabView
        self.tabview = ctk.CTkTabview(self, corner_radius=15, border_width=1, border_color=("#DBDBDB", "#333333"))
        self.tabview.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.tabview.add("📥 인바운드 (고객 문의)")
        self.tabview.add("📤 아웃바운드 (제안/영업)")

        # Setup Tabs
        self.setup_inbound_tab()
        self.setup_outbound_tab()

        # Shared Result Card
        self.result_frame = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color=("#DBDBDB", "#333333"))
        self.result_frame.grid(row=2, column=0, padx=0, pady=(20, 0), sticky="nsew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=1)

        self.res_header = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.res_header.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        
        self.res_label = ctk.CTkLabel(self.res_header, text="생성된 AI 답변", font=ctk.CTkFont(size=16, weight="bold"))
        self.res_label.pack(side="left")

        self.sync_notion_btn = ctk.CTkButton(self.res_header, text="📔 Notion 저장", 
                                              command=self.sync_to_notion, width=100, height=32)
        self.sync_notion_btn.pack(side="right", padx=5)
        
        self.copy_button = ctk.CTkButton(self.res_header, text="📋 복사", width=80, height=32, 
                                         command=self.copy_to_clipboard,
                                         fg_color=("#3B8ED0", "#1F538D"))
        self.copy_button.pack(side="right", padx=5)

        self.result_text = ctk.CTkTextbox(self.result_frame, font=ctk.CTkFont(size=13), border_width=0)
        self.result_text.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="nsew")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.xlsx *.xls *.md *.txt")])
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == ".pdf":
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                self.uploaded_content = text[:5000]
                messagebox.showinfo("성공", f"PDF 파일 '{os.path.basename(file_path)}'을 읽어왔습니다.")
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
                self.uploaded_content = df.to_string(index=False)[:5000]
                messagebox.showinfo("성공", f"엑셀 파일 '{os.path.basename(file_path)}'을 읽어왔습니다.")
            elif ext in [".md", ".txt"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.uploaded_content = f.read()[:5000]
                messagebox.showinfo("성공", f"{ext.upper()} 파일 '{os.path.basename(file_path)}'을 읽어왔습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")

    def sync_to_notion(self):
        result = self.result_text.get("1.0", "end-1c")
        if not result.strip() or "AI 답변 생성 중" in result:
            messagebox.showwarning("데이터 없음", "먼저 답변을 생성해 주세요.")
            return
        
        title = f"영업 답변 초안 ({pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')})"
        success, msg = self.notion_service.add_lead(title, result)
        if success:
            messagebox.showinfo("성공", msg)
        else:
            messagebox.showerror("실패", msg)

    def setup_inbound_tab(self):
        tab = self.tabview.tab("📥 인바운드 (고객 문의)")
        tab.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(tab, text="문의 내용 또는 상황", font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        self.inbound_input = ctk.CTkTextbox(tab, height=120, border_width=1)
        self.inbound_input.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew")

        # Row 1: Main Categories
        btn_frame_1 = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame_1.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.create_quick_btn(btn_frame_1, "💰 가격/견적", lambda: self.quick_response("inbound", "가격 및 견적 문의")).pack(side="left", padx=(0, 10))
        self.create_quick_btn(btn_frame_1, "⚔️ 경쟁사 비교", lambda: self.quick_response("inbound", "경쟁사 비교")).pack(side="left", padx=10)
        self.create_quick_btn(btn_frame_1, "💳 크레딧/결제", lambda: self.quick_response("inbound", "크레딧 및 결제 정책")).pack(side="left", padx=10)

        # Row 2: Secondary Categories
        btn_frame_2 = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame_2.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.create_quick_btn(btn_frame_2, "🛠️ 기능/스펙", lambda: self.quick_response("inbound", "기능 및 스펙 상세")).pack(side="left", padx=(0, 10))
        self.create_quick_btn(btn_frame_2, "🆘 기술 지원", lambda: self.quick_response("inbound", "기술 지원 및 장애 문의")).pack(side="left", padx=10)
        self.create_quick_btn(btn_frame_2, "✨ 자유 답변", lambda: self.quick_response("inbound"), primary=True).pack(side="right")

    def setup_outbound_tab(self):
        tab = self.tabview.tab("📤 아웃바운드 (제안/영업)")
        tab.grid_columnconfigure(0, weight=1)

        # Domain Selection
        domain_frame = ctk.CTkFrame(tab, fg_color="transparent")
        domain_frame.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        
        ctk.CTkLabel(domain_frame, text="🎯 대상 도메인 (산업군)", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(0, 10))
        self.domain_var = ctk.StringVar(value="IT/SW")
        self.domain_menu = ctk.CTkOptionMenu(domain_frame, values=["IT/SW", "제조업", "금융/핀테크", "유통/커머스", "의료/바이오", "교육", "기타"],
                                             variable=self.domain_var, width=150)
        self.domain_menu.pack(side="left")

        ctk.CTkLabel(tab, text="잠재 고객 정보 또는 상황", font=ctk.CTkFont(size=14, weight="bold")).grid(row=1, column=0, padx=20, pady=(15, 5), sticky="w")
        self.outbound_input = ctk.CTkTextbox(tab, height=120, border_width=1)
        self.outbound_input.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")

        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.create_quick_btn(btn_frame, "📧 콜드 메일 작성", lambda: self.quick_response("outbound", "콜드 이메일")).pack(side="left", padx=(0, 10))
        self.create_quick_btn(btn_frame, "☕ 커피챗 제안", lambda: self.quick_response("outbound", "커피챗 제안")).pack(side="left", padx=10)
        self.create_quick_btn(btn_frame, "🚀 자유 제안 생성", lambda: self.quick_response("outbound"), primary=True).pack(side="right")

    def create_quick_btn(self, master, text, command, primary=False):
        # Always use blue background and white text for high visibility as requested
        fg = ("#3B8ED0", "#1F538D")
        return ctk.CTkButton(master, text=text, command=command, height=40, 
                             fg_color=fg, text_color="white",
                             font=ctk.CTkFont(weight="bold"))

    def quick_response(self, mode, template=None):
        context = self.inbound_input.get("1.0", "end-1c") if mode == "inbound" else self.outbound_input.get("1.0", "end-1c")
        target_domain = self.domain_var.get() if mode == "outbound" else None

        if not context.strip() and not template and not self.uploaded_content:
            messagebox.showwarning("입력 필요", "상황 설명을 입력하거나 파일을 첨부해 주세요.")
            return

        self.result_text.delete("1.0", "end")
        self.update_status("🔍 [1/4] 상황 컨텍스트 분석 중...")

        # Combine content
        combined_context = f"{context}\n\n[첨부 서류 내용]\n{self.uploaded_content}"

        thread = threading.Thread(target=self.run_generation, args=(mode, combined_context, template, target_domain))
        thread.start()

    def update_status(self, message):
        self.result_text.insert("insert", f"{message}\n")

    def run_generation(self, mode, context, template, target_domain=None):
        try:
            self.after(0, lambda: self.update_status(f"📝 [2/4] {'대상 도메인 특화' if target_domain else '최적의'} 페르소나 설정 중..."))
            self.after(1000, lambda: self.update_status("✍️ [3/4] 맞춤형 영업 문구 초안 작성 중..."))

            result = self.ai_service.draft_response(mode, context, template, target_domain)

            self.after(0, lambda: self.update_status("✨ [4/4] 답변 생성 완료!"))
            self.after(500, lambda: self.show_result(result))
        except Exception as e:
            self.after(0, lambda: self.show_result(f"오류 발생: {str(e)}"))


    def show_result(self, result):
        from core.config import increment_stat
        self.result_text.delete("1.0", "end")
        self.result_text.insert("insert", result)
        if "오류 발생" not in result:
            increment_stat("inquiries")

    def copy_to_clipboard(self):
        text = self.result_text.get("1.0", "end-1c")
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("복사 완료", "답변이 클립보드에 복사되었습니다.")
