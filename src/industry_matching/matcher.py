from typing import Dict, List, Any
import json
from ..ai_client import get_ai_client

class IndustryMatcher:
    def __init__(self, ai_model: str = "claude"):
        self.ai_client = get_ai_client(ai_model)
        self.industries = [
            "コンサルティング",
            "IT・ソフトウェア", 
            "金融・銀行",
            "メーカー・製造業",
            "商社・流通",
            "インフラ・公共",
            "メディア・広告",
            "医療・ヘルスケア",
            "不動産・建設",
            "教育・研究"
        ]
    
    def analyze_fit(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """ユーザープロフィールを基に業界適性を分析"""
        
        system_prompt = """
あなたは就活生の業界適性を分析する専門家です。
学生の経験、スキル、価値観を基に、どの業界が適しているかを分析してください。

以下の業界を対象に分析してください：
- コンサルティング
- IT・ソフトウェア
- 金融・銀行
- メーカー・製造業
- 商社・流通
- インフラ・公共
- メディア・広告
- 医療・ヘルスケア
- 不動産・建設
- 教育・研究

各業界について適性度を1-10で評価し、理由も含めて回答してください。
結果はJSONフォーマットで返してください。
"""
        
        prompt = f"""
学生プロフィール:
{json.dumps(user_profile, ensure_ascii=False, indent=2)}

上記のプロフィールを基に、業界適性を分析してください。

期待する出力フォーマット:
{{
    "overall_assessment": "総合的な評価コメント",
    "industry_scores": {{
        "業界名": {{
            "score": 8,
            "reason": "適性が高い理由",
            "recommended_roles": ["おすすめ職種1", "おすすめ職種2"]
        }}
    }},
    "top_recommendations": ["最適業界1", "最適業界2", "最適業界3"]
}}
"""
        
        try:
            response = self.ai_client.generate_response(prompt, system_prompt)
            # JSONの解析を試行
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                # JSON解析に失敗した場合はテキストレスポンスを返す
                return {"raw_response": response, "status": "text_response"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def get_industry_info(self, industry_name: str) -> Dict[str, Any]:
        """特定業界の詳細情報を取得"""
        
        prompt = f"""
{industry_name}業界について、就活生向けに以下の情報を提供してください：

1. 業界の特徴と動向
2. 求められる人材像
3. 主要企業
4. 平均年収レンジ
5. キャリアパス
6. 業界の将来性
7. 入社後の業務内容例

JSONフォーマットで回答してください。
"""
        
        try:
            response = self.ai_client.generate_response(prompt)
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {"raw_response": response, "status": "text_response"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def generate_motivation_template(self, industry_name: str, user_strengths: List[str]) -> str:
        """業界向けの志望動機テンプレートを生成"""
        
        prompt = f"""
{industry_name}業界志望の学生向けに、志望動機のテンプレートを作成してください。

学生の強み:
{', '.join(user_strengths)}

以下の構成で作成してください：
1. 業界への関心のきっかけ
2. 業界の魅力・将来性への言及
3. 自分の強みと業界への貢献
4. 具体的な目標・やりたいこと

400文字程度でお願いします。
"""
        
        return self.ai_client.generate_response(prompt)