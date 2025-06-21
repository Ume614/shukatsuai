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
    
    st.title("🎯 就活AIコンパス")
    st.markdown("**就活生向けAI支援ツール** - 企業分析から始まる一貫した就活支援")
    
    # ワークフロー状態の初期化
    if 'workflow' not in st.session_state:
        st.session_state.workflow = IntegratedWorkflow()
    
    # Sidebar for navigation
    st.sidebar.title("📋 メニュー")
    page = st.sidebar.selectbox(
        "機能選択",
        ["🏠 ホーム", "🎯 統合ワークフロー", "🏢 企業分析", "👤 業界適性診断", "📝 ES生成・改善", "💬 面接対策"]
    )
    
    if page == "🏠 ホーム":
        home_page()
    elif page == "🎯 統合ワークフロー":
        integrated_workflow_page()
    elif page == "🏢 企業分析":
        company_analysis_page()
    elif page == "👤 業界適性診断":
        industry_matching_page()
    elif page == "📝 ES生成・改善":
        essay_generation_page()
    elif page == "💬 面接対策":
        interview_prep_page()

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
            
            if st.form_submit_button("📊 パーソナリティ分析実行", type="primary"):
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
    st.header("🏠 就活AIコンパス へようこそ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 新機能: 統合ワークフロー")
        st.markdown("""
        **企業分析から始まる一貫したプロセス:**
        
        **1. 🏢 企業分析 → 求める人物像特定**
        **2. 👤 あなたのパーソナリティ定義**
        **3. 🔍 ギャップ分析・改善提案**
        **4. 📝 最適化されたES生成**
        **5. 💬 戦略的面接対策**
        
        すべてが繋がった効果的な就活準備が可能です！
        """)
        
        st.info("🚀 **おすすめ**: 「統合ワークフロー」で体系的な就活準備を始めましょう！")
    
    with col2:
        st.subheader("🛠 個別機能")
        st.markdown("""
        **🏢 企業分析AI**
        - IR情報の自動分析
        - 企業の強み・弱み抽出
        
        **👤 業界適性診断**
        - 10業界との適性マッチング
        - キャリアパス提案
        
        **📝 ES生成・改善**
        - AI による文章生成
        - 添削・改善提案
        
        **💬 面接対策**
        - 想定質問生成
        - 模擬面接フィードバック
        """)
        
        st.success("💡 各機能は単独でも利用可能です")

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