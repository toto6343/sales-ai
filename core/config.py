import json
import os
import sys

def get_base_dir():
    # PyInstaller로 빌드된 경우 실행 파일(.exe)의 위치를 반환
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # 일반 스크립트 실행인 경우 프로젝트 루트 위치를 반환
    return os.path.dirname(os.path.dirname(__file__))

SETTINGS_FILE = os.path.join(get_base_dir(), "settings.json")

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "openai_api_key": "",
            "company_name": "",
            "contact_name": "",
            "product_description": "",
            "notion_api_key": "",
            "notion_database_id": "",
            "stats": {"leads": 0, "inquiries": 0, "notion_syncs": 0},
            "token_usage": {"OpenAI": 0, "Anthropic": 0, "Gemini": 0}
        }
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        # 누락된 키가 있으면 기본값 추가
        default_keys = {
            "openai_api_key": "", "company_name": "", "contact_name": "", 
            "product_description": "", "notion_api_key": "", "notion_database_id": "",
            "stats": {"leads": 0, "inquiries": 0, "notion_syncs": 0},
            "token_usage": {"OpenAI": 0, "Anthropic": 0, "Gemini": 0}
        }
        for key, value in default_keys.items():
            if key not in data:
                data[key] = value
        
        # Ensure token_usage has all providers
        if "token_usage" not in data:
            data["token_usage"] = {"OpenAI": 0, "Anthropic": 0, "Gemini": 0}
        else:
            for provider in ["OpenAI", "Anthropic", "Gemini"]:
                if provider not in data["token_usage"]:
                    data["token_usage"][provider] = 0
                    
        return data

def increment_stat(stat_name):
    settings = load_settings()
    if "stats" in settings:
        settings["stats"][stat_name] = settings["stats"].get(stat_name, 0) + 1
        save_settings(settings)

def add_token_usage(provider, tokens):
    settings = load_settings()
    if "token_usage" not in settings:
        settings["token_usage"] = {"OpenAI": 0, "Anthropic": 0, "Gemini": 0}
    
    settings["token_usage"][provider] = settings["token_usage"].get(provider, 0) + tokens
    save_settings(settings)

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)
