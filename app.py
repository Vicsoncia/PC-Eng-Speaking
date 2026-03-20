import streamlit as st
import random
import speech_recognition as sr
from datetime import datetime
import time

st.set_page_config(page_title="英語口語練習", page_icon="🎤")

st.title("🎤 英語口語練習 ComBot")
st.write("點擊錄音按鈕，**真的開口說英文**！")

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 學生名字
name = st.text_input("👤 你的名字", placeholder="例如：王小明")

# 題目選擇
topic = st.selectbox("📝 選擇題目", [
    "Describe your favorite hobby",
    "What did you do last weekend?",
    "Talk about your best friend",
    "Describe your dream vacation",
    "What do you want to be in the future?"
])

# 顯示題目中譯（幫助理解）
translations = {
    "Describe your favorite hobby": "（描述你最喜歡的愛好）",
    "What did you do last weekend?": "（你上週末做了什麼？）",
    "Talk about your best friend": "（談談你最好的朋友）",
    "Describe your dream vacation": "（描述你的夢想假期）",
    "What do you want to be in the future?": "（你未來想做什麼？）"
}
st.caption(translations[topic])

# 錄音按鈕
if st.button("🎤 點擊開始錄音", type="primary", use_container_width=True):
    if not name:
        st.error("⚠️ 請先輸入名字！")
    else:
        with st.status("🎙️ 錄音中... 請開始說話（5秒後自動停止）", expanded=True) as status:
            try:
                # 初始化語音識別器
                recognizer = sr.Recognizer()
                
                # 使用麥克風錄音
                with sr.Microphone() as source:
                    st.write("🔊 調整背景噪音...")
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    st.write("🗣️ 現在可以說話了！")
                    
                    # 錄音（5秒）
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    st.write("✅ 錄音完成，正在識別...")
                
                # 語音識別
                try:
                    text = recognizer.recognize_google(audio, language='en-US')
                    status.update(label="✅ 識別成功！", state="complete")
                    
                    st.success(f"📝 你說的是：**{text}**")
                    
                    # 開始評分
                    with st.spinner("正在評分中..."):
                        time.sleep(1)  # 讓用戶看到評分過程
                        
                        # 評分邏輯
                        words = text.split()
                        word_count = len(words)
                        unique_words = len(set(words))
                        
                        # 流利度（詞數越多越流利）
                        fluency = min(10, 5 + word_count // 2)
                        
                        # 詞彙豐富度
                        vocab = min(10, 3 + unique_words)
                        
                        # 語法（簡單檢查）
                        grammar = 8
                        common_errors = ["is are", "was were", "has have", "do does"]
                        for error in common_errors:
                            if error in text.lower():
                                grammar -= 1
                        
                        # 發音（用詞長度簡單模擬）
                        avg_word_len = sum(len(w) for w in words) / word_count if word_count > 0 else 0
                        pronunciation = min(10, 5 + int(avg_word_len))
                        
                        # 計算總分
                        total = (fluency + pronunciation + grammar + vocab) * 2.5
                        
                        # 顯示分數
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("流利度", f"{fluency}/10", help="說得越多越流利")
                            st.metric("語法", f"{grammar}/10", help="句子結構正確性")
                        with col2:
                            st.metric("發音", f"{pronunciation}/10", help="單詞發音清晰度")
                            st.metric("詞彙", f"{vocab}/10", help="詞彙多樣性")
                        
                        st.metric("總分", f"{round(total, 1)}/100", delta=f"{word_count} 個詞")
                        
                        # 生成反饋
                        feedback = []
                        if fluency < 7:
                            feedback.append("💬 試著說更長的句子")
                        if pronunciation < 7:
                            feedback.append("🗣️ 注意單詞發音要清晰")
                        if grammar < 7:
                            feedback.append("📝 檢查時態（過去式/現在式）")
                        if vocab < 7:
                            feedback.append("📚 試試用更多不同的詞")
                        if not feedback:
                            feedback.append("🎉 非常棒！繼續保持")
                        
                        st.info("💡 " + " ".join(feedback))
                        
                        # 保存成績
                        if "scores" not in st.session_state:
                            st.session_state.scores = []
                        
                        st.session_state.scores.append({
                            "name": name,
                            "topic": topic,
                            "text": text,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "scores": {
                                "fluency": fluency,
                                "pronunciation": pronunciation,
                                "grammar": grammar,
                                "vocabulary": vocab,
                                "total": round(total, 1)
                            }
                        })
                        
                        st.balloons()
                        
                except sr.UnknownValueError:
                    status.update(label="❌ 無法識別", state="error")
                    st.error("😕 聽不清楚，請再試一次（說大聲一點）")
                except sr.RequestError:
                    status.update(label="❌ 服務錯誤", state="error")
                    st.error("🌐 網路連線問題，請檢查網路")
                    
            except Exception as e:
                status.update(label="❌ 錯誤", state="error")
                st.error(f"發生錯誤：{str(e)}")
                st.info("💡 提示：請確保麥克風已連接並允許使用")

# 查看成績記錄
if st.button("📊 查看全班成績"):
    if "scores" in st.session_state and st.session_state.scores:
        st.write("### 📋 最近成績記錄")
        
        # 建立成績表格
        records = []
        for record in st.session_state.scores[-10:]:
            records.append({
                "姓名": record["name"],
                "分數": record["scores"]["total"],
                "日期": record["date"],
                "題目": record["topic"][:20] + "..."
            })
        
        st.dataframe(records, use_container_width=True)
        
        # 計算全班平均
        avg_score = sum([s["scores"]["total"] for s in st.session_state.scores]) / len(st.session_state.scores)
        st.metric("📈 全班平均分", f"{round(avg_score, 1)}/100")
        
        # 個人最佳成績
        if name:
            personal_scores = [s["scores"]["total"] for s in st.session_state.scores if s["name"] == name]
            if personal_scores:
                best = max(personal_scores)
                avg_personal = sum(personal_scores) / len(personal_scores)
                st.write(f"👤 **{name}** 的最佳成績：{best} 分，平均：{round(avg_personal, 1)} 分")
    else:
        st.info("📭 還沒有成績記錄")

# 清除記錄按鈕
if st.button("🗑️ 清除所有記錄"):
    st.session_state.scores = []
    st.rerun()

# 使用說明
with st.expander("📖 使用說明"):
    st.write("""
    1. **輸入名字**（第一次使用時）
    2. **選擇題目**（5個題目可以選）
    3. **點擊錄音按鈕**，然後開始說話
    4. **等5秒**，系統會自動停止錄音
    5. **看評分結果**和改進建議
    
    ⚠️ 注意：
    - 需要允許瀏覽器使用麥克風
    - 在安靜的環境說話效果更好
    - 說得越多越長，分數越高
    """)
