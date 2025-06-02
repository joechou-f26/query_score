import streamlit as st
import pandas as pd

# 載入資料檔案
COURSE_FILE = "course_list.xlsx"
SCORE_FILE = "score.xlsx"

st.title("📘 學生成績查詢系統")

# 讀取課程清單
try:
    course_df = pd.read_excel(COURSE_FILE)
    course_list = course_df.iloc[:, 0].dropna().tolist()
    selected_course = st.selectbox("請選擇科目：", course_list)
except Exception as e:
    st.error(f"無法讀取 course_list.xlsx，錯誤訊息：{e}")
    st.stop()

# 輸入學號
student_id = st.text_input("請輸入學號：")

# 查詢按鈕
if st.button("查詢"):
    try:
        # 讀取該科目對應的工作表
        score_df = pd.read_excel(SCORE_FILE, sheet_name=selected_course)

        # 檢查必要欄位
        if 'id' not in score_df.columns:
            st.error("錯誤：找不到欄位『學號』欄位")
            st.stop()

        # 過濾該學號的資料
        #student_row = score_df[score_df['id'].astype(str) == student_id.strip()]
        student_row = score_df[score_df['id'].astype(str).str.upper() == student_id.strip().upper()]
        if student_row.empty:
            st.warning("查無此學號成績")
        else:
            # 計算平均成績（排除學號、姓名等文字欄位）
            score_only = student_row.drop(columns=['id', 'name','MidTerm'], errors='ignore')  #只做小考平均
            score_only = score_only.apply(pd.to_numeric, errors='coerce')
            avg_score = score_only.mean(axis=1).round(2)

            # 加上平均分數欄
            student_row = student_row.copy()
            student_row['小考平均分數'] = avg_score

            # 顯示成績
            st.subheader("🔎 查詢結果")
            st.dataframe(student_row)
    except Exception as e:
        st.error(f"讀取成績資料時發生錯誤：{e}")

