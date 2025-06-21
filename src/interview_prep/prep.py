from typing import Dict, List, Any, Tuple
import json
import random
from ..ai_client import get_ai_client

class InterviewPrep:
    def __init__(self, ai_model: str = "claude"):
        self.ai_client = get_ai_client(ai_model)
        
        # 基本的な面接質問カテゴリ
        self.question_categories = {
            "自己紹介・自己PR": [
                "自己紹介をお願いします",
                "あなたの強みは何ですか？",
                "あなたの弱みは何ですか？",
                "学生時代に最も力を入れたことは？"
            ],
            "志望動機・企業理解": [
                "なぜ当社を志望するのですか？",
                "なぜこの業界を選んだのですか？",
                "当社の事業内容について説明してください",
                "当社の強みは何だと思いますか？"
            ],
            "キャリア・将来": [
                "10年後の自分はどうなっていたいですか？",
                "当社でやりたい仕事は何ですか？",
                "キャリアプランを教えてください"
            ],
            "価値観・性格": [
                "チームワークで大切にしていることは？",
                "困難な状況をどう乗り越えますか？",
                "リーダーシップを発揮した経験は？"
            ]
        }
    
    def generate_questions(self, company_name: str, industry: str, job_type: str = "総合職") -> List[Dict[str, Any]]:
        """企業・業界別の想定質問を生成"""
        
        system_prompt = """
あなたは人事面接官の専門家です。
企業情報を基に、その企業の面接で実際に聞かれそうな質問を生成してください。

質問カテゴリ：
1. 基本質問（自己PR、志望動機など）
2. 企業固有質問（その企業の事業や戦略に関する質問）
3. 業界理解質問
4. 状況対応質問（ケース面接的な要素）
5. 価値観・カルチャーフィット確認質問

各カテゴリから2-3問ずつ、計15問程度生成してください。
"""
        
        prompt = f"""
企業名: {company_name}
業界: {industry}
職種: {job_type}

上記の企業の面接で聞かれる可能性が高い質問を生成してください。

JSONフォーマットで回答：
{{
    "basic_questions": ["質問1", "質問2"],
    "company_specific": ["質問1", "質問2"],
    "industry_questions": ["質問1", "質問2"],
    "situational": ["質問1", "質問2"],
    "culture_fit": ["質問1", "質問2"]
}}
"""
        
        try:
            response = self.ai_client.generate_response(prompt, system_prompt)
            try:
                result = json.loads(response)
                # フラットなリストに変換
                all_questions = []
                for category, questions in result.items():
                    for q in questions:
                        all_questions.append({
                            "question": q,
                            "category": category,
                            "difficulty": self._assess_difficulty(q)
                        })
                return all_questions
            except json.JSONDecodeError:
                # フォールバック: 基本質問を返す
                return self._get_basic_questions()
        except Exception as e:
            return [{"error": str(e), "status": "error"}]
    
    def generate_answer_template(self, question: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """質問に対する回答テンプレートを生成"""
        
        system_prompt = """
あなたは面接対策の専門家です。
面接質問に対して、学生のプロフィールを基に効果的な回答例を作成してください。

回答の構成：
1. 結論ファースト
2. 具体的なエピソード
3. 学んだこと・成長
4. 企業での活かし方（志望動機系の場合）

STAR法（Situation, Task, Action, Result）を意識した構成にしてください。
"""
        
        prompt = f"""
面接質問: {question}

学生プロフィール:
{json.dumps(user_profile, ensure_ascii=False, indent=2)}

上記の質問に対する効果的な回答例を作成してください。
回答時間は1-2分程度を想定してください。

JSONフォーマットで回答：
{{
    "answer_template": "回答例",
    "key_points": ["アピールポイント1", "アピールポイント2"],
    "tips": ["回答時のコツ1", "回答時のコツ2"],
    "avoid": ["避けるべき表現や内容"]
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
    
    def mock_interview_session(self, questions: List[str], user_answers: List[str]) -> Dict[str, Any]:
        """模擬面接セッション（回答評価とフィードバック）"""
        
        feedback_list = []
        
        for i, (question, answer) in enumerate(zip(questions, user_answers)):
            feedback = self._evaluate_answer(question, answer)
            feedback_list.append({
                "question_no": i + 1,
                "question": question,
                "answer": answer,
                "feedback": feedback
            })
        
        overall_assessment = self._generate_overall_assessment(feedback_list)
        
        return {
            "individual_feedback": feedback_list,
            "overall_assessment": overall_assessment,
            "improvement_areas": self._identify_improvement_areas(feedback_list)
        }
    
    def _evaluate_answer(self, question: str, answer: str) -> Dict[str, Any]:
        """個別回答の評価"""
        
        prompt = f"""
面接質問: {question}
学生の回答: {answer}

以下の観点で回答を評価してください（各項目1-10点）：
1. 質問への適切性
2. 具体性・エピソードの充実
3. 論理性・構成
4. 熱意・表現力
5. 独自性・差別化

総合評価と改善提案もお願いします。

JSONフォーマットで回答してください。
"""
        
        try:
            response = self.ai_client.generate_response(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"raw_feedback": response}
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_overall_assessment(self, feedback_list: List[Dict]) -> str:
        """全体的な評価コメント生成"""
        
        prompt = f"""
模擬面接の結果を基に、全体的な評価とアドバイスを生成してください：

面接結果:
{json.dumps(feedback_list, ensure_ascii=False, indent=2)}

以下の形式で回答してください：
- 全体的な印象（良い点）
- 改善すべき点
- 次回面接に向けたアドバイス
"""
        
        return self.ai_client.generate_response(prompt)
    
    def _identify_improvement_areas(self, feedback_list: List[Dict]) -> List[str]:
        """改善領域の特定"""
        
        improvement_areas = []
        
        # 簡易的な分析（実際はより詳細な分析が必要）
        common_issues = [
            "具体性の不足",
            "構成の改善",
            "企業研究の深堀り",
            "表現力の向上"
        ]
        
        return random.sample(common_issues, 2)
    
    def _assess_difficulty(self, question: str) -> str:
        """質問の難易度評価"""
        
        if any(word in question for word in ["なぜ", "理由", "どう思う", "説明"]):
            return "高"
        elif any(word in question for word in ["経験", "エピソード", "具体的"]):
            return "中"
        else:
            return "低"
    
    def _get_basic_questions(self) -> List[Dict[str, Any]]:
        """基本的な面接質問を返す（フォールバック用）"""
        
        basic_questions = [
            {"question": "自己紹介をお願いします", "category": "basic", "difficulty": "低"},
            {"question": "なぜ当社を志望するのですか？", "category": "motivation", "difficulty": "高"},
            {"question": "あなたの強みは何ですか？", "category": "self_pr", "difficulty": "中"},
            {"question": "学生時代に最も力を入れたことは？", "category": "experience", "difficulty": "中"},
            {"question": "10年後の自分はどうなっていたいですか？", "category": "career", "difficulty": "高"}
        ]
        
        return basic_questions