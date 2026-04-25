import customtkinter as ctk
from core.ai_service import AIService
from core.notion_service import NotionService
import threading
from tkinter import filedialog, messagebox
import pdfplumber
import pandas as pd
import os

class LeadGenView(ctk.CTkFrame):
    def __init__(self, master, ai_service: AIService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.ai_service = ai_service
        self.notion_service = NotionService()
        self.uploaded_content = ""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=0, pady=(0, 20), sticky="ew")
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="🎯 리드 발굴 (Lead Generation)", 
                                        font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(side="left", anchor="nw")

        # File Upload Buttons in Header
        self.file_btn_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.file_btn_frame.pack(side="right")
        
        self.upload_btn = ctk.CTkButton(self.file_btn_frame, text="📄 정책 서류 첨부", 
                                        command=self.upload_file, width=150, height=35,
                                        fg_color=("#2FA572", "#217346")) # Greenish for files
        self.upload_btn.pack(side="right", padx=5)

        # Main Input Card
        self.card_frame = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color=("#DBDBDB", "#333333"))
        self.card_frame.grid(row=1, column=0, padx=0, pady=0, sticky="ew")
        self.card_frame.grid_columnconfigure(0, weight=1)

        # Content inside Card
        content_padding = 25
        
        # Industry Input
        self.ind_label = ctk.CTkLabel(self.card_frame, text="타겟 업종", font=ctk.CTkFont(size=14, weight="bold"))
        self.ind_label.grid(row=0, column=0, padx=content_padding, pady=(content_padding, 5), sticky="w")
        self.ind_entry = ctk.CTkEntry(self.card_frame, placeholder_text="예: 제조업, 온라인 쇼핑몰, IT 스타트업", height=40)
        self.ind_entry.grid(row=1, column=0, padx=content_padding, pady=(0, 15), sticky="ew")

        # Customer Size Input
        self.size_label = ctk.CTkLabel(self.card_frame, text="고객사 규모", font=ctk.CTkFont(size=14, weight="bold"))
        self.size_label.grid(row=2, column=0, padx=content_padding, pady=(10, 5), sticky="w")
        self.size_entry = ctk.CTkEntry(self.card_frame, placeholder_text="예: 50인 미만, 매출 100억 이상 중견기업", height=40)
        self.size_entry.grid(row=3, column=0, padx=content_padding, pady=(0, 15), sticky="ew")

        # Details Input
        self.details_label = ctk.CTkLabel(self.card_frame, text="추가 상세 조건 및 파일 컨텍스트", font=ctk.CTkFont(size=14, weight="bold"))
        self.details_label.grid(row=4, column=0, padx=content_padding, pady=(10, 5), sticky="w")
        self.details_entry = ctk.CTkEntry(self.card_frame, placeholder_text="파일을 업로드하면 자동으로 컨텍스트가 추가됩니다", height=40)
        self.details_entry.grid(row=5, column=0, padx=content_padding, pady=(0, 20), sticky="ew")

        # Analyze Button
        self.analyze_button = ctk.CTkButton(self.card_frame, text="잠재 고객 분석 시작", 
                                            command=self.start_analysis,
                                            height=50,
                                            font=ctk.CTkFont(size=16, weight="bold"))
        self.analyze_button.grid(row=6, column=0, padx=content_padding, pady=(0, content_padding), sticky="ew")

        # Result Section (Bottom Card)
        self.result_frame = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color=("#DBDBDB", "#333333"))
        self.result_frame.grid(row=2, column=0, padx=0, pady=(20, 0), sticky="nsew")
        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_rowconfigure(1, weight=1)

        self.res_header = ctk.CTkFrame(self.result_frame, fg_color="transparent")
        self.res_header.grid(row=0, column=0, padx=20, pady=(15, 10), sticky="ew")
        
        self.res_label = ctk.CTkLabel(self.res_header, text="분석 리포트", font=ctk.CTkFont(size=16, weight="bold"))
        self.res_label.pack(side="left")

        self.sync_notion_btn = ctk.CTkButton(self.res_header, text="📔 Notion으로 전송", 
                                              command=self.sync_to_notion, width=120, height=32)
        self.sync_notion_btn.pack(side="right")

        self.result_text = ctk.CTkTextbox(self.result_frame, font=ctk.CTkFont(size=13), border_width=0, corner_radius=0)
        self.result_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.xlsx *.xls *.md *.txt")])
        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == ".pdf":
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                self.uploaded_content = text[:5000] # Limit to first 5k chars for prompt
                messagebox.showinfo("성공", "PDF 파일 내용을 읽어왔습니다.")
            elif ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
                self.uploaded_content = df.to_string(index=False)[:5000]
                messagebox.showinfo("성공", "엑셀 파일 내용을 읽어왔습니다.")
            elif ext in [".md", ".txt"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.uploaded_content = f.read()[:5000]
                messagebox.showinfo("성공", f"{ext.upper()} 파일 내용을 읽어왔습니다.")
            
            self.details_entry.delete(0, "end")
            self.details_entry.insert(0, f"[파일 업로드됨: {os.path.basename(file_path)}]")
            
            # Auto-start analysis after upload
            self.start_analysis()
        except Exception as e:
            messagebox.showerror("오류", f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")

    def sync_to_notion(self):
        result = self.result_text.get("1.0", "end-1c")
        if not result.strip() or "AI 답변 생성 중" in result:
            messagebox.showwarning("데이터 없음", "먼저 분석을 완료해 주세요.")
            return
        
        industry = self.ind_entry.get() or "미지정 업종"
        title = f"리드 분석 리포트: {industry}"
        
        success, msg = self.notion_service.add_lead(title, result)
        if success:
            messagebox.showinfo("성공", msg)
        else:
            messagebox.showerror("실패", msg)

    def start_analysis(self):
        self.result_text.delete("1.0", "end")
        self.update_status("🔍 [1/4] 데이터 수집 및 분석 준비 중...", "disabled")
        
        thread = threading.Thread(target=self.run_analysis)
        thread.start()

    def update_status(self, message, state=None):
        self.result_text.insert("insert", f"{message}\n")
        if state:
            self.analyze_button.configure(state=state, text="분석 진행 중...")

    def run_analysis(self):
        try:
            # Step 2: Context Parsing
            self.after(0, lambda: self.update_status("📄 [2/4] 업로드된 문서 및 컨텍스트 파싱 중..."))
            industry = self.ind_entry.get()
            size = self.size_entry.get()
            details = self.details_entry.get()
            combined_details = f"{details}\n\n[첨부 파일 내용 요약]\n{self.uploaded_content}"

            # Step 3: AI Analysis
            self.after(0, lambda: self.update_status("🧠 [3/4] AI 전략 엔진 가동: 잠재 고객 페르소나 매칭 중..."))
            result = self.ai_service.generate_leads(industry, size, combined_details)
            
            # Step 4: Finalizing
            self.after(0, lambda: self.update_status("✨ [4/4] 리포트 생성 완료!"))
            self.after(500, lambda: self.show_result(result))
        except Exception as e:
            self.after(0, lambda: self.show_result(f"오류 발생: {str(e)}"))

    def show_result(self, result):
        from core.config import increment_stat
        self.result_text.delete("1.0", "end")
        self.result_text.insert("insert", result)
        self.analyze_button.configure(state="normal", text="잠재 고객 분석 시작")
        if "오류 발생" not in result:
            increment_stat("leads")
