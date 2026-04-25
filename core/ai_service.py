from openai import OpenAI
import anthropic
import google.generativeai as genai
from .config import load_settings, add_token_usage, increment_stat

class AIService:
    def __init__(self):
        self.settings = load_settings()
        self.openai_client = None
        self.anthropic_client = None
        self.gemini_model = None
        self._initialize_clients()

    def _initialize_clients(self):
        self.settings = load_settings()
        
        # Initialize OpenAI
        openai_key = self.settings.get("openai_api_key")
        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)
        
        # Initialize Anthropic
        anthropic_key = self.settings.get("anthropic_api_key")
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)

        # Initialize Google Gemini
        google_key = self.settings.get("google_api_key")
        if google_key:
            genai.configure(api_key=google_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')

    def _optimize_text(self, text):
        """불필요한 공백 및 줄바꿈을 제거하여 토큰 사용량을 최소화합니다."""
        if not text: return ""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n".join(lines)

    def generate_leads(self, industry, customer_size, product_details):
        self._initialize_clients()
        provider = self.settings.get("ai_provider", "OpenAI")
        
        # 텍스트 최적화 (토큰 절약)
        industry = self._optimize_text(industry)
        customer_size = self._optimize_text(customer_size)
        product_details = self._optimize_text(product_details)[:4000] # 컨텍스트 제한

        company_info = f"회사명: {self.settings['company_name']}\n제품: {self.settings['product_description']}"
        
        prompt = f"""영업 AI로서 다음 정보를 바탕으로 잠재 고객 리드 5가지를 분석해 주세요.

[우리 회사]
{company_info}

[대상 정보]
- 업종: {industry}
- 규모: {customer_size}
- 상세: {product_details}

[요청]
1. 잠재 고객 유형 5가지 분석.
2. 우선순위, 타겟 포인트, 첫 접근 방법 포함.
3. 한국어로 친절하게 답변."""

        if provider == "OpenAI" and self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                add_token_usage("OpenAI", response.usage.total_tokens)
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI 오류: {str(e)}"
        
        elif provider == "Anthropic" and self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                add_token_usage("Anthropic", response.usage.input_tokens + response.usage.output_tokens)
                return response.content[0].text
            except Exception as e:
                return f"Anthropic 오류: {str(e)}"

        elif provider == "Gemini" and self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                # Gemini usage metadata might vary, but usually response.usage_metadata
                try:
                    tokens = response.usage_metadata.total_token_count
                    add_token_usage("Gemini", tokens)
                except:
                    pass
                return response.text
            except Exception as e:
                return f"Gemini 오류: {str(e)}"
        
        return "오류: 선택된 AI 엔진의 API 키가 설정되지 않았습니다."

    def draft_response(self, mode, context, template_type=None, target_domain=None):
        self._initialize_clients()
        provider = self.settings.get("ai_provider", "OpenAI")
        
        # 텍스트 최적화
        context = self._optimize_text(context)[:4000]
        
        company_info = f"회사명: {self.settings['company_name']}\n담당자: {self.settings['contact_name']}\n제품: {self.settings['product_description']}"
        mode_str = "인바운드" if mode == "inbound" else "아웃바운드"
        domain_str = f"- 대상 도메인/산업군: {target_domain}" if target_domain else ""
        
        # Category specific instructions
        category_instruction = ""
        if template_type:
            if "가격" in template_type:
                category_instruction = "단순 가격 안내를 넘어, 제품의 가성비와 도입 시 얻을 수 있는 ROI(투자 대비 효과)를 강조해 주세요."
            elif "크레딧" in template_type or "결제" in template_type:
                category_instruction = "결제 주기, 크레딧 차감 정책, 환불 규정 등 정책적인 부분을 명확하고 신뢰감 있게 설명해 주세요."
            elif "기능" in template_type or "스펙" in template_type:
                category_instruction = "기술적인 사양뿐만 아니라, 실제 비즈니스 현장에서 어떻게 활용될 수 있는지 Use Case 중심으로 설명해 주세요."
            elif "기술 지원" in template_type or "장애" in template_type:
                category_instruction = "불편에 대한 깊은 공감을 먼저 표하고, 해결 프로세스와 빠른 조치 의지를 보여주어 안심시켜 주세요."

        prompt = f"""영업 AI로서 최적의 영업 메시지를 작성해 주세요.

[우리 회사]
{company_info}

[상황]
- 모드: {mode_str} ({template_type or "일반"})
{domain_str}
- 고객 상황: {context}

[요청]
1. 정중한 한국어 비즈니스 톤.
2. {category_instruction}
3. {f"{target_domain} 산업군의 특성을 고려한" if target_domain else "핵심"} 소구 포인트 포함.
4. 바로 복사 가능한 형태."""

        if provider == "OpenAI" and self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                add_token_usage("OpenAI", response.usage.total_tokens)
                return response.choices[0].message.content
            except Exception as e:
                return f"OpenAI 오류: {str(e)}"
        
        elif provider == "Anthropic" and self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                add_token_usage("Anthropic", response.usage.input_tokens + response.usage.output_tokens)
                return response.content[0].text
            except Exception as e:
                return f"Anthropic 오류: {str(e)}"

        elif provider == "Gemini" and self.gemini_model:
            try:
                response = self.gemini_model.generate_content(prompt)
                try:
                    tokens = response.usage_metadata.total_token_count
                    add_token_usage("Gemini", tokens)
                except:
                    pass
                return response.text
            except Exception as e:
                return f"Gemini 오류: {str(e)}"
        
        return "오류: 선택된 AI 엔진의 API 키가 설정되지 않았습니다."
