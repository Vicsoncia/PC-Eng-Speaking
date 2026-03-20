import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="英語口語練習", page_icon="🎤")

st.title("🎤 英語口語練習 ComBot")
st.write("點擊按鈕，用英文回答問題")

# 學生名字
name = st.text_input("你的名字", placeholder="例如：王小明")

# 題目選擇
topic = st.selectbox("選擇題目", [
    "Describe your favorite hobby (描述你最喜歡的愛好)",
    "What did you do last weekend? (你上週末做了什麼？)",
    "Talk about your best friend (談談你最好的朋友)"
])

# 錄音按鈕（模擬錄音）
if st.button("🎤 開始錄音", type="primary"):
    with st.spinner("錄音中...請說話"):
        import time
        time.sleep(2)
    
    # 模擬語音識別結果
    texts = {
        "Describe your favorite hobby (描述你最喜歡的愛好)": "I like playing basketball because it's fun and I can play with my friends.",
        "What did you do last weekend? (你上週末做了什麼？)": "I went to the park with my family and we had a picnic.",
        "Talk about your best friend (談談你最好的朋友)": "My best friend is very kind and always helps me with my homework."
    }
    text = texts[topic]
    
    st.success("識別完成！")
    st.write(f"📝 你說的是：**{text}**")
    
    # 隨機評分（但保持合理範圍）
    fluency = random.randint(7, 10)
    pronunciation = random.randint(7, 10)
    grammar = random.randint(7, 10)
    vocabulary = random.randint(7, 10)
    total = (fluency + pronunciation + grammar + vocabulary) * 2.5
    
    # 顯示分數（用好看的格子）
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("流利度", f"{fluency}/10")
    with col2:
        st.metric("發音", f"{pronunciation}/10")
    with col3:
        st.metric("語法", f"{grammar}/10")
    with col4:
        st.metric("詞彙", f"{vocabulary}/10")
    
    st.metric("總分", f"{round(total, 1)}/100", delta_color="off")
    
    # 生成反饋建議
    feedback = []
    if fluency < 8:
        feedback.append("💬 試著說得更流暢，減少停頓")
    if pronunciation < 8:
        feedback.append("🗣️ 注意單詞發音")
    if grammar < 8:
        feedback.append("📝 檢查時態和主謂一致")
    if vocabulary < 8:
        feedback.append("📚 嘗試用更多樣的詞彙")
    if not feedback:
        feedback.append("🎉 太棒了！繼續保持")
    
    st.info("💡 改進建議：" + " ".join(feedback))
    
    # 保存成績（存在雲端）
    if name:
        try:
            # 這裡用 st.session_state 模擬數據庫
            if "scores" not in st.session_state:
                st.session_state.scores = []
            st.session_state.scores.append({
                "name": name,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "score": round(total, 1)
            })
            st.success(f"✅ {name} 的成績已保存！")
        except:
            st.error("保存失敗")

# 查看班級統計
if st.button("📊 查看全班成績"):
    if "scores" in st.session_state and st.session_state.scores:
        st.write("### 最近成績記錄")
        for record in st.session_state.scores[-10:]:  # 顯示最近10筆
            st.write(f"**{record['name']}**：{record['score']} 分 ({record['date']})")
        
        # 計算平均分
        avg = sum([s["score"] for s in st.session_state.scores]) / len(st.session_state.scores)
        st.metric("全班平均分", f"{round(avg, 1)}/100")
    else:
        st.info("還沒有成績記錄")
