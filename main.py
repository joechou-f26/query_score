import streamlit as st
import pandas as pd

# 載入資料檔案
COURSE_FILE = "course_list.xlsx"
SCORE_FILE = "score.xlsx"

st.title("📘 學生成績查詢")

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
        #st.dataframe(score_df)
        
        # 檢查必要欄位
        if '學號' not in score_df.columns:
            st.error("錯誤：找不到『學號』欄位 !")
            st.stop()

        # 過濾該學號的資料
        student_row = score_df[score_df['學號'].astype(str).str.upper() == student_id.strip().upper()]
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
            st.dataframe(student_row)
    except Exception as e:
        st.error(f"讀取成績資料時發生錯誤：{e}")

