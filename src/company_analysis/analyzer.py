import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any, List
import re
from ..ai_client import get_ai_client

class CompanyAnalyzer:
    def __init__(self, ai_model: str = "claude"):
        self.ai_client = get_ai_client(ai_model)
        
    def analyze(self, company_name: str) -> Dict[str, Any]:
        """企業の総合分析を実行"""
        try:
            # 1. 企業の基本情報を取得
            company_info = self._fetch_company_info(company_name)
            
            # 2. IR情報を取得
            ir_data = self._fetch_ir_data(company_name)
            
            # 3. AIで分析
            analysis = self._analyze_with_ai(company_name, company_info, ir_data)
            
            return {
                "company_name": company_name,
                "basic_info": company_info,
                "ir_summary": ir_data,
                "ai_analysis": analysis,
                "status": "success"
            }
        except Exception as e:
            return {
                "company_name": company_name,
                "error": str(e),
                "status": "error"
            }
    
    def _fetch_company_info(self, company_name: str) -> Dict[str, str]:
        """企業の基本情報を取得（簡易実装）"""
        # 実際のプロダクションでは企業データベースAPIを使用
        return {
            "name": company_name,
            "industry": "分析中...",
            "description": "企業情報を取得中..."
        }
    
    def _fetch_ir_data(self, company_name: str) -> Dict[str, Any]:
        """IR情報を取得（モックデータ）"""
        # 実際の実装では上場企業のIR情報をスクレイピング
        mock_data = {
            "revenue_trend": "売上高: 増加傾向",
            "profit_trend": "営業利益: 安定",
            "key_initiatives": [
                "DX推進",
                "海外展開",
                "サステナビリティ強化"
            ],
            "challenges": [
                "人材確保",
                "競争激化",
                "コスト上昇"
            ]
        }
        return mock_data
    
    def _analyze_with_ai(self, company_name: str, company_info: Dict, ir_data: Dict) -> str:
        """AIを使用して企業分析を実行"""
        system_prompt = """
あなたは就活生向けの企業分析の専門家です。
提供された企業情報とIR情報を基に、以下の観点で分析してください：

1. 企業の強み・競争優位性
2. 事業戦略と成長分野
3. 業界内でのポジション
4. 直近の課題と対応策
5. 就活生が注目すべきポイント

分析結果は構造化されたJSONフォーマットで返してください。
"""
        
        prompt = f"""
企業名: {company_name}

基本情報:
{json.dumps(company_info, ensure_ascii=False, indent=2)}

IR情報:
{json.dumps(ir_data, ensure_ascii=False, indent=2)}

上記の情報を基に、就活生向けの企業分析を実行してください。
"""
        
        return self.ai_client.generate_response(prompt, system_prompt)
    
    def get_interview_points(self, company_name: str) -> List[str]:
        """面接で聞かれそうなポイントを抽出"""
        analysis_result = self.analyze(company_name)
        
        prompt = f"""
以下の企業分析結果を基に、面接で聞かれる可能性が高い質問を5つ生成してください：

企業分析結果:
{json.dumps(analysis_result, ensure_ascii=False, indent=2)}

例：
- 当社の強みは何だと思いますか？
- なぜ当社を志望するのですか？
- 当社の課題をどう解決したいですか？

リスト形式で回答してください。
"""
        
        response = self.ai_client.generate_response(prompt)
        # 簡易的な解析（実際はより堅牢な実装が必要）
        questions = [line.strip() for line in response.split('\n') if line.strip() and line.strip().startswith('-')]
        return questions[:5]