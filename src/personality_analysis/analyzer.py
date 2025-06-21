from typing import Dict, List, Any
import json
from ..ai_client import get_ai_client

class PersonalityAnalyzer:
    def __init__(self, ai_model: str = "claude"):
        self.ai_client = get_ai_client(ai_model)
        
    def analyze_required_personality(self, company_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """企業分析結果から求められる人物像を分析"""
        
        system_prompt = """
あなたは人事コンサルタントです。
企業の分析結果を基に、その企業が求める人物像・パーソナリティを詳細に分析してください。

以下の観点で分析を行ってください：
1. 価値観・考え方
2. 行動特性
3. スキル・能力
4. コミュニケーションスタイル
5. リーダーシップスタイル
6. 問題解決アプローチ
7. 学習・成長志向
8. チームワーク・協調性

結果はJSONフォーマットで返してください。
"""
        
        prompt = f"""
企業分析結果:
{json.dumps(company_analysis, ensure_ascii=False, indent=2)}

上記の企業分析を基に、この企業が求める理想的な人物像・パーソナリティを分析してください。

期待する出力フォーマット:
{{
    "company_name": "企業名",
    "required_personality": {{
        "values": ["価値観1", "価値観2", "価値観3"],
        "behavioral_traits": ["行動特性1", "行動特性2", "行動特性3"],
        "skills": ["必要スキル1", "必要スキル2", "必要スキル3"],
        "communication_style": "コミュニケーションスタイルの説明",
        "leadership_style": "リーダーシップスタイルの説明",
        "problem_solving": "問題解決アプローチの説明",
        "growth_mindset": "学習・成長に対する姿勢",
        "teamwork": "チームワークの重要性と特徴"
    }},
    "key_interview_points": [
        "面接で重視されるポイント1",
        "面接で重視されるポイント2", 
        "面接で重視されるポイント3"
    ],
    "success_factors": [
        "この企業で成功する要因1",
        "この企業で成功する要因2",
        "この企業で成功する要因3"
    ]
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
    
    def define_user_personality(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """ユーザー情報から現在のパーソナリティを定義"""
        
        system_prompt = """
あなたは心理学・人事評価の専門家です。
ユーザーの経験、強み、価値観などの情報を基に、そのユーザーの現在のパーソナリティプロフィールを作成してください。

以下の観点で分析してください：
1. 価値観・考え方の傾向
2. 行動パターン・特性
3. 現在のスキル・能力
4. コミュニケーションの傾向
5. リーダーシップの発揮方法
6. 問題解決のアプローチ
7. 学習・成長への取り組み方
8. チームでの役割・貢献方法

客観的で建設的な分析を行ってください。
"""
        
        prompt = f"""
ユーザー情報:
{json.dumps(user_info, ensure_ascii=False, indent=2)}

上記の情報を基に、このユーザーの現在のパーソナリティプロフィールを作成してください。

期待する出力フォーマット:
{{
    "current_personality": {{
        "values": ["現在の価値観1", "現在の価値観2", "現在の価値観3"],
        "behavioral_traits": ["行動特性1", "行動特性2", "行動特性3"],
        "skills": ["現在のスキル1", "現在のスキル2", "現在のスキル3"],
        "communication_style": "コミュニケーションスタイルの説明",
        "leadership_style": "リーダーシップスタイルの説明",
        "problem_solving": "問題解決アプローチの説明",
        "growth_mindset": "学習・成長に対する姿勢",
        "teamwork": "チームワークでの役割・貢献"
    }},
    "strengths": [
        "強み1の詳細説明",
        "強み2の詳細説明",
        "強み3の詳細説明"
    ],
    "development_areas": [
        "成長領域1",
        "成長領域2",
        "成長領域3"
    ],
    "personality_summary": "総合的なパーソナリティの特徴説明"
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
    
    def analyze_personality_gap(self, user_personality: Dict, required_personality: Dict) -> Dict[str, Any]:
        """ユーザーのパーソナリティと企業要求のギャップ分析"""
        
        system_prompt = """
あなたは人事・キャリアコンサルタントです。
ユーザーの現在のパーソナリティと企業が求めるパーソナリティを比較分析し、
ギャップを特定して具体的な改善提案を行ってください。

分析観点：
1. 一致している点（強み）
2. ギャップがある点（改善領域）
3. 具体的な改善アクション
4. 面接での対策・アピール方法
5. 中長期的な成長プラン
"""
        
        prompt = f"""
ユーザーの現在のパーソナリティ:
{json.dumps(user_personality, ensure_ascii=False, indent=2)}

企業が求めるパーソナリティ:
{json.dumps(required_personality, ensure_ascii=False, indent=2)}

上記を比較分析して、ギャップ分析と改善提案を行ってください。

期待する出力フォーマット:
{{
    "gap_analysis": {{
        "strengths_match": [
            {{
                "area": "一致領域1",
                "description": "詳細説明",
                "interview_appeal": "面接でのアピール方法"
            }}
        ],
        "gaps_identified": [
            {{
                "area": "ギャップ領域1", 
                "current_state": "現在の状態",
                "required_state": "求められる状態",
                "gap_severity": "high/medium/low"
            }}
        ]
    }},
    "improvement_plan": {{
        "immediate_actions": [
            {{
                "action": "すぐに取り組むべき行動1",
                "timeline": "期間",
                "method": "具体的な方法"
            }}
        ],
        "medium_term_goals": [
            {{
                "goal": "中期目標1",
                "timeline": "期間", 
                "steps": ["ステップ1", "ステップ2"]
            }}
        ],
        "long_term_development": [
            "長期的な成長方向性1",
            "長期的な成長方向性2"
        ]
    }},
    "interview_strategy": {{
        "highlight_strengths": ["アピールすべき強み1", "アピールすべき強み2"],
        "address_gaps": ["ギャップへの対処法1", "ギャップへの対処法2"],
        "sample_responses": [
            {{
                "question": "想定質問1",
                "response_approach": "回答アプローチ"
            }}
        ]
    }},
    "overall_fit_score": "70",
    "fit_assessment": "適合度の総合評価コメント"
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
    
    def generate_personality_development_plan(self, gap_analysis: Dict[str, Any], company_name: str) -> str:
        """パーソナリティ改善のための具体的なアクションプランを生成"""
        
        prompt = f"""
以下のギャップ分析結果を基に、{company_name}への転職・就職を目指す人向けの
具体的なパーソナリティ改善プランを作成してください。

ギャップ分析結果:
{json.dumps(gap_analysis, ensure_ascii=False, indent=2)}

以下の構成で実践的なプランを作成してください：
1. 改善の優先順位
2. 具体的なアクションプラン（30日、90日、180日）
3. 日常的な習慣・行動の変更提案
4. 学習・スキルアップの推奨
5. 実践練習の方法
6. 進捗確認・測定方法

実行可能で具体的な内容にしてください。
"""
        
        return self.ai_client.generate_response(prompt)