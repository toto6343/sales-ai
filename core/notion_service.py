import requests
import json
from .config import load_settings, increment_stat

class NotionService:
    def __init__(self):
        self.settings = load_settings()
        self.headers = {
            "Authorization": f"Bearer {self.settings.get('notion_api_key')}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def add_lead(self, title, description):
        self.settings = load_settings()
        database_id = self.settings.get("notion_database_id")
        if not database_id or not self.settings.get("notion_api_key"):
            return False, "노션 API 키 또는 데이터베이스 ID가 설정되지 않았습니다."

        url = "https://api.notion.com/v1/pages"
        
        # Simple schema: Name and Description (Text)
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "이름": {
                    "title": [
                        {"text": {"content": title}}
                    ]
                },
                "내용": {
                    "rich_text": [
                        {"text": {"content": description[:2000]}} # Notion limit
                    ]
                }
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(data))
            if response.status_code == 200:
                increment_stat("notion_syncs")
                return True, "노션에 성공적으로 저장되었습니다."
            else:
                return False, f"노션 저장 실패: {response.text}"
        except Exception as e:
            return False, f"오류 발생: {str(e)}"
