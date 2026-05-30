import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="中學生智慧理財系統", layout="wide")

# ---- 1. 每個月的收入 ----
st.markdown("### **1. 每個月的收入 / 零花錢總額 (元)**")
income = st.number_input("", min_value=0, value=1500, step=50, label_visibility="collapsed", key="income_input")
st.write("") 

# ---- 2. 目前個人總存款 摺疊區 ----
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

# ---- 3. 每月必定消費（剛需）摺疊區 ----
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

# ---- 4. 每月自我意願消費（非剛需）摺疊區 ----
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

# ---- 5. 夢想目標輸入區 ----
st.markdown("### **5. 存錢想買的東西以及金額**")
target_name = st.text_input("你想買的夢想物品名稱", value="最新款降噪耳機")
target_value = st.number_input("該物品的目標價值 (元)", min_value=1, value=3000, step=100)

# --- 6. 後端計量算法與圖表渲染 ---
st.write("")
st.header("第二步：動態回測與邊際效益分析看板")

base_savings = income - total_essential - total_discretionary
needed_amount = target_value - total_savings

if base_savings <= 0:
    st.error("預算超支警告：你每月的總開銷已經超過了你的收入！請點開上方摺疊盒刪減非必須開支。")
else:
    if needed_amount <= 0:
        base_months = 0.0
        base_days = 0.0
        predicted_date = datetime.date.today()
        st.success("目前選入的總存款已足夠購買此物品，無需額外等待儲蓄時間。")
    else:
        base_months = needed_amount / base_savings
        base_days = base_months * 30.4
        predicted_date = datetime.date.today() + datetime.timedelta(days=int(base_days))
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.metric(label="每月淨儲蓄", value=f"{round(base_savings)} 元")
    with col_kpi2:
        st.metric(label="預計解鎖時間", value=f"{round(base_days)} 天", delta=f"{round(base_months, 1)} 個月", delta_color="inverse")
        st.markdown(f"### **預測實現日期：{predicted_date.strftime('%Y年%m月%d日')}**")
        
    s_percentages = [i / 10.0 for i in range(0, 11)]
    sensitivity_data = []
    marginal_data = []
    prev_days = base_days 
    
    # 核心算法升級：同時將具體金額與該場景下的精確日期存入 DataFrame
    for i, s in enumerate(s_percentages):
        saved_amount = total_discretionary * s  # 計算該比例下具體省了多少錢
        new_discretionary = total_discretionary * (1 - s)
        new_savings = income - total_essential - new_discretionary
        
        if needed_amount <= 0:
            new_days = 0.0
        else:
            new_months = needed_amount / new_savings
            new_days = new_months * 30.4
            
        days_saved = base_days - new_days
        # 計算在此省錢場景下，未來的具體實現日期
        scenario_date = datetime.date.today() + datetime.timedelta(days=int(new_days))
        
        sensitivity_data.append({
            "節省比例": f"{int(s * 100)}%", 
            "累積提前天數": round(days_saved),
            "具體金額數值": round(saved_amount),
            "具體日期": scenario_date.strftime('%Y年%m月%d日')
        })
        if i > 0:
            marginal_data.append({"節省比例變動 (X)": f"{int(s_percentages[i-1]*100)}% → {int(s*100)}%", "邊際提前天數 (Y)": round(prev_days - new_days, 1)})
        prev_days = new_days

    df_trend = pd.DataFrame(sensitivity_data)
    df_marginal = pd.DataFrame(marginal_data)
    
    graph_col1, graph_col2 = st.columns(2)
    
    # ---- 左圖：累積儲蓄效益 ----
    with graph_col1:
        st.subheader("累積儲蓄效益")
        fig_trend = px.line(df_trend, x="節省比例", y="累積提前天數", markers=True, template="plotly_white")
        fig_trend.update_layout(clickmode='event+select')
        
        selected_trend = st.plotly_chart(fig_trend, on_select="rerun", use_container_width=True, key="trend_chart")
        
        # 點擊聯動邏輯升級：動態反查對應的金額與日期
        if selected_trend and "selection" in selected_trend and selected_trend["selection"]["points"]:
            pt = selected_trend["selection"]["points"][0]
            click_x = pt['x']
            
            # 從資料庫反查對應欄位
            matched_row = df_trend[df_trend["節省比例"] == click_x].iloc[0]
            exact_money = matched_row["具體金額數值"]
            exact_date = matched_row["具體日期"]
            days_ahead = matched_row["累積提前天數"]
            
            # 按照要求的格式完美輸出
            st.info(f"已選中點數據：當省錢比例為 {click_x} （即每個月省下 {exact_money} 元）時，總共可提前 {days_ahead} 天（即在 {exact_date} ）實現目標。")
        else:
            st.caption("提示：點擊上方折線圖中的藍色圓點，可在這裡動態查看該點的數據。")

    # ---- 右圖：邊際省錢效益 ----
    with graph_col2:
        st.subheader("邊際省錢效益")
        fig_marginal = px.bar(df_marginal, x="節省比例變動 (X)", y="邊際提前天數 (Y)", template="plotly_white")
        fig_marginal.update_layout(clickmode='event+select')
        
        selected_marginal = st.plotly_chart(fig_marginal, on_select="rerun", use_container_width=True, key="marginal_chart")
        
        if selected_marginal and "selection" in selected_marginal and selected_marginal["selection"]["points"]:
            pt = selected_marginal["selection"]["points"][0]
            st.info(f"已選中區間數據：{pt['x']} 階段，每多省10%可額外縮短 {pt['y']} 天。")
        else:
            st.caption("提示：點擊上方柱狀圖的長條，可在這裡動態查看該區間的詳細邊際效益。")
