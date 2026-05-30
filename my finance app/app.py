import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="中學生智慧理財系統", layout="wide")

# ---- 1. 每個月的收入 (單獨一行) ----
st.markdown("### **1. 每個月的收入 / 零花錢總額 (元)**")
income = st.number_input("", min_value=0, value=1500, step=50, label_visibility="collapsed", key="income_input")
st.write("") 

# ---- 2. 目前個人總存款 摺疊區 (單獨一行) ----
with st.expander("2. 點開填寫：目前個人總存款 (元)", expanded=True):
    savings_total_placeholder = st.empty()
    
    default_savings = pd.DataFrame([
        {"存款項目": "銀行/郵局帳戶", "金額": 1000, "選入計算": True},
        {"存款項目": "存錢筒現鈔", "金額": 200, "選入計算": True},
    ])
    
    edited_savings_df = st.data_editor(
        default_savings,
        num_rows="dynamic",
        use_container_width=True,
        key="savings_table"
    )
    
    edited_savings_df["選入計算"] = edited_savings_df["選入計算"].fillna(False).astype(bool)
    active_savings = edited_savings_df[edited_savings_df["選入計算"] == True]
    total_savings = pd.to_numeric(active_savings["金額"], errors='coerce').fillna(0).sum()
    savings_total_placeholder.metric("總存款總計 (已選入)", f"{total_savings} 元")

st.write("") 

# ---- 3. 每月必定消費（剛需）摺疊區 (單獨一行) ----
with st.expander("3. 點開填寫：每月必定消費的開支 (剛需開支)", expanded=True):
    essential_total_placeholder = st.empty()
    
    default_essential = pd.DataFrame([
        {"必備事項": "交通/公車卡", "消費金額": 200, "選入計算": True},
        {"必備事項": "學校午餐", "消費金額": 400, "選入計算": True},
    ])
    
    edited_essential_df = st.data_editor(
        default_essential,
        num_rows="dynamic",
        use_container_width=True,
        key="essential_table"
    )
    
    edited_essential_df["選入計算"] = edited_essential_df["選入計算"].fillna(False).astype(bool)
    active_essential = edited_essential_df[edited_essential_df["選入計算"] == True]
    total_essential = pd.to_numeric(active_essential["消費金額"], errors='coerce').fillna(0).sum()
    essential_total_placeholder.metric("必定消費總計 (已選入)", f"{total_essential} 元")

st.write("")

# ---- 4. 每月自我意願消費（非剛需）摺疊區 (單獨一行) ----
with st.expander("4. 點開填寫：每月自我意願消費 (娛樂開支)", expanded=True):
    discretionary_total_placeholder = st.empty()
    
    default_discretionary = pd.DataFrame([
        {"娛樂事項": "手搖飲", "消費金額": 150, "選入計算": True},
        {"娛樂事項": "手遊/Steam", "消費金額": 200, "選入計算": True},
    ])
    
    edited_discretionary_df = st.data_editor(
        default_discretionary,
        num_rows="dynamic",
        use_container_width=True,
        key="discretionary_table"
    )
    
    edited_discretionary_df["選入計算"] = edited_discretionary_df["選入計算"].fillna(False).astype(bool)
    active_discretionary = edited_discretionary_df[edited_discretionary_df["選入計算"] == True]
    total_discretionary = pd.to_numeric(active_discretionary["消費金額"], errors='coerce').fillna(0).sum()
    discretionary_total_placeholder.metric("自我意願總計 (已選入)", f"{total_discretionary} 元")

st.write("") 
st.divider()

# ---- 5. 夢想目標輸入區 (單獨一行) ----
st.markdown("### **5. 存錢想買的東西以及金額**")
target_name = st.text_input("你想買的夢想物品名稱", value="最新款降噪耳機")
target_value = st.number_input("該物品的目標價值 (元)", min_value=1, value=3000, step=100)

# --- 6. 後端計量算法與圖表渲染 ---
st.write("")
st.header("第二步：動態回測與邊際效益分析看板")

base_savings = income - total_essential - total_discretionary
needed_amount = target_value - total_savings

if base_savings <= 0:
    st.error(f"預算超支警告：你每月的總開銷已經超過了你的收入！請點開上方摺疊盒刪減非必須開支。")
else:
    if needed_amount <= 0:
        base_months = 0.0
        base_days = 0.0
        st.success(f"目前選入的總存款已足夠購買此物品，無需額外等待儲蓄時間。")
    else:
        base_months = needed_amount / base_savings
        base_days = base_months * 30.4
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.metric(label="每月淨儲蓄", value=f"{round(base_savings)} 元")
    with col_kpi2:
        st.metric(label="預計解鎖時間", value=f"{round(base_days)} 天", delta=f"{round(base_months, 1)} 個月", delta_color="inverse")
        
    s_percentages = [i / 10.0 for i in range(0, 11)]
    sensitivity_data = []
    marginal_data = []
    prev_days = base_days 
    
    for i, s in enumerate(s_percentages):
        new_discretionary = total_discretionary * (1 - s)
        new_savings = income - total_essential - new_discretionary
        
        if needed_amount <= 0:
            new_days = 0.0
        else:
            new_months = needed_amount / new_savings
            new_days = new_months * 30.4
            
        days_saved = base_days - new_days
        
        sensitivity_data.append({"節省比例": f"{int(s * 100)}%", "累積提前天數": round(days_saved)})
        if i > 0:
            marginal_data.append({"節省比例變動 (X)": f"{int(s_percentages[i-1]*100)}% → {int(s*100)}%", "邊際提前天數 (Y)": round(prev_days - new_days, 1)})
        prev_days = new_days

    df_trend = pd.DataFrame(sensitivity_data)
    df_marginal = pd.DataFrame(marginal_data)
    
    graph_col1, graph_col2 = st.columns(2)
    with graph_col1:
        st.subheader("累積儲
