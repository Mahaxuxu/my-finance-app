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

# ---- 預計收入 摺疊區 ----
with st.expander("預計收入 (未來特定單筆收入)", expanded=True):
    income_total_placeholder = st.empty()
    
    default_incomes = pd.DataFrame([
        {"項目名稱": "過年紅包", "金額": 1000, "預計收入日期": datetime.date.today() + datetime.timedelta(days=60), "選入計算": True},
    ])
    
    edited_incomes_df = st.data_editor(
        default_incomes,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "項目名稱": st.column_config.TextColumn("第一項：項目名稱"),
            "金額": st.column_config.NumberColumn("第二項：金額 (元)", min_value=0, step=50),
            "預計收入日期": st.column_config.DateColumn(
                "第三項：預計收入日期 (點擊彈出日曆)",
                min_value=datetime.date.today(),
                format="YYYY-MM-DD"
            ),
            "選入計算": st.column_config.CheckboxColumn("選入計算")
        },
        key="incomes_table"
    )
    
    edited_incomes_df["選入計算"] = edited_incomes_df["選入計算"].fillna(False).astype(bool)
    active_incomes = edited_incomes_df[edited_incomes_df["選入計算"] == True].copy()
    
    if not active_incomes.empty:
        active_incomes["預計收入日期"] = pd.to_datetime(active_incomes["預計收入日期"]).dt.date
        
    total_future_income = pd.to_numeric(active_incomes["金額"], errors='coerce').fillna(0).sum()
    income_total_placeholder.metric("預計未來收入總計 (已選入)", f"{total_future_income} 元")

st.write("")

# ---- 同理新增：預計開支 摺疊區 (內建日曆選擇器) ----
with st.expander("預計開支 (未來特定單筆開支)", expanded=True):
    expense_total_placeholder = st.empty()
    
    default_expenses = pd.DataFrame([
        {"項目名稱": "補習班教材費", "金額": 500, "預計開支日期": datetime.date.today() + datetime.timedelta(days=30), "選入計算": True},
    ])
    
    edited_expenses_df = st.data_editor(
        default_expenses,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "項目名稱": st.column_config.TextColumn("第一項：項目名稱"),
            "金額": st.column_config.NumberColumn("第二項：金額 (元)", min_value=0, step=50),
            "預計開支日期": st.column_config.DateColumn(
                "第三項：預計開支日期 (點擊彈出日曆)",
                min_value=datetime.date.today(),
                format="YYYY-MM-DD"
            ),
            "選入計算": st.column_config.CheckboxColumn("選入計算")
        },
        key="expenses_table"
    )
    
    edited_expenses_df["選入計算"] = edited_expenses_df["選入計算"].fillna(False).astype(bool)
    active_expenses = edited_expenses_df[edited_expenses_df["選入計算"] == True].copy()
    
    if not active_expenses.empty:
        active_expenses["預計開支日期"] = pd.to_datetime(active_expenses["預計開支日期"]).dt.date
        
    total_future_expense = pd.to_numeric(active_expenses["金額"], errors='coerce').fillna(0).sum()
    expense_total_placeholder.metric("預計未來開支總計 (已選入)", f"{total_future_expense} 元")

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

# --- 6. 核心計量算法：升級為雙向現金流時序模擬器 ---
def simulate_timeline(target_val, initial_savings, monthly_savings, active_inc_df, active_exp_df):
    today = datetime.date.today()
    current_savings = initial_savings
    daily_savings = monthly_savings / 30.4
    
    if current_savings >= target_val:
        return 0, today
        
    # 建立收入字典
    if not active_inc_df.empty:
        income_by_date = active_inc_df.groupby("預計收入日期")["金額"].sum().to_dict()
    else:
        income_by_date = {}
        
    # 建立開支字典
    if not active_exp_df.empty:
        expense_by_date = active_exp_df.groupby("預計開支日期")["金額"].sum().to_dict()
    else:
        expense_by_date = {}
        
    max_days = 3650
    
    for day in range(1, max_days + 1):
        sim_date = today + datetime.timedelta(days=day)
        current_savings += daily_savings
        
        # 捕捉當天是否有單筆收入注入
        if sim_date in income_by_date:
            current_savings += income_by_date[sim_date]
            
        # 捕捉當天是否有單筆開支扣除
        if sim_date in expense_by_date:
            current_savings -= expense_by_date[sim_date]
            
        if current_savings >= target_val:
            return day, sim_date
            
    return max_days, today + datetime.timedelta(days=max_days)

# --- 7. 看板渲染 ---
st.write("")
st.header("第二步：動態回測與邊際效益分析看板")

base_savings = income - total_essential - total_discretionary

if base_savings <= 0:
    st.error("預算超支警告：你每月的總開銷已經超過了你的收入！請點開上方摺疊盒刪減非必須開支。")
else:
    # 將收入與開支同時傳入模擬器中
    base_days, predicted_date = simulate_timeline(target_value, total_savings, base_savings, active_incomes, active_expenses)
    base_months = base_days / 30.4
    
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
    
    for i, s in enumerate(s_percentages):
        saved_amount = total_discretionary * s  
        new_discretionary = total_discretionary * (1 - s)
        new_savings = income - total_essential - new_discretionary
        
        # 不同省錢情境下同步加入雙向現金流模擬
        new_days, scenario_date = simulate_timeline(target_value, total_savings, new_savings, active_incomes, active_expenses)
        days_saved = base_days - new_days
        
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
        
        if selected_trend and "selection" in selected_trend and selected_trend["selection"]["points"]:
            pt = selected_trend["selection"]["points"][0]
            click_x = pt['x']
            
            matched_row = df_trend[df_trend["節省比例"] == click_x].iloc[0]
            exact_money = matched_row["具體金額數值"]
            exact_date = matched_row["具體日期"]
            days_ahead = matched_row["累積提前天數"]
            
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
