import streamlit as st
import os
import json
from dotenv import load_dotenv
from src.integrated_workflow import IntegratedWorkflow
from src.company_analysis.analyzer import CompanyAnalyzer
from src.industry_matching.matcher import IndustryMatcher
from src.essay_generation.generator import EssayGenerator
from src.interview_prep.prep import InterviewPrep

load_dotenv()

def main():
    st.set_page_config(
        page_title="就活AIコンパス",
        page_icon="🎯",
        layout="wide"
    )
    
    st.markdown("就活生向けAI支援ツール - 企業分析から始まる一貫した就活支援")
    
    # ワークフロー状態の初期化
    if 'workflow' not in st.session_state:
        st.session_state.workflow = IntegratedWorkflow()
    
    # Sidebar for navigation
    st.sidebar.title("📋 メニュー")
    page = st.sidebar.selectbox(
        "機能選択",
        ["🎯 就活AIコンパス", "👤 プロフィール設定", "❓ ヘルプ"]
    )
    
    if page == "🎯 就活AIコンパス":
        home_page()
    elif page == "👤 プロフィール設定":
        profile_setting_page()
    elif page == "❓ ヘルプ":
        help_page()

def integrated_workflow_page():
    st.header("🎯 統合ワークフロー")
    st.markdown("**企業分析から始まる一貫した就活準備プロセス**")
    
    # プロセス表示
    st.subheader("📋 プロセス概要")
    
    process_steps = [
        "1️⃣ 企業分析 → 企業が求める人物像を特定",
        "2️⃣ パーソナリティ定義 → あなたの現在の特性を分析", 
        "3️⃣ ギャップ分析 → 理想と現実の差を明確化",
        "4️⃣ ES生成 → ギャップを踏まえた最適なES作成",
        "5️⃣ 面接対策 → 戦略的な面接準備"
    ]
    
    for step in process_steps:
        st.write(step)
    
    st.divider()
    
    # Step 1: 企業分析
    st.subheader("1️⃣ 企業分析")
    company_name = st.text_input("🏢 志望企業名を入力してください", key="workflow_company")
    
    if st.button("🔍 企業分析を開始", type="primary"):
        if company_name:
            with st.spinner("企業分析と求める人物像を分析中..."):
                result = st.session_state.workflow.start_workflow(company_name)
                
                if result.get("status") == "success":
                    st.success("✅ 企業分析完了！")
                    
                    # 企業分析結果
                    with st.expander("🏢 企業分析結果", expanded=True):
                        st.json(result["company_analysis"])
                    
                    # 求める人物像
                    with st.expander("👤 この企業が求める人物像", expanded=True):
                        required_personality = result["required_personality"]
                        if "required_personality" in required_personality:
                            personality = required_personality["required_personality"]
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**💭 重視する価値観:**")
                                for value in personality.get("values", []):
                                    st.write(f"• {value}")
                                
                                st.write("**🎯 求める行動特性:**")
                                for trait in personality.get("behavioral_traits", []):
                                    st.write(f"• {trait}")
                            
                            with col2:
                                st.write("**🛠 必要なスキル:**")
                                for skill in personality.get("skills", []):
                                    st.write(f"• {skill}")
                                
                                st.write("**💬 コミュニケーション:**")
                                st.write(personality.get("communication_style", ""))
                        
                        if "key_interview_points" in required_personality:
                            st.write("**❓ 面接重要ポイント:**")
                            for point in required_personality["key_interview_points"]:
                                st.write(f"• {point}")
                    
                    st.session_state.workflow_step = 2
                else:
                    st.error(f"❌ エラー: {result.get('error', '不明なエラー')}")
        else:
            st.error("企業名を入力してください")
    
    # Step 2: パーソナリティ定義
    if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 2:
        st.divider()
        st.subheader("2️⃣ あなたのパーソナリティ定義")
        
        # プロフィール設定の確認
        if 'user_profile' in st.session_state and st.session_state.user_profile:
            profile = st.session_state.user_profile
            st.info(f"📋 プロフィール設定済み: {profile.get('name', 'ユーザー')}さん")
            
            if st.button("🔍 プロフィールを基にパーソナリティ分析実行", type="primary"):
                with st.spinner("プロフィール情報を基にパーソナリティを分析中..."):
                    result = st.session_state.workflow.define_user_personality()
                    
                    if result.get("status") == "success":
                        st.success("✅ パーソナリティ分析完了！")
                        
                        user_personality = result["user_personality"]
                        if "current_personality" in user_personality:
                            personality = user_personality["current_personality"]
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**💭 あなたの価値観:**")
                                for value in personality.get("values", []):
                                    st.write(f"• {value}")
                                
                                st.write("**🎯 あなたの行動特性:**")
                                for trait in personality.get("behavioral_traits", []):
                                    st.write(f"• {trait}")
                            
                            with col2:
                                st.write("**💪 現在の強み:**")
                                for strength in user_personality.get("strengths", []):
                                    st.write(f"• {strength}")
                                
                                st.write("**🌱 成長領域:**")
                                for area in user_personality.get("development_areas", []):
                                    st.write(f"• {area}")
                        
                        st.session_state.workflow_step = 3
                    else:
                        st.error(f"❌ エラー: {result.get('error')}")
        else:
            st.warning("⚠️ プロフィール設定が必要です")
            st.info("👤 左メニューの「プロフィール設定」で基本情報を入力してから、パーソナリティ分析を実行してください。")
            
            # 手動入力オプション
            with st.expander("✏️ 手動でパーソナリティ情報を入力"):
                with st.form("personality_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        strengths = st.text_area("💪 あなたの強み・特徴", key="personality_strengths")
                        experiences = st.text_area("📚 主な経験・活動", key="personality_experiences")
                        values = st.text_area("⭐ 大切にしている価値観", key="personality_values")
                    
                    with col2:
                        goals = st.text_area("🎯 将来の目標・やりたいこと", key="personality_goals")
                        leadership = st.text_area("👥 リーダーシップ経験", key="personality_leadership")
                        problem_solving = st.text_area("🔧 問題解決の経験", key="personality_problem_solving")
                    
                    if st.form_submit_button("📊 手動パーソナリティ分析実行", type="primary"):
                        if strengths and experiences:
                            user_info = {
                                "strengths": strengths,
                                "experiences": experiences,
                                "values": values,
                                "goals": goals,
                                "leadership": leadership,
                                "problem_solving": problem_solving
                            }
                            
                            with st.spinner("パーソナリティを分析中..."):
                                result = st.session_state.workflow.define_user_personality(user_info)
                                
                                if result.get("status") == "success":
                                    st.success("✅ パーソナリティ分析完了！")
                                    
                                    user_personality = result["user_personality"]
                                    if "current_personality" in user_personality:
                                        personality = user_personality["current_personality"]
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write("**💭 あなたの価値観:**")
                                            for value in personality.get("values", []):
                                                st.write(f"• {value}")
                                            
                                            st.write("**🎯 あなたの行動特性:**")
                                            for trait in personality.get("behavioral_traits", []):
                                                st.write(f"• {trait}")
                                        
                                        with col2:
                                            st.write("**💪 現在の強み:**")
                                            for strength in user_personality.get("strengths", []):
                                                st.write(f"• {strength}")
                                            
                                            st.write("**🌱 成長領域:**")
                                            for area in user_personality.get("development_areas", []):
                                                st.write(f"• {area}")
                                    
                                    st.session_state.workflow_step = 3
                                else:
                                    st.error(f"❌ エラー: {result.get('error')}")
                        else:
                            st.error("強みと経験は必須入力です")
    
    # Step 3: ギャップ分析
    if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 3:
        st.divider()
        st.subheader("3️⃣ ギャップ分析・改善提案")
        
        if st.button("🔍 ギャップ分析実行", type="primary"):
            with st.spinner("ギャップ分析を実行中..."):
                result = st.session_state.workflow.analyze_personality_gap()
                
                if result.get("status") == "success":
                    st.success("✅ ギャップ分析完了！")
                    
                    gap_analysis = result["gap_analysis"]
                    
                    # 適合度スコア
                    if "overall_fit_score" in gap_analysis:
                        score = gap_analysis["overall_fit_score"]
                        st.metric("🎯 適合度スコア", f"{score}/100")
                        st.write(gap_analysis.get("fit_assessment", ""))
                    
                    # 強み（一致点）
                    if "gap_analysis" in gap_analysis and "strengths_match" in gap_analysis["gap_analysis"]:
                        st.write("**✅ あなたの強み（企業要求と一致）:**")
                        for match in gap_analysis["gap_analysis"]["strengths_match"]:
                            st.success(f"**{match.get('area', '')}**: {match.get('description', '')}")
                            st.write(f"💡 面接アピール: {match.get('interview_appeal', '')}")
                    
                    # ギャップ（改善点）
                    if "gap_analysis" in gap_analysis and "gaps_identified" in gap_analysis["gap_analysis"]:
                        st.write("**⚠️ 改善が必要な領域:**")
                        for gap in gap_analysis["gap_analysis"]["gaps_identified"]:
                            severity_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                            icon = severity_color.get(gap.get("gap_severity", "medium"), "🟡")
                            
                            st.warning(f"{icon} **{gap.get('area', '')}**")
                            st.write(f"現在: {gap.get('current_state', '')}")
                            st.write(f"求められる状態: {gap.get('required_state', '')}")
                    
                    # 改善プラン
                    if "improvement_plan" in gap_analysis:
                        plan = gap_analysis["improvement_plan"]
                        
                        st.write("**📈 改善アクションプラン:**")
                        
                        if "immediate_actions" in plan:
                            st.write("*すぐに取り組むべき行動:*")
                            for action in plan["immediate_actions"]:
                                st.write(f"• **{action.get('action', '')}** ({action.get('timeline', '')})")
                                st.write(f"  方法: {action.get('method', '')}")
                        
                        if "medium_term_goals" in plan:
                            st.write("*中期目標:*")
                            for goal in plan["medium_term_goals"]:
                                st.write(f"• **{goal.get('goal', '')}** ({goal.get('timeline', '')})")
                    
                    st.session_state.workflow_step = 4
                else:
                    st.error(f"❌ エラー: {result.get('error')}")
    
    # Step 4: ES生成
    if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 4:
        st.divider()
        st.subheader("4️⃣ 最適化されたES生成")
        
        if st.button("📝 ES生成実行", type="primary"):
            with st.spinner("ギャップ分析を反映したESを生成中..."):
                result = st.session_state.workflow.generate_tailored_essays()
                
                if result.get("status") == "success":
                    st.success("✅ ES生成完了！")
                    
                    essays = result["essays"]
                    
                    # 自己PR
                    if "self_pr" in essays:
                        st.write("**📄 自己PR:**")
                        self_pr = essays["self_pr"]
                        if isinstance(self_pr, dict) and "self_pr" in self_pr:
                            st.write(self_pr["self_pr"])
                            st.text_area("📋 自己PRコピー用", value=self_pr["self_pr"], height=150)
                        else:
                            st.write(self_pr)
                    
                    # 志望動機
                    if "motivation" in essays:
                        st.write("**🎯 志望動機:**")
                        st.write(essays["motivation"])
                        st.text_area("📋 志望動機コピー用", value=essays["motivation"], height=150)
                    
                    st.session_state.workflow_step = 5
                else:
                    st.error(f"❌ エラー: {result.get('error')}")
    
    # Step 5: 面接対策
    if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 5:
        st.divider()
        st.subheader("5️⃣ 戦略的面接対策")
        
        if st.button("💬 面接対策生成", type="primary"):
            with st.spinner("面接戦略を準備中..."):
                result = st.session_state.workflow.prepare_interview_strategy()
                
                if result.get("status") == "success":
                    st.success("✅ 面接対策完了！")
                    
                    interview_prep = result["interview_preparation"]
                    
                    # 想定質問
                    if "questions" in interview_prep:
                        st.write("**❓ 想定面接質問:**")
                        questions = interview_prep["questions"]
                        
                        categories = {}
                        for q in questions:
                            category = q.get("category", "その他")
                            if category not in categories:
                                categories[category] = []
                            categories[category].append(q)
                        
                        for category, qs in categories.items():
                            with st.expander(f"📋 {category} ({len(qs)}問)"):
                                for i, q in enumerate(qs, 1):
                                    difficulty_color = {"低": "🟢", "中": "🟡", "高": "🔴"}
                                    difficulty_icon = difficulty_color.get(q.get("difficulty", "中"), "⚪")
                                    st.write(f"{i}. {difficulty_icon} {q['question']}")
                    
                    # 面接戦略
                    if "strategy" in interview_prep:
                        strategy = interview_prep["strategy"]
                        
                        if "highlight_strengths" in strategy:
                            st.write("**💪 面接でアピールすべき強み:**")
                            for strength in strategy["highlight_strengths"]:
                                st.write(f"• {strength}")
                        
                        if "address_gaps" in strategy:
                            st.write("**🔧 ギャップへの対処法:**")
                            for gap in strategy["address_gaps"]:
                                st.write(f"• {gap}")
                    
                    # 改善プラン
                    if "development_plan" in interview_prep:
                        st.write("**📈 パーソナリティ改善プラン:**")
                        st.write(interview_prep["development_plan"])
                    
                    st.success("🎉 **ワークフロー完了！** 準備が整いました。")
                else:
                    st.error(f"❌ エラー: {result.get('error')}")

def home_page():
    st.header("🏠 ホーム")
    st.markdown("AI があなたの就活を成功に導きます")
    
    # プロフィール確認
    if 'user_profile' not in st.session_state:
        st.warning("⚠️ まずは「👤 プロフィール設定」で基本情報を入力してください")
    else:
        profile = st.session_state.user_profile
        st.success(f"👋 {profile.get('name', 'ユーザー')}さん、こんにちは！")
    
    st.divider()
    
    # メイン機能: 企業分析
    st.subheader("🏢 企業分析を開始")
    st.markdown("志望企業を入力して、AI による包括的な企業分析と就活準備を始めましょう")
    
    # 企業名入力
    company_name = st.text_input(
        "🏢 企業名を入力してください",
        placeholder="例: トヨタ自動車、ソフトバンク、三菱商事",
        key="home_company_input"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 完全分析開始", type="primary", use_container_width=True):
            if company_name:
                # ワークフローを開始（プロフィール設定なしでも可能）
                st.session_state.selected_company = company_name
                st.session_state.workflow_active = True
                st.success(f"✅ {company_name} の分析を開始します")
                
                # ワークフロー開始
                with st.spinner("企業分析を実行中..."):
                    result = st.session_state.workflow.start_workflow(company_name)
                    
                    if result.get("status") == "success":
                        st.success("🎉 企業分析完了！詳細ワークフローで続きを進めてください")
                        st.session_state.show_detailed_workflow = True
                        st.rerun()
                    else:
                        st.error(f"❌ エラー: {result.get('error', '不明なエラー')}")
            else:
                st.error("❌ 企業名を入力してください")
    
    with col2:
        if st.button("🔍 詳細ワークフロー", use_container_width=True):
            if company_name:
                # ワークフローを開始してセッション状態を設定（プロフィール設定なしでも可能）
                st.session_state.selected_company = company_name
                st.session_state.show_detailed_workflow = True
                st.success(f"✅ {company_name} の詳細ワークフローを開始します")
                st.rerun()
            else:
                st.error("❌ 企業名を入力してください")
    
    st.divider()
    
    # 機能紹介（簡潔版）
    st.subheader("🌟 主な機能")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 統合ワークフロー**
        
        企業分析→パーソナリティ分析→ES生成→面接対策まで一貫サポート
        """)
    
    with col2:
        st.markdown("""
        **👤 プロフィール管理**
        
        大学・学部・部活・ガクチカなど基本情報を一元管理
        """)
    
    with col3:
        st.markdown("""
        **🤖 AI支援**
        
        Claude AI が最適な就活戦略とコンテンツを自動生成
        """)
    
    # 使い方ガイド
    with st.expander("📖 使い方ガイド"):
        st.markdown("""
        **🚀 クイックスタート**
        1. 企業名を入力して「完全分析開始」をクリック
        2. AI企業分析結果を確認
        3. 簡易フォームでパーソナリティ情報を入力
        4. ギャップ分析→ES生成→面接対策と順次実行
        
        **📊 詳細分析の場合**
        1. 👤「プロフィール設定」で詳細情報を入力
        2. より精密なパーソナリティ分析が可能
        3. カスタマイズされたES・面接対策を生成
        
        **💡 ポイント**
        - プロフィール設定は後からでもOK
        - 企業分析は即座に開始可能
        - 詳細設定で分析精度がアップ
        
        詳しくは「❓ ヘルプ」をご覧ください。
        """)
    
    # 詳細ワークフローの表示
    if st.session_state.get('show_detailed_workflow', False):
        st.divider()
        st.subheader("📋 詳細ワークフロー")
        integrated_workflow_content()

def integrated_workflow_content():
    """統合ワークフローのコンテンツ（タイトルなし）"""
    # プロセス表示
    st.markdown("**企業分析から始まる一貫した就活準備プロセス**")
    
    process_steps = [
        "1️⃣ 企業分析 → 企業が求める人物像を特定",
        "2️⃣ パーソナリティ定義 → あなたの現在の特性を分析", 
        "3️⃣ ギャップ分析 → 理想と現実の差を明確化",
        "4️⃣ ES生成 → ギャップを踏まえた最適なES作成",
        "5️⃣ 面接対策 → 戦略的な面接準備"
    ]
    
    for step in process_steps:
        st.write(step)
    
    st.divider()
    
    # Step 1: 企業分析結果表示（既に実行済みの場合）
    if st.session_state.workflow.workflow_state.get("company_analysis"):
        st.subheader("1️⃣ 企業分析結果")
        
        company_analysis = st.session_state.workflow.workflow_state["company_analysis"]
        st.success("✅ 企業分析完了！")
        
        # 統合された企業分析レポート
        with st.container():
            st.markdown("""
            <style>
            /* ダークモード対応のベーススタイル */
            @media (prefers-color-scheme: dark) {
                .analysis-container {
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
                    border: 1px solid #333 !important;
                }
                .section-card {
                    background: rgba(45, 55, 72, 0.95) !important;
                    border: 1px solid #4a5568 !important;
                    color: #e2e8f0 !important;
                }
                .section-title {
                    color: #e2e8f0 !important;
                    border-left-color: #63b3ed !important;
                }
                .info-item {
                    background: #2d3748 !important;
                    border-left-color: #63b3ed !important;
                    color: #e2e8f0 !important;
                }
                .metric-label {
                    color: #a0aec0 !important;
                }
                .metric-value {
                    color: #e2e8f0 !important;
                }
            }
            
            .analysis-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 15px;
                margin: 1rem 0;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.1);
            }
            .analysis-title {
                color: white;
                font-size: 1.8rem;
                font-weight: 700;
                margin-bottom: 1rem;
                text-align: center;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            .section-card {
                background: rgba(255,255,255,0.95);
                padding: 1.5rem;
                border-radius: 12px;
                margin: 1rem 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
            }
            .section-title {
                font-size: 1.4rem;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 1rem;
                border-left: 4px solid #3498db;
                padding-left: 1rem;
            }
            .info-item {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 8px;
                border-left: 3px solid #3498db;
                margin: 0.5rem 0;
                transition: all 0.3s ease;
            }
            .info-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            .metric-label {
                font-weight: 600;
                color: #34495e;
                font-size: 0.9rem;
                margin-bottom: 0.3rem;
            }
            .metric-value {
                color: #2c3e50;
                line-height: 1.5;
                font-size: 0.95rem;
            }
            .ai-analysis-text {
                line-height: 1.7;
                font-size: 0.95rem;
                margin: 0.4rem 0;
                padding: 0.3rem 0;
            }
            .ai-analysis-title {
                font-size: 1.2rem;
                font-weight: 600;
                margin: 1.5rem 0 0.8rem 0;
                padding: 0.5rem 0;
                border-bottom: 2px solid #e9ecef;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="analysis-title">🤖 AI企業分析レポート</h2>', unsafe_allow_html=True)
            
            # 基本情報セクション
            if company_analysis.get("basic_info"):
                basic_info = company_analysis["basic_info"]
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🏢 企業概要</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="metric-label">企業名</div>
                        <div class="metric-value">{basic_info.get('name', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="metric-label">業界</div>
                        <div class="metric-value">{basic_info.get('industry', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="metric-label">事業概要</div>
                        <div class="metric-value">{basic_info.get('description', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 財務情報セクション
            if company_analysis.get("ir_summary"):
                ir_data = company_analysis["ir_summary"]
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📈 財務・事業動向</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="metric-label">💰 売上動向</div>
                        <div class="metric-value">{ir_data.get('revenue_trend', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if ir_data.get("key_initiatives"):
                        st.markdown('<div class="metric-label">🚀 重点施策</div>', unsafe_allow_html=True)
                        for initiative in ir_data["key_initiatives"]:
                            st.markdown(f"<div class='metric-value'>• {initiative}</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="info-item">
                        <div class="metric-label">📊 利益動向</div>
                        <div class="metric-value">{ir_data.get('profit_trend', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if ir_data.get("challenges"):
                        st.markdown('<div class="metric-label">⚠️ 主要課題</div>', unsafe_allow_html=True)
                        for challenge in ir_data["challenges"]:
                            st.markdown(f"<div class='metric-value'>• {challenge}</div>", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # AI分析セクション
            if company_analysis.get("ai_analysis"):
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🧠 AI戦略分析</div>', unsafe_allow_html=True)
                
                ai_analysis = company_analysis["ai_analysis"]
                
                if isinstance(ai_analysis, str):
                    if ai_analysis.startswith("Error:"):
                        st.error(ai_analysis)
                    else:
                        lines = ai_analysis.split('\n')
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue
                            
                            if (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
                                line.startswith(('##', '**')) or
                                line.startswith(('○', '●', '・', '◆', '◇')) or
                                '：' in line[:20] or ':' in line[:20]):
                                st.markdown(f'<div class="ai-analysis-title">{line}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="ai-analysis-text" style="margin-left: 1.5rem;">{line}</div>', unsafe_allow_html=True)
                else:
                    try:
                        import json
                        if isinstance(ai_analysis, dict):
                            analysis_data = ai_analysis
                        else:
                            analysis_data = json.loads(ai_analysis)
                        
                        analysis_sections = {
                            "strengths": {"title": "💪 企業の強み", "color": "#27ae60"},
                            "weaknesses": {"title": "⚠️ 課題・弱み", "color": "#e74c3c"},
                            "opportunities": {"title": "🌟 事業機会", "color": "#3498db"},
                            "competitive_position": {"title": "🎯 競争ポジション", "color": "#9b59b6"}
                        }
                        
                        for key, config in analysis_sections.items():
                            if key in analysis_data:
                                st.markdown(f'<div class="ai-analysis-title" style="color: {config["color"]};">{config["title"]}</div>', unsafe_allow_html=True)
                                value = analysis_data[key]
                                if isinstance(value, list):
                                    for item in value:
                                        st.markdown(f'<div class="ai-analysis-text" style="margin-left: 1.5rem;">• {item}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="ai-analysis-text" style="margin-left: 1.5rem;">{value}</div>', unsafe_allow_html=True)
                        
                        for key, value in analysis_data.items():
                            if key not in analysis_sections:
                                st.markdown(f'<div class="ai-analysis-title">{key}</div>', unsafe_allow_html=True)
                                if isinstance(value, list):
                                    for item in value:
                                        st.markdown(f'<div class="ai-analysis-text" style="margin-left: 1.5rem;">• {item}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="ai-analysis-text" style="margin-left: 1.5rem;">{value}</div>', unsafe_allow_html=True)
                    
                    except (json.JSONDecodeError, TypeError):
                        lines = str(ai_analysis).split('\n')
                        for line in lines:
                            line = line.strip()
                            if not line:
                                continue
                            
                            if (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')) or
                                line.startswith(('##', '**')) or
                                line.startswith(('○', '●', '・', '◆', '◇')) or
                                '：' in line[:20] or ':' in line[:20]):
                                st.markdown(f'<div class="ai-analysis-title">{line}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="ai-analysis-text" style="margin-left: 1.5rem;">{line}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 求める人物像
        required_personality = st.session_state.workflow.workflow_state.get("required_personality")
        if required_personality:
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="analysis-title">👤 求める人物像</h2>', unsafe_allow_html=True)
            
            if "required_personality" in required_personality:
                personality = required_personality["required_personality"]
                
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                
                # 価値観とスキルを2カラムで表示
                col1, col2 = st.columns(2)
                
                with col1:
                    if personality.get("values"):
                        st.markdown('<h4 style="color: #27ae60; margin-bottom: 0.8rem;">💭 重視する価値観</h4>', unsafe_allow_html=True)
                        for value in personality["values"]:
                            st.markdown(f'<div style="margin: 0.2rem 0; padding: 0.3rem 0.8rem; background: #d5edda; border-left: 3px solid #27ae60; border-radius: 4px;">✓ {value}</div>', unsafe_allow_html=True)
                    
                    if personality.get("communication_style"):
                        st.markdown('<h4 style="color: #3498db; margin: 1rem 0 0.8rem 0;">💬 コミュニケーション</h4>', unsafe_allow_html=True)
                        st.markdown(f'<div style="line-height: 1.6; margin: 0.2rem 0;">{personality["communication_style"]}</div>', unsafe_allow_html=True)
                    
                    if personality.get("leadership_style"):
                        st.markdown('<h4 style="color: #9b59b6; margin: 1rem 0 0.8rem 0;">👥 リーダーシップ</h4>', unsafe_allow_html=True)
                        st.markdown(f'<div style="line-height: 1.6; margin: 0.2rem 0;">{personality["leadership_style"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    if personality.get("skills"):
                        st.markdown('<h4 style="color: #e67e22; margin-bottom: 0.8rem;">🛠 必要なスキル</h4>', unsafe_allow_html=True)
                        for skill in personality["skills"]:
                            st.markdown(f'<div style="margin: 0.2rem 0; padding: 0.3rem 0.8rem; background: #fdeaa7; border-left: 3px solid #e67e22; border-radius: 4px;">🔧 {skill}</div>', unsafe_allow_html=True)
                    
                    if personality.get("problem_solving"):
                        st.markdown('<h4 style="color: #e74c3c; margin: 1rem 0 0.8rem 0;">🔧 問題解決</h4>', unsafe_allow_html=True)
                        st.markdown(f'<div style="line-height: 1.6; margin: 0.2rem 0;">{personality["problem_solving"]}</div>', unsafe_allow_html=True)
                    
                    if personality.get("teamwork"):
                        st.markdown('<h4 style="color: #1abc9c; margin: 1rem 0 0.8rem 0;">🤝 チームワーク</h4>', unsafe_allow_html=True)
                        st.markdown(f'<div style="line-height: 1.6; margin: 0.2rem 0;">{personality["teamwork"]}</div>', unsafe_allow_html=True)
                
                # 行動特性と成長姿勢を下段に表示
                if personality.get("behavioral_traits") or personality.get("growth_mindset"):
                    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if personality.get("behavioral_traits"):
                            st.markdown('<h4 style="color: #3498db; margin-bottom: 0.8rem;">🎯 求める行動特性</h4>', unsafe_allow_html=True)
                            for trait in personality["behavioral_traits"]:
                                st.markdown(f'<div style="margin: 0.2rem 0; padding: 0.3rem 0.8rem; background: #d1ecf1; border-left: 3px solid #3498db; border-radius: 4px;">• {trait}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        if personality.get("growth_mindset"):
                            st.markdown('<h4 style="color: #8e44ad; margin-bottom: 0.8rem;">📈 成長姿勢</h4>', unsafe_allow_html=True)
                            st.markdown(f'<div style="line-height: 1.6; margin: 0.2rem 0;">{personality["growth_mindset"]}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 面接重要ポイント
            if "key_interview_points" in required_personality:
                st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
                st.markdown('<h4 style="color: #e74c3c; margin-bottom: 0.8rem;">❓ 面接で重視されるポイント</h4>', unsafe_allow_html=True)
                for i, point in enumerate(required_personality["key_interview_points"], 1):
                    st.markdown(f'<div style="margin: 0.2rem 0; padding: 0.3rem 0.8rem; background: #fadbd8; border-left: 3px solid #e74c3c; border-radius: 4px;"><strong>{i}.</strong> {point}</div>', unsafe_allow_html=True)
            
            # 成功要因
            if "success_factors" in required_personality:
                st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
                st.markdown('<h4 style="color: #f39c12; margin-bottom: 0.8rem;">🏆 この企業で成功する要因</h4>', unsafe_allow_html=True)
                for factor in required_personality["success_factors"]:
                    st.markdown(f'<div style="margin: 0.2rem 0; padding: 0.3rem 0.8rem; background: #fdeaa7; border-left: 3px solid #f39c12; border-radius: 4px;">⭐ {factor}</div>', unsafe_allow_html=True)
            
            # その他の詳細情報があれば表示
            if isinstance(required_personality, str) and not required_personality.get("required_personality"):
                # テキスト形式の場合
                st.write(required_personality)
        
        st.session_state.workflow_step = 2
        
        # Step 2以降の処理を表示
        if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 2:
            st.divider()
            st.subheader("2️⃣ あなたのパーソナリティ定義")
            
            # プロフィール設定の確認
            if 'user_profile' in st.session_state and st.session_state.user_profile:
                profile = st.session_state.user_profile
                st.info(f"📋 プロフィール設定済み: {profile.get('name', 'ユーザー')}さん")
                
                if st.button("🔍 プロフィールを基にパーソナリティ分析実行", type="primary", key="workflow_personality_next"):
                    with st.spinner("プロフィール情報を基にパーソナリティを分析中..."):
                        result = st.session_state.workflow.define_user_personality()
                        
                        if result.get("status") == "success":
                            st.success("✅ パーソナリティ分析完了！")
                            
                            user_personality = result["user_personality"]
                            if "current_personality" in user_personality:
                                personality = user_personality["current_personality"]
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**💭 あなたの価値観:**")
                                    for value in personality.get("values", []):
                                        st.write(f"• {value}")
                                    
                                    st.write("**🎯 あなたの行動特性:**")
                                    for trait in personality.get("behavioral_traits", []):
                                        st.write(f"• {trait}")
                                
                                with col2:
                                    st.write("**💪 現在の強み:**")
                                    for strength in user_personality.get("strengths", []):
                                        st.write(f"• {strength}")
                                    
                                    st.write("**🌱 成長領域:**")
                                    for area in user_personality.get("development_areas", []):
                                        st.write(f"• {area}")
                            
                            st.session_state.workflow_step = 3
                            st.rerun()
                        else:
                            st.error(f"❌ エラー: {result.get('error')}")
            else:
                st.info("💡 プロフィール設定済みの場合、より詳細な分析が可能です")
                st.markdown("**オプション1:** 👤 左メニューの「プロフィール設定」で詳細情報を入力")
                st.markdown("**オプション2:** 👇 下記フォームで簡易入力")
            
            # 手動入力オプション（常に表示）
            with st.expander("✏️ 簡易パーソナリティ情報入力", expanded=True if 'user_profile' not in st.session_state or not st.session_state.user_profile else False):
                with st.form("personality_form_simple"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        strengths = st.text_area("💪 あなたの強み・特徴", key="personality_strengths_simple")
                        experiences = st.text_area("📚 主な経験・活動", key="personality_experiences_simple")
                        values = st.text_area("⭐ 大切にしている価値観", key="personality_values_simple")
                    
                    with col2:
                        goals = st.text_area("🎯 将来の目標・やりたいこと", key="personality_goals_simple")
                        leadership = st.text_area("👥 リーダーシップ経験", key="personality_leadership_simple")
                        problem_solving = st.text_area("🔧 問題解決の経験", key="personality_problem_solving_simple")
                    
                    if st.form_submit_button("📊 簡易パーソナリティ分析実行", type="primary"):
                        if strengths and experiences:
                            user_info = {
                                "strengths": strengths,
                                "experiences": experiences,
                                "values": values,
                                "goals": goals,
                                "leadership": leadership,
                                "problem_solving": problem_solving
                            }
                            
                            with st.spinner("パーソナリティを分析中..."):
                                result = st.session_state.workflow.define_user_personality(user_info)
                                
                                if result.get("status") == "success":
                                    st.success("✅ パーソナリティ分析完了！")
                                    
                                    user_personality = result["user_personality"]
                                    if "current_personality" in user_personality:
                                        personality = user_personality["current_personality"]
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write("**💭 あなたの価値観:**")
                                            for value in personality.get("values", []):
                                                st.write(f"• {value}")
                                            
                                            st.write("**🎯 あなたの行動特性:**")
                                            for trait in personality.get("behavioral_traits", []):
                                                st.write(f"• {trait}")
                                        
                                        with col2:
                                            st.write("**💪 現在の強み:**")
                                            for strength in user_personality.get("strengths", []):
                                                st.write(f"• {strength}")
                                            
                                            st.write("**🌱 成長領域:**")
                                            for area in user_personality.get("development_areas", []):
                                                st.write(f"• {area}")
                                    
                                    st.session_state.workflow_step = 3
                                    st.rerun()
                                else:
                                    st.error(f"❌ エラー: {result.get('error')}")
                        else:
                            st.error("強みと経験は必須入力です")
        
        # Step 3: ギャップ分析
        if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 3:
            st.divider()
            st.subheader("3️⃣ ギャップ分析・改善提案")
            
            if st.button("🔍 ギャップ分析実行", type="primary", key="workflow_gap_next"):
                with st.spinner("ギャップ分析を実行中..."):
                    result = st.session_state.workflow.analyze_personality_gap()
                    
                    if result.get("status") == "success":
                        st.success("✅ ギャップ分析完了！")
                        
                        gap_analysis = result["gap_analysis"]
                        
                        # 適合度スコア
                        if "overall_fit_score" in gap_analysis:
                            score = gap_analysis["overall_fit_score"]
                            st.metric("🎯 適合度スコア", f"{score}/100")
                            st.write(gap_analysis.get("fit_assessment", ""))
                        
                        # 強み（一致点）
                        if "gap_analysis" in gap_analysis and "strengths_match" in gap_analysis["gap_analysis"]:
                            st.write("**✅ あなたの強み（企業要求と一致）:**")
                            for match in gap_analysis["gap_analysis"]["strengths_match"]:
                                st.success(f"**{match.get('area', '')}**: {match.get('description', '')}")
                                st.write(f"💡 面接アピール: {match.get('interview_appeal', '')}")
                        
                        # ギャップ（改善点）
                        if "gap_analysis" in gap_analysis and "gaps_identified" in gap_analysis["gap_analysis"]:
                            st.write("**⚠️ 改善が必要な領域:**")
                            for gap in gap_analysis["gap_analysis"]["gaps_identified"]:
                                severity_color = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                                icon = severity_color.get(gap.get("gap_severity", "medium"), "🟡")
                                
                                st.warning(f"{icon} **{gap.get('area', '')}**")
                                st.write(f"現在: {gap.get('current_state', '')}")
                                st.write(f"求められる状態: {gap.get('required_state', '')}")
                        
                        # 改善プラン
                        if "improvement_plan" in gap_analysis:
                            plan = gap_analysis["improvement_plan"]
                            
                            st.write("**📈 改善アクションプラン:**")
                            
                            if "immediate_actions" in plan:
                                st.write("*すぐに取り組むべき行動:*")
                                for action in plan["immediate_actions"]:
                                    st.write(f"• **{action.get('action', '')}** ({action.get('timeline', '')})")
                                    st.write(f"  方法: {action.get('method', '')}")
                            
                            if "medium_term_goals" in plan:
                                st.write("*中期目標:*")
                                for goal in plan["medium_term_goals"]:
                                    st.write(f"• **{goal.get('goal', '')}** ({goal.get('timeline', '')})")
                        
                        st.session_state.workflow_step = 4
                        st.rerun()
                    else:
                        st.error(f"❌ エラー: {result.get('error')}")
        
        # Step 4: ES生成
        if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 4:
            st.divider()
            st.subheader("4️⃣ 最適化されたES生成")
            
            if st.button("📝 ES生成実行", type="primary", key="workflow_essay_next"):
                with st.spinner("ギャップ分析を反映したESを生成中..."):
                    result = st.session_state.workflow.generate_tailored_essays()
                    
                    if result.get("status") == "success":
                        st.success("✅ ES生成完了！")
                        
                        essays = result["essays"]
                        
                        # 自己PR
                        if "self_pr" in essays:
                            st.write("**📄 自己PR:**")
                            self_pr = essays["self_pr"]
                            if isinstance(self_pr, dict) and "self_pr" in self_pr:
                                st.write(self_pr["self_pr"])
                                st.text_area("📋 自己PRコピー用", value=self_pr["self_pr"], height=150, key="copy_self_pr_next")
                            else:
                                st.write(self_pr)
                        
                        # 志望動機
                        if "motivation" in essays:
                            st.write("**🎯 志望動機:**")
                            st.write(essays["motivation"])
                            st.text_area("📋 志望動機コピー用", value=essays["motivation"], height=150, key="copy_motivation_next")
                        
                        st.session_state.workflow_step = 5
                        st.rerun()
                    else:
                        st.error(f"❌ エラー: {result.get('error')}")
        
        # Step 5: 面接対策
        if hasattr(st.session_state, 'workflow_step') and st.session_state.workflow_step >= 5:
            st.divider()
            st.subheader("5️⃣ 戦略的面接対策")
            
            if st.button("💬 面接対策生成", type="primary", key="workflow_interview_next"):
                with st.spinner("面接戦略を準備中..."):
                    result = st.session_state.workflow.prepare_interview_strategy()
                    
                    if result.get("status") == "success":
                        st.success("✅ 面接対策完了！")
                        
                        interview_prep = result["interview_preparation"]
                        
                        # 想定質問
                        if "questions" in interview_prep:
                            st.write("**❓ 想定面接質問:**")
                            questions = interview_prep["questions"]
                            
                            categories = {}
                            for q in questions:
                                category = q.get("category", "その他")
                                if category not in categories:
                                    categories[category] = []
                                categories[category].append(q)
                            
                            for category, qs in categories.items():
                                with st.expander(f"📋 {category} ({len(qs)}問)"):
                                    for i, q in enumerate(qs, 1):
                                        difficulty_color = {"低": "🟢", "中": "🟡", "高": "🔴"}
                                        difficulty_icon = difficulty_color.get(q.get("difficulty", "中"), "⚪")
                                        st.write(f"{i}. {difficulty_icon} {q['question']}")
                        
                        # 面接戦略
                        if "strategy" in interview_prep:
                            strategy = interview_prep["strategy"]
                            
                            if "highlight_strengths" in strategy:
                                st.write("**💪 面接でアピールすべき強み:**")
                                for strength in strategy["highlight_strengths"]:
                                    st.write(f"• {strength}")
                            
                            if "address_gaps" in strategy:
                                st.write("**🔧 ギャップへの対処法:**")
                                for gap in strategy["address_gaps"]:
                                    st.write(f"• {gap}")
                        
                        # 改善プラン
                        if "development_plan" in interview_prep:
                            st.write("**📈 パーソナリティ改善プラン:**")
                            st.write(interview_prep["development_plan"])
                        
                        st.success("🎉 **ワークフロー完了！** 準備が整いました。")
                    else:
                        st.error(f"❌ エラー: {result.get('error')}")

def profile_setting_page():
    st.header("👤 プロフィール設定")
    st.markdown("あなたの基本情報を入力してください。この情報を基にAIがパーソナライズされた就活支援を提供します。")
    
    # プロフィール初期化
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    
    with st.form("profile_form"):
        st.subheader("📚 基本情報")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "👤 お名前",
                value=st.session_state.user_profile.get('name', ''),
                placeholder="山田太郎"
            )
            
            university = st.text_input(
                "🏫 大学名",
                value=st.session_state.user_profile.get('university', ''),
                placeholder="例: 東京大学"
            )
            
            faculty = st.text_input(
                "📖 学部",
                value=st.session_state.user_profile.get('faculty', ''),
                placeholder="例: 経済学部"
            )
            
            department = st.text_input(
                "🔬 学科",
                value=st.session_state.user_profile.get('department', ''),
                placeholder="例: 経済学科"
            )
            
            graduation_year = st.selectbox(
                "🎓 卒業予定年",
                options=[2024, 2025, 2026, 2027, 2028],
                index=1 if st.session_state.user_profile.get('graduation_year') == 2025 else 0
            )
        
        with col2:
            club_activities = st.text_area(
                "⚽ 部活動・サークル",
                value=st.session_state.user_profile.get('club_activities', ''),
                placeholder="例: テニス部（4年間）、ボランティアサークル",
                height=100
            )
            
            part_time_job = st.text_area(
                "💼 アルバイト経験",
                value=st.session_state.user_profile.get('part_time_job', ''),
                placeholder="例: 塾講師（2年間）、カフェスタッフ",
                height=100
            )
            
            internship = st.text_area(
                "🏢 インターン経験",
                value=st.session_state.user_profile.get('internship', ''),
                placeholder="例: IT企業でのエンジニアインターン（3ヶ月）",
                height=100
            )
        
        st.subheader("🌟 自己分析")
        
        gakuchika = st.text_area(
            "📈 学生時代に力を入れたこと（ガクチカ）",
            value=st.session_state.user_profile.get('gakuchika', ''),
            placeholder="具体的なエピソードと成果を記入してください",
            height=150
        )
        
        strengths = st.text_area(
            "💪 あなたの強み",
            value=st.session_state.user_profile.get('strengths', ''),
            placeholder="例: リーダーシップ、分析力、コミュニケーション力",
            height=100
        )
        
        values = st.text_area(
            "⭐ 大切にしている価値観",
            value=st.session_state.user_profile.get('values', ''),
            placeholder="例: 成長、チームワーク、社会貢献",
            height=100
        )
        
        career_goals = st.text_area(
            "🎯 将来の目標・やりたいこと",
            value=st.session_state.user_profile.get('career_goals', ''),
            placeholder="将来どのようなキャリアを歩みたいか",
            height=100
        )
        
        st.subheader("🏭 志望業界・職種")
        
        target_industries = st.multiselect(
            "🎯 志望業界",
            options=[
                "IT・ソフトウェア", "金融・銀行", "コンサルティング", 
                "メーカー・製造業", "商社・流通", "インフラ・公共",
                "メディア・広告", "医療・ヘルスケア", "不動産・建設", "教育・研究"
            ],
            default=st.session_state.user_profile.get('target_industries', [])
        )
        
        job_types = st.multiselect(
            "💼 志望職種",
            options=[
                "営業", "マーケティング", "企画", "経営企画", "人事",
                "財務・経理", "エンジニア", "研究開発", "コンサルタント", "その他"
            ],
            default=st.session_state.user_profile.get('job_types', [])
        )
        
        if st.form_submit_button("💾 プロフィール保存", type="primary"):
            # プロフィールデータを保存
            st.session_state.user_profile = {
                'name': name,
                'university': university,
                'faculty': faculty,
                'department': department,
                'graduation_year': graduation_year,
                'club_activities': club_activities,
                'part_time_job': part_time_job,
                'internship': internship,
                'gakuchika': gakuchika,
                'strengths': strengths,
                'values': values,
                'career_goals': career_goals,
                'target_industries': target_industries,
                'job_types': job_types
            }
            
            st.success("✅ プロフィールが保存されました！")
            st.info("🏠 ホーム画面で企業分析を開始できます")
    
    # 現在のプロフィール表示
    if st.session_state.user_profile:
        st.divider()
        st.subheader("📋 現在のプロフィール")
        
        profile = st.session_state.user_profile
        
        col1, col2 = st.columns(2)
        
        with col1:
            if profile.get('name'):
                st.write(f"**👤 名前:** {profile['name']}")
            if profile.get('university'):
                st.write(f"**🏫 大学:** {profile['university']} {profile.get('faculty', '')} {profile.get('department', '')}")
            if profile.get('graduation_year'):
                st.write(f"**🎓 卒業予定:** {profile['graduation_year']}年")
        
        with col2:
            if profile.get('target_industries'):
                st.write(f"**🎯 志望業界:** {', '.join(profile['target_industries'])}")
            if profile.get('job_types'):
                st.write(f"**💼 志望職種:** {', '.join(profile['job_types'])}")

def help_page():
    st.header("❓ ヘルプ")
    st.markdown("就活AIコンパスの使い方を説明します")
    
    # FAQ形式
    with st.expander("🚀 はじめ方", expanded=True):
        st.markdown("""
        **1. プロフィール設定**
        - 左メニューの「👤 プロフィール設定」から基本情報を入力
        - 大学・学部・ガクチカ・強みなどを詳しく記入
        
        **2. 企業分析開始**
        - ホーム画面で志望企業名を入力
        - 「🚀 完全分析開始」をクリック
        
        **3. ワークフロー実行**
        - 「🎯 統合ワークフロー」で段階的に進行
        - AI がパーソナライズされた就活支援を提供
        """)
    
    with st.expander("🎯 統合ワークフローとは？"):
        st.markdown("""
        企業分析から面接対策まで一貫した就活準備プロセスです：
        
        **1. 🏢 企業分析**
        - IR情報や事業戦略の自動分析
        - 企業が求める人物像の特定
        
        **2. 👤 パーソナリティ分析**
        - あなたの特性と企業要求の比較
        - ギャップの特定と改善提案
        
        **3. 📝 ES生成**
        - ギャップ分析を反映した最適なES作成
        - 自己PR・志望動機の自動生成
        
        **4. 💬 面接対策**
        - 企業特化の想定質問生成
        - 戦略的な回答準備
        """)
    
    with st.expander("👤 プロフィール設定のコツ"):
        st.markdown("""
        **詳細に記入するほど精度が向上します：**
        
        **ガクチカ記入のポイント:**
        - 具体的な数値・成果を含める
        - 困難や課題とその解決方法
        - 学んだことや成長した点
        
        **強み記入のポイント:**
        - エピソードと関連付ける
        - 客観的な評価があれば記載
        - 企業でどう活かせるかも考える
        
        **価値観記入のポイント:**
        - なぜその価値観を大切にするのか
        - 行動にどう表れているか
        """)
    
    with st.expander("🏢 企業分析の活用方法"):
        st.markdown("""
        **分析結果の見方:**
        - 企業の強み・弱み・戦略を把握
        - 求める人物像を理解
        - 業界内のポジションを確認
        
        **活用方法:**
        - 志望動機の材料として活用
        - 面接での質問準備
        - 企業研究の効率化
        
        **注意点:**
        - 情報は参考程度に留める
        - 最新情報は公式サイトで確認
        - 複数の企業を比較検討
        """)
    
    with st.expander("📝 ES・面接対策のポイント"):
        st.markdown("""
        **ES生成機能:**
        - AI が最適な構成を提案
        - ギャップ分析を反映した内容
        - コピー＆ペースト可能な形式
        
        **面接対策機能:**
        - 企業・業界特化の想定質問
        - パーソナリティに基づく回答戦略
        - 強みのアピール方法を提案
        
        **改善のコツ:**
        - AI の提案を参考に自分なりにアレンジ
        - 実際の経験と照らし合わせて修正
        - 複数パターンを用意
        """)
    
    with st.expander("🔧 トラブルシューティング"):
        st.markdown("""
        **よくある問題と解決方法:**
        
        **企業分析が失敗する場合:**
        - 企業名を正確に入力（上場企業名推奨）
        - しばらく時間をおいて再試行
        
        **プロフィールが保存されない場合:**
        - 必須項目（名前・大学など）を入力
        - ブラウザをリフレッシュして再試行
        
        **ワークフローが進まない場合:**
        - 前のステップが完了しているか確認
        - プロフィール設定が済んでいるか確認
        
        **その他の問題:**
        - ページをリフレッシュしてみる
        - 別のブラウザで試してみる
        """)
    
    st.divider()
    
    st.subheader("📧 お問い合わせ")
    st.markdown("""
    その他ご質問やバグの報告は、GitHubのIssuesページまでお願いします。
    
    🔗 **GitHub Repository**: https://github.com/Ume614/shukatsuai
    """)
    
    st.info("💡 **ヒント**: プロフィール設定を詳しく記入するほど、AIの分析精度が向上します！")

def company_analysis_page():
    st.header("🏢 企業分析AI")
    st.markdown("企業名を入力すると、IR情報や事業戦略を基にAIが包括的な企業分析を行います。")
    
    company_name = st.text_input("📝 企業名を入力してください", placeholder="例: トヨタ自動車、ソフトバンク、三菱商事")
    
    col1, col2 = st.columns(2)
    with col1:
        analyze_btn = st.button("🔍 企業分析実行", type="primary")
    with col2:
        questions_btn = st.button("❓ 想定質問生成")
    
    if analyze_btn and company_name:
        analyzer = CompanyAnalyzer()
        with st.spinner("企業情報を分析中... 少々お待ちください"):
            result = analyzer.analyze(company_name)
            
            if result["status"] == "success":
                st.success("✅ 分析完了！")
                
                # 分析結果の表示
                st.subheader("📊 分析結果")
                
                with st.expander("🏢 企業基本情報", expanded=True):
                    st.write(result["basic_info"])
                
                with st.expander("📈 IR情報サマリー"):
                    st.write(result["ir_summary"])
                
                with st.expander("🤖 AI分析レポート"):
                    st.write(result["ai_analysis"])
            else:
                st.error(f"❌ エラーが発生しました: {result.get('error', '不明なエラー')}")
    
    if questions_btn and company_name:
        analyzer = CompanyAnalyzer()
        with st.spinner("想定質問を生成中..."):
            questions = analyzer.get_interview_points(company_name)
            
            st.subheader("❓ 面接想定質問")
            for i, question in enumerate(questions, 1):
                st.write(f"{i}. {question}")

def industry_matching_page():
    st.header("🎯 業界適性診断")
    st.markdown("あなたの経験やスキルを基に、最適な業界を AI が診断します。")
    
    with st.form("profile_form"):
        st.subheader("👤 プロフィール入力")
        
        col1, col2 = st.columns(2)
        with col1:
            strengths = st.text_area("💪 あなたの強み", placeholder="リーダーシップ、分析力、コミュニケーション力など")
            experiences = st.text_area("🎓 主な経験・活動", placeholder="サークル活動、アルバイト、インターンなど")
        
        with col2:
            interests = st.text_area("❤️ 興味・関心分野", placeholder="テクノロジー、国際情勢、ビジネスなど")
            values = st.text_area("⭐ 大切にしている価値観", placeholder="成長、安定、社会貢献など")
        
        submitted = st.form_submit_button("🔍 適性診断実行", type="primary")
        
        if submitted:
            if strengths and experiences:
                matcher = IndustryMatcher()
                user_profile = {
                    "strengths": strengths,
                    "experiences": experiences,
                    "interests": interests,
                    "values": values
                }
                
                with st.spinner("業界適性を分析中..."):
                    result = matcher.analyze_fit(user_profile)
                    
                    if result.get("status") != "error":
                        st.success("✅ 診断完了！")
                        
                        if "industry_scores" in result:
                            st.subheader("📊 業界適性スコア")
                            
                            scores_data = []
                            for industry, data in result["industry_scores"].items():
                                scores_data.append({
                                    "業界": industry,
                                    "適性スコア": data["score"],
                                    "理由": data["reason"]
                                })
                            
                            # スコア順にソート
                            scores_data.sort(key=lambda x: x["適性スコア"], reverse=True)
                            
                            for data in scores_data[:5]:  # 上位5つを表示
                                with st.expander(f"{data['業界']} (スコア: {data['適性スコア']}/10)"):
                                    st.write(f"**理由**: {data['理由']}")
                        
                        if "overall_assessment" in result:
                            st.subheader("📝 総合評価")
                            st.write(result["overall_assessment"])
                        
                        if "raw_response" in result:
                            st.subheader("🤖 AI分析結果")
                            st.write(result["raw_response"])
                    else:
                        st.error(f"❌ エラー: {result.get('error')}")
            else:
                st.error("❌ 強みと経験は必須入力です")

def essay_generation_page():
    st.header("📝 ES生成・改善")
    st.markdown("AI があなたの情報を基に魅力的なES文章を生成・改善します。")
    
    tab1, tab2, tab3 = st.tabs(["✨ 自己PR生成", "🎯 志望動機生成", "✏️ 文章改善"])
    
    with tab1:
        st.subheader("✨ 自己PR生成")
        
        with st.form("self_pr_form"):
            col1, col2 = st.columns(2)
            with col1:
                strengths = st.text_area("💪 あなたの強み", key="pr_strengths")
                experiences = st.text_area("📚 具体的なエピソード", key="pr_experiences")
            
            with col2:
                target_company = st.text_input("🏢 対象企業（任意）", key="pr_company")
                achievements = st.text_area("🏆 成果・学び", key="pr_achievements")
            
            generate_pr = st.form_submit_button("🚀 自己PR生成", type="primary")
            
            if generate_pr and strengths and experiences:
                generator = EssayGenerator()
                user_info = {
                    "strengths": strengths,
                    "experiences": experiences,
                    "achievements": achievements
                }
                
                with st.spinner("自己PRを生成中..."):
                    result = generator.generate_self_pr(user_info, target_company)
                    
                    if result["status"] == "success":
                        st.success("✅ 自己PR生成完了！")
                        st.subheader("📄 生成された自己PR")
                        st.write(result["self_pr"])
                        
                        # コピー用のテキストエリア
                        st.text_area("📋 コピー用", value=result["self_pr"], height=150)
                    else:
                        st.error(f"❌ エラー: {result.get('error')}")
    
    with tab2:
        st.subheader("🎯 志望動機生成")
        st.info("企業分析機能と連携して、より精度の高い志望動機を生成します。")
        
        company_name = st.text_input("🏢 企業名", key="motivation_company")
        user_experiences = st.text_area("📚 関連する経験・興味", key="motivation_exp")
        
        if st.button("🚀 志望動機生成", key="gen_motivation"):
            if company_name and user_experiences:
                generator = EssayGenerator()
                analyzer = CompanyAnalyzer()
                
                with st.spinner("企業分析と志望動機を生成中..."):
                    company_info = analyzer.analyze(company_name)
                    user_info = {"experiences": user_experiences}
                    
                    motivation = generator.generate_motivation_letter(company_info, user_info)
                    
                    st.success("✅ 志望動機生成完了！")
                    st.subheader("📄 生成された志望動機")
                    st.write(motivation)
    
    with tab3:
        st.subheader("✏️ 文章改善・添削")
        
        essay_text = st.text_area("📝 改善したいES文章を入力してください", height=200)
        essay_type = st.selectbox("📋 文章の種類", ["自己PR", "志望動機", "学生時代に力を入れたこと", "その他"])
        
        if st.button("🔍 文章改善実行", type="primary"):
            if essay_text:
                generator = EssayGenerator()
                
                with st.spinner("文章を分析・改善中..."):
                    result = generator.improve_essay(essay_text, essay_type)
                    
                    if "scores" in result:
                        st.success("✅ 改善提案完了！")
                        
                        # スコア表示
                        st.subheader("📊 評価スコア")
                        col1, col2, col3, col4, col5 = st.columns(5)
                        
                        with col1:
                            st.metric("構成", f"{result['scores']['structure']}/10")
                        with col2:
                            st.metric("具体性", f"{result['scores']['specificity']}/10")
                        with col3:
                            st.metric("独自性", f"{result['scores']['uniqueness']}/10")
                        with col4:
                            st.metric("志望度", f"{result['scores']['motivation']}/10")
                        with col5:
                            st.metric("文章力", f"{result['scores']['writing']}/10")
                        
                        # 改善提案
                        if "improvements" in result:
                            st.subheader("💡 改善提案")
                            for improvement in result["improvements"]:
                                with st.expander(f"🔧 {improvement['category']}"):
                                    st.write(f"**問題点**: {improvement['issue']}")
                                    st.write(f"**改善案**: {improvement['suggestion']}")
                        
                        # 改善版文章
                        if "revised_text" in result:
                            st.subheader("✨ 改善版文章")
                            st.write(result["revised_text"])
                    else:
                        st.write(result.get("raw_response", "改善提案を生成できませんでした"))

def interview_prep_page():
    st.header("💬 面接対策")
    st.markdown("企業・業界別の想定質問生成と回答テンプレート作成で面接準備をサポート")
    
    tab1, tab2 = st.tabs(["❓ 想定質問生成", "🎤 模擬面接"])
    
    with tab1:
        st.subheader("❓ 想定質問生成")
        
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("🏢 企業名", key="interview_company")
            industry = st.text_input("🏭 業界", key="interview_industry", placeholder="IT、金融、商社など")
        
        with col2:
            job_type = st.selectbox("💼 職種", ["総合職", "技術職", "営業職", "企画職", "その他"])
        
        if st.button("🔍 想定質問生成", type="primary"):
            if company_name and industry:
                prep = InterviewPrep()
                
                with st.spinner("想定質問を生成中..."):
                    questions = prep.generate_questions(company_name, industry, job_type)
                    
                    if questions and not questions[0].get("error"):
                        st.success("✅ 想定質問生成完了！")
                        
                        # カテゴリ別に質問を表示
                        categories = {}
                        for q in questions:
                            category = q.get("category", "その他")
                            if category not in categories:
                                categories[category] = []
                            categories[category].append(q)
                        
                        for category, qs in categories.items():
                            with st.expander(f"📋 {category} ({len(qs)}問)"):
                                for i, q in enumerate(qs, 1):
                                    difficulty_color = {"低": "🟢", "中": "🟡", "高": "🔴"}
                                    difficulty_icon = difficulty_color.get(q.get("difficulty", "中"), "⚪")
                                    st.write(f"{i}. {difficulty_icon} {q['question']}")
                    else:
                        st.error("質問生成中にエラーが発生しました")
    
    with tab2:
        st.subheader("🎤 模擬面接")
        st.info("💡 質問に対する回答を入力すると、AIがフィードバックを提供します")
        
        # 簡易的な模擬面接実装
        sample_questions = [
            "自己紹介をお願いします",
            "なぜ当社を志望するのですか？",
            "あなたの強みは何ですか？"
        ]
        
        selected_question = st.selectbox("📝 練習したい質問を選択", sample_questions)
        user_answer = st.text_area("💭 あなたの回答", height=150, placeholder="ここに回答を入力してください...")
        
        if st.button("📊 回答評価", type="primary"):
            if user_answer:
                prep = InterviewPrep()
                
                with st.spinner("回答を評価中..."):
                    # 単一質問の評価
                    feedback = prep._evaluate_answer(selected_question, user_answer)
                    
                    st.success("✅ 評価完了！")
                    
                    if "raw_feedback" in feedback:
                        st.write(feedback["raw_feedback"])
                    else:
                        st.subheader("📊 評価結果")
                        st.json(feedback)

if __name__ == "__main__":
    main()