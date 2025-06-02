import streamlit as st
import pandas as pd

# ====== 設定檔案路徑 ======
COURSE_FILE = "course_list.xlsx"
SCORE_FILE = "score.xlsx"

# ====== 密碼驗證 ======
st.title("🔐 學生成績查詢")
correct_password = "1132"
password = st.text_input("請輸入密碼：", type="password")

if password != correct_password:
    st.warning("請輸入正確密碼才能進行查詢。")
    st.stop()

# ====== 讀取課程清單 ======
try:
    course_df = pd.read_excel(COURSE_FILE)
    course_list = course_df.iloc[:, 0].dropna().tolist()
    selected_course = st.selectbox("請選擇科目：", course_list)
except Exception as e:
    st.error(f"無法讀取 course_list.xlsx，錯誤訊息：{e}")
    st.stop()

# ====== 快取單一工作表的函數 ======
@st.cache_data
def load_score_sheet(sheet_name):
    return pd.read_excel(SCORE_FILE, sheet_name=sheet_name)

# ====== 使用者輸入學號 ======
student_id = st.text_input("請輸入學號：")

if st.button("查詢"):
    try:
        score_df = load_score_sheet(selected_course)

        if "學號" not in score_df.columns:
            st.error("錯誤：找不到欄位『學號』")
            st.stop()

        student_row = score_df[score_df["學號"].astype(str).str.upper() == student_id.strip().upper()]
        if student_row.empty:
            st.warning("查無此學號成績!")
        else:
            # 計算平均成績（排除學號、姓名等文字欄位）
            score_only = student_row.drop(columns=['學號', '姓名','期中考'], errors='ignore')  #只做小考平均
            score_only = score_only.apply(pd.to_numeric, errors='coerce')
            avg_score = score_only.mean(axis=1).round(2)
            cnt_score=len(score_only.columns)
            
            # 加上平均分數欄（放在第 2 個欄位，也就是 學號 和 姓名 之後）
            student_row = student_row.copy()
            student_row.insert(2, '小考平均', avg_score)  # index=2 表示放在第 3 欄
            student_row.insert(3, '小考次數', cnt_score)  
            
            # 顯示成績
            st.subheader("🔎 查詢結果")
            st.dataframe(student_row, hide_index=True)

    except Exception as e:
        st.error(f"查詢過程中發生錯誤：{e}")
