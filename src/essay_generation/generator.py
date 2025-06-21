from typing import Dict, List, Any
import json
from ..ai_client import get_ai_client

class EssayGenerator:
    def __init__(self, ai_model: str = "claude"):
        self.ai_client = get_ai_client(ai_model)
    
    def generate_self_pr(self, user_info: Dict[str, Any], target_company: str = None) -> Dict[str, Any]:
        """自己PR文を生成"""
        
        system_prompt = """
あなたは就活ESの自己PR作成専門家です。
学生の経験や強みを基に、魅力的で具体的な自己PR文を作成してください。

自己PRの構成：
1. 結論（強み・アピールポイント）
2. 具体的なエピソード（STAR法推奨）
3. 学んだこと・成長した点
4. 企業でどう活かすか

400文字程度で作成してください。
"""
        
        company_context = f"対象企業: {target_company}\n" if target_company else ""
        
        prompt = f"""
{company_context}学生情報:
{json.dumps(user_info, ensure_ascii=False, indent=2)}

上記の情報を基に、魅力的な自己PR文を作成してください。
"""
        
        try:
            response = self.ai_client.generate_response(prompt, system_prompt)
            return {
                "self_pr": response,
                "status": "success"
            }
        except Exception as e:
            return {
                "error": str(e),
                "status": "error"
            }
    
    def improve_essay(self, essay_text: str, essay_type: str = "自己PR") -> Dict[str, Any]:
        """ES文章の改善提案"""
        
        system_prompt = """
あなたは就活ESの添削専門家です。
提出されたES文章を以下の観点で評価し、改善提案を行ってください：

評価観点：
1. 構成・論理性 (1-10点)
2. 具体性・エピソードの充実度 (1-10点)
3. 独自性・差別化 (1-10点)
4. 企業への志望度の伝わりやすさ (1-10点)
5. 文章力・読みやすさ (1-10点)

改善提案：
- 具体的な修正箇所の指摘
- より良い表現の提案
- 追加すべき要素の提案
"""
        
        prompt = f"""
ES種類: {essay_type}

提出文章:
{essay_text}

上記の文章を評価し、改善提案を行ってください。
JSONフォーマットで回答してください：

{{
    "scores": {{
        "structure": 8,
        "specificity": 7,
        "uniqueness": 6,
        "motivation": 8,
        "writing": 9
    }},
    "total_score": 38,
    "improvements": [
        {{
            "category": "構成",
            "issue": "問題点",
            "suggestion": "改善提案"
        }}
    ],
    "revised_text": "改善版の文章"
}}
"""
        
        try:
            response = self.ai_client.generate_response(prompt, system_prompt)
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                return {"raw_response": response, "status": "text_response"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def generate_motivation_letter(self, company_info: Dict, user_info: Dict) -> str:
        """志望動機を生成"""
        
        prompt = f"""
以下の情報を基に、説得力のある志望動機を作成してください：

企業情報:
{json.dumps(company_info, ensure_ascii=False, indent=2)}

学生情報:
{json.dumps(user_info, ensure_ascii=False, indent=2)}

構成:
1. 業界・企業への関心のきっかけ
2. 企業の魅力・共感した点
3. 自分の経験・強みと企業での活かし方
4. 入社後の目標・やりたいこと

400文字程度で作成してください。
"""
        
        return self.ai_client.generate_response(prompt)
    
    def get_essay_templates(self) -> Dict[str, str]:
        """ES文章のテンプレート集を提供"""
        
        templates = {
            "自己PR": """
【結論】私の強みは○○です。

【エピソード】大学時代に○○に取り組み、○○という課題に直面しました。この課題に対し、○○の方法でアプローチし、○○という成果を上げることができました。

【学び】この経験から○○を学び、○○という能力を身につけました。

【企業での活用】この強みを貴社の○○業務において活かし、○○で貢献したいと考えています。
            """,
            
            "志望動機": """
【きっかけ】○○がきっかけで貴社に興味を持ちました。

【企業の魅力】貴社の○○という点に強く共感し、○○という将来性に魅力を感じています。

【自分の強み】私は○○という経験を通じて○○という強みを身につけており、この強みを貴社の○○で活かしたいと考えています。

【入社後の目標】入社後は○○に取り組み、○○という形で貢献していきたいです。
            """,
            
            "学生時代に力を入れたこと": """
【テーマ】学生時代に最も力を入れたことは○○です。

【動機】○○という理由でこの活動に取り組みました。

【課題と取り組み】活動中に○○という課題に直面し、○○という方法で解決に取り組みました。

【成果と学び】結果として○○という成果を上げ、○○を学ぶことができました。
            """
        }
        
        return templates