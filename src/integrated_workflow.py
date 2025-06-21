from typing import Dict, Any, Optional, List
import json
from .company_analysis.analyzer import CompanyAnalyzer
from .personality_analysis.analyzer import PersonalityAnalyzer
from .essay_generation.generator import EssayGenerator
from .interview_prep.prep import InterviewPrep

class IntegratedWorkflow:
    """企業分析から始まる統合ワークフロー管理"""
    
    def __init__(self, ai_model: str = "claude"):
        self.company_analyzer = CompanyAnalyzer(ai_model)
        self.personality_analyzer = PersonalityAnalyzer(ai_model)
        self.essay_generator = EssayGenerator(ai_model)
        self.interview_prep = InterviewPrep(ai_model)
        
        # ワークフローの状態管理
        self.workflow_state = {
            "company_analysis": None,
            "required_personality": None,
            "user_personality": None,
            "gap_analysis": None,
            "generated_essays": {},
            "interview_preparation": None
        }
    
    def start_workflow(self, company_name: str) -> Dict[str, Any]:
        """Step 1: 企業分析からワークフローを開始"""
        try:
            # 企業分析実行
            company_analysis = self.company_analyzer.analyze(company_name)
            
            if company_analysis.get("status") == "success":
                self.workflow_state["company_analysis"] = company_analysis
                
                # 企業が求める人物像を分析
                required_personality = self.personality_analyzer.analyze_required_personality(company_analysis)
                self.workflow_state["required_personality"] = required_personality
                
                return {
                    "status": "success",
                    "step": "company_analysis_completed",
                    "company_analysis": company_analysis,
                    "required_personality": required_personality,
                    "next_step": "user_personality_definition"
                }
            else:
                return company_analysis
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def define_user_personality(self, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Step 2: ユーザーのパーソナリティを定義"""
        try:
            if not self.workflow_state["company_analysis"]:
                return {"status": "error", "error": "企業分析を先に実行してください"}
            
            # user_infoが提供されていない場合、セッション状態から取得を試みる
            if user_info is None:
                try:
                    import streamlit as st
                    if hasattr(st, 'session_state') and 'user_profile' in st.session_state:
                        profile = st.session_state.user_profile
                        user_info = {
                            "name": profile.get('name', ''),
                            "university": f"{profile.get('university', '')} {profile.get('faculty', '')} {profile.get('department', '')}".strip(),
                            "graduation_year": profile.get('graduation_year', ''),
                            "club_activities": profile.get('club_activities', ''),
                            "part_time_job": profile.get('part_time_job', ''),
                            "internship": profile.get('internship', ''),
                            "gakuchika": profile.get('gakuchika', ''),
                            "strengths": profile.get('strengths', ''),
                            "values": profile.get('values', ''),
                            "career_goals": profile.get('career_goals', ''),
                            "target_industries": ', '.join(profile.get('target_industries', [])),
                            "job_types": ', '.join(profile.get('job_types', []))
                        }
                    else:
                        return {"status": "error", "error": "ユーザープロフィール情報が見つかりません"}
                except ImportError:
                    return {"status": "error", "error": "ユーザー情報を提供してください"}
            
            # ユーザーパーソナリティ分析
            user_personality = self.personality_analyzer.define_user_personality(user_info)
            self.workflow_state["user_personality"] = user_personality
            
            return {
                "status": "success",
                "step": "user_personality_defined",
                "user_personality": user_personality,
                "next_step": "gap_analysis"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def analyze_personality_gap(self) -> Dict[str, Any]:
        """Step 3: パーソナリティギャップ分析"""
        try:
            if not self.workflow_state["user_personality"] or not self.workflow_state["required_personality"]:
                return {"status": "error", "error": "ユーザーパーソナリティと企業要求パーソナリティの両方が必要です"}
            
            # ギャップ分析実行
            gap_analysis = self.personality_analyzer.analyze_personality_gap(
                self.workflow_state["user_personality"],
                self.workflow_state["required_personality"]
            )
            self.workflow_state["gap_analysis"] = gap_analysis
            
            return {
                "status": "success",
                "step": "gap_analysis_completed",
                "gap_analysis": gap_analysis,
                "next_step": "essay_generation"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_tailored_essays(self) -> Dict[str, Any]:
        """Step 4: ギャップ分析を踏まえたES生成"""
        try:
            if not self.workflow_state["gap_analysis"]:
                return {"status": "error", "error": "ギャップ分析を先に実行してください"}
            
            company_name = self.workflow_state["company_analysis"].get("company_name", "")
            user_info = self.workflow_state["user_personality"]
            gap_analysis = self.workflow_state["gap_analysis"]
            
            # 改善されたユーザー情報を作成
            enhanced_user_info = self._create_enhanced_user_info(user_info, gap_analysis)
            
            # 自己PR生成
            self_pr = self.essay_generator.generate_self_pr(enhanced_user_info, company_name)
            
            # 志望動機生成
            motivation = self.essay_generator.generate_motivation_letter(
                self.workflow_state["company_analysis"],
                enhanced_user_info
            )
            
            essays = {
                "self_pr": self_pr,
                "motivation": motivation
            }
            
            self.workflow_state["generated_essays"] = essays
            
            return {
                "status": "success",
                "step": "essays_generated",
                "essays": essays,
                "next_step": "interview_preparation"
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def prepare_interview_strategy(self) -> Dict[str, Any]:
        """Step 5: 面接戦略準備"""
        try:
            if not self.workflow_state["gap_analysis"]:
                return {"status": "error", "error": "ギャップ分析が必要です"}
            
            company_name = self.workflow_state["company_analysis"].get("company_name", "")
            company_info = self.workflow_state["company_analysis"]
            gap_analysis = self.workflow_state["gap_analysis"]
            
            # 企業・業界特化の想定質問生成
            questions = self.interview_prep.generate_questions(
                company_name, 
                company_info.get("basic_info", {}).get("industry", ""), 
                "総合職"
            )
            
            # ギャップ分析に基づく面接戦略
            interview_strategy = gap_analysis.get("interview_strategy", {})
            
            # パーソナリティ改善プラン
            development_plan = self.personality_analyzer.generate_personality_development_plan(
                gap_analysis, company_name
            )
            
            interview_preparation = {
                "questions": questions,
                "strategy": interview_strategy,
                "development_plan": development_plan,
                "key_points": self._extract_interview_key_points(gap_analysis)
            }
            
            self.workflow_state["interview_preparation"] = interview_preparation
            
            return {
                "status": "success",
                "step": "interview_preparation_completed",
                "interview_preparation": interview_preparation,
                "workflow_completed": True
            }
            
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_complete_workflow_summary(self) -> Dict[str, Any]:
        """完全なワークフロー結果のサマリー"""
        return {
            "workflow_summary": {
                "company_analysis": self.workflow_state["company_analysis"],
                "required_personality": self.workflow_state["required_personality"],
                "user_personality": self.workflow_state["user_personality"],
                "gap_analysis": self.workflow_state["gap_analysis"],
                "generated_essays": self.workflow_state["generated_essays"],
                "interview_preparation": self.workflow_state["interview_preparation"]
            },
            "status": "completed" if self._is_workflow_complete() else "in_progress"
        }
    
    def _create_enhanced_user_info(self, user_info: Dict, gap_analysis: Dict) -> Dict[str, Any]:
        """ギャップ分析に基づいてユーザー情報を強化"""
        enhanced_info = user_info.copy()
        
        # ギャップ分析から強みをアピールポイントとして追加
        if "gap_analysis" in gap_analysis and "strengths_match" in gap_analysis["gap_analysis"]:
            strengths_match = gap_analysis["gap_analysis"]["strengths_match"]
            enhanced_info["highlighted_strengths"] = [item.get("description", "") for item in strengths_match]
        
        # 改善提案をエピソードとして追加
        if "improvement_plan" in gap_analysis and "immediate_actions" in gap_analysis["improvement_plan"]:
            actions = gap_analysis["improvement_plan"]["immediate_actions"]
            enhanced_info["improvement_actions"] = [action.get("action", "") for action in actions]
        
        return enhanced_info
    
    def _extract_interview_key_points(self, gap_analysis: Dict) -> List[str]:
        """ギャップ分析から面接の重要ポイントを抽出"""
        key_points = []
        
        if "interview_strategy" in gap_analysis:
            strategy = gap_analysis["interview_strategy"]
            
            if "highlight_strengths" in strategy:
                key_points.extend([f"強みとしてアピール: {strength}" for strength in strategy["highlight_strengths"]])
            
            if "address_gaps" in strategy:
                key_points.extend([f"ギャップ対処法: {gap}" for gap in strategy["address_gaps"]])
        
        return key_points
    
    def _is_workflow_complete(self) -> bool:
        """ワークフローが完了しているかチェック"""
        required_steps = [
            "company_analysis",
            "required_personality", 
            "user_personality",
            "gap_analysis",
            "generated_essays",
            "interview_preparation"
        ]
        
        return all(self.workflow_state.get(step) is not None for step in required_steps)