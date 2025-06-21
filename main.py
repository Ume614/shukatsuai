import streamlit as st
import os
import json
from dotenv import load_dotenv
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
    st.markdown("**就活生向けAI支援ツール** - 企業分析から面接対策まで一貫サポート")
    
    # Sidebar for navigation
    st.sidebar.title("📋 メニュー")
    page = st.sidebar.selectbox(
        "機能選択",
        ["🏠 ホーム", "🏢 企業分析", "🎯 業界適性診断", "📝 ES生成・改善", "💬 面接対策"]
    )
    
    if page == "🏠 ホーム":
        home_page()
    elif page == "🏢 企業分析":
        company_analysis_page()
    elif page == "🎯 業界適性診断":
        industry_matching_page()
    elif page == "📝 ES生成・改善":
        essay_generation_page()
    elif page == "💬 面接対策":
        interview_prep_page()

def home_page():
    st.header("🏠 就活AIコンパス へようこそ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 主な機能")
        st.markdown("""
        **1. 🏢 企業分析AI**
        - IR情報の自動収集・分析
        - 企業の強み・弱み抽出
        - 業界内ポジション分析
        
        **2. 🎯 業界適性診断**
        - 個人プロフィール分析
        - 10業界との適性マッチング
        - おすすめキャリアパス提案
        
        **3. 📝 ES生成・改善**
        - AI による自己PR生成
        - 志望動機の自動作成
        - 文章添削・改善提案
        
        **4. 💬 面接対策**
        - 企業別想定質問生成
        - 回答テンプレート作成
        - 模擬面接フィードバック
        """)
    
    with col2:
        st.subheader("🎯 使い方")
        st.markdown("""
        **Step 1:** 左のメニューから機能を選択
        
        **Step 2:** 必要な情報を入力
        
        **Step 3:** AIが分析・生成を実行
        
        **Step 4:** 結果を確認・活用
        """)
        
        st.info("💡 **ヒント**: まずは「企業分析」から始めて、興味のある企業を深く理解しましょう！")

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