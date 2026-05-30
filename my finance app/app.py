import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="中學生智慧理財系統", layout="wide")

# ---- 1. 零用錢收入配置 (預設初始化為：每周發放 300 元) ----
st.markdown("### **1. 零用錢收入配置**")
col_freq, col_amt = st.columns([1, 2])

with col_freq:
    inc_freq = st.selectbox("請選擇收入發放週期：", ["每日發放", "每周發放", "每月發放"], index=1, key="inc_freq_select")

with col_amt:
    if inc_freq == "每日發放":
        raw_income = st.number_input("請輸入每日零用錢金額 (元)：", min_value=0, value=50, step=10, key="income_daily")
        income = raw_income * 30.4
    elif inc_freq == "每周發放":
        raw_income = st.number_input("請輸入每周零用錢金額 (元)：", min_value=0, value=300, step=50, key="income_weekly")
        income = raw_income * (30.4 / 7)
    else:
        raw_income = st.number_input("請輸入每月零用錢金額 (元)：", min_value=0, value=1500, step=50, key="income_monthly")
        income = raw_income

st.caption(f"系統後台已自動將其標準化換算為每月等值收入：約 {round(income)} 元")
st.write("") 

# ---- 2. 目前個人總存款 摺疊區 (預設初始化為：總計 8000 元大本金) ----
with st.expander("2. 盤點現有存款現額 (活期與現金)", expanded=True):
    savings_total_placeholder = st.empty()
    
    default_savings = pd.DataFrame([
        {"存款項目": "銀行/郵局帳戶", "金額": 7000, "選入計算": True},
        {"存款項目": "存錢筒現鈔", "金額": 1000, "選入計算": True},
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
    savings_total_placeholder.metric("現有存款總計 (已選入)", f"{total_savings} 元")

st.write("") 

# ---- 預計收入 摺疊區 (預設初始化為：第 3 天極早期注入 3000 元紅包) ----
with st.expander("未來預期單筆收入明細 (如紅包、獎學金)", expanded=True):
    income_total_placeholder = st.empty()
    
    default_incomes = pd.DataFrame([
        {"項目名稱": "過年紅包", "金額": 3000, "預計收入日期": datetime.date.today() + datetime.timedelta(days=3), "選入計算": True},
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
    income_total_placeholder.metric("預期未來收入總計 (已選入)", f"{total_future_income} 元")

st.write("")

# ---- 預計開支 摺疊區 (預設初始化為：30 天後扣除 500 元教材費) ----
with st.expander("未來預期單筆大額開支明細 (如教材費、大宗購買)", expanded=True):
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
    expense_total_placeholder.metric("預期未來開支總計 (已選入)", f"{total_future_expense} 元")

st.write("")

# ---- 3. 每月必定消費 摺疊區 (預設初始化為：必要生活開支 500 元) ----
with st.expander("3. 每月必要生活開支統計 (剛需消費)", expanded=True):
    essential_total_placeholder = st.empty()
    
    default_essential = pd.DataFrame([
        {"必備事項": "午餐/公車", "消費金額": 500, "選入計算": True},
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
    essential_total_placeholder.metric("必要開支總計 (已選入)", f"{total_essential} 元")

st.write("")

# ---- 4. 每月自我意願消費 摺疊區 (預設初始化為：娛樂預算共 400 元) ----
with st.expander("4. 每月非必要娛樂開支預算 (彈性消費)", expanded=True):
    discretionary_total_placeholder = st.empty()
    
    default_discretionary = pd.DataFrame([
        {"娛樂事項": "手搖飲", "消費金額": 150, "選入計算": True},
        {"娛樂事項": "遊戲", "消費金額": 250, "選入計算": True},
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
    discretionary_total_placeholder.metric("娛樂開支總計 (已選入)", f"{total_discretionary} 元")

st.write("") 
st.sidebar.markdown(f"**演示提示**：目前已自動代入零錢通最佳效果測試數據組。")
st.style = st.divider()

# ---- 5. 夢想目標輸入區 (預設初始化為：15,000 元高階平板，拉長模擬跨度) ----
st.markdown("### **5. 設定最終儲蓄目標**")
target_name = st.text_input("儲蓄目標物名稱", value="高階全視線平板電腦")
target_value = st.number_input("目標物市場價格 (元)", min_value=1, value=15000, step=100)


# --- 6. 核心計量算法：雙向現金流 + 理財複利時序模擬器 ---
def simulate_timeline(target_val, initial_savings, monthly_savings, active_inc_df, active_exp_df, rate_annual=0.0):
    today = datetime.date.today()
    current_savings = initial_savings
    daily_savings = monthly_savings / 30.4
    
    if current_savings >= target_val:
        return 0, today
        
    inc_dict = active_inc_df.groupby("預計收入日期")["金額"].sum().to_dict() if not active_inc_df.empty else {}
    exp_dict = active_exp_df.groupby("預計開支日期")["金額"].sum().to_dict() if not active_exp_df.empty else {}
    
    max_days = 3650
    daily_rate = (rate_annual / 100) / 365
    
    for day in range(1, max_days + 1):
        sim_date = today + datetime.timedelta(days=day)
        
        current_savings += current_savings * daily_rate
        current_savings += daily_savings
        
        if sim_date in inc_dict:
            current_savings += inc_dict[sim_date]
        if sim_date in exp_dict:
            current_savings -= exp_dict[sim_date]
            
        if current_savings >= target_val:
            return day, sim_date
            
    return max_days, today + datetime.timedelta(days=max_days)


# =========================================================
# 📊 第一大板塊：基礎現狀回測（純儲蓄現狀）
# =========================================================
st.write("")
st.header("數據分析第一階段：常態儲蓄路徑回測 (未配置理財)")

base_savings = income - total_essential - total_discretionary

if base_savings <= 0:
    st.error("預算超支警告：每月總開銷已超過總收入，請回上方重新調整預算。")
else:
    base_days, predicted_date = simulate_timeline(target_value, total_savings, base_savings, active_incomes, active_expenses, 0.0)
    base_months = base_days / 30.4
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.metric(label="每月淨儲蓄本金", value=f"{round(base_savings)} 元")
    with col_kpi2:
        st.metric(label="預估達標時間", value=f"{round(base_days)} 天 ({round(base_months, 1)} 個月)")
        st.markdown(f"### **精確達標日期：{predicted_date.strftime('%Y年%m月%d日')}**")
        
    s_percentages = [i / 10.0 for i in range(0, 11)]
    sensitivity_data = []
    marginal_data = []
    prev_days = base_days 
    
    for i, s in enumerate(s_percentages):
        saved_amount = total_discretionary * s  
        new_discretionary = total_discretionary * (1 - s)
        new_savings = income - total_essential - new_discretionary
        
        new_days, scenario_date = simulate_timeline(target_value, total_savings, new_savings, active_incomes, active_expenses, 0.0)
        days_saved = base_days - new_days
        
        sensitivity_data.append({
            "節省比例": f"{int(s * 100)}%", 
            "累積提前天數": round(days_saved),
            "具體金額數值": round(saved_amount),
            "具體日期": scenario_date.strftime('%Y年%m月%d日')
        })
        if i > 0:
            marginal_data.append({"節省比例變動 (X)": f"{int(s_percentages[i-1]*100)}% → {int(s * 100)}%", "邊際提前天數 (Y)": round(prev_days - new_days, 1)})
        prev_days = new_days

    df_trend = pd.DataFrame(sensitivity_data)
    df_marginal = pd.DataFrame(marginal_data)
    
    graph_col1, graph_col2 = st.columns(2)
    
    with graph_col1:
        st.subheader("縮減娛樂開支的累積加速天數")
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
            st.info(f"數據分析：當非必要開支縮減 {click_x} （相當於每月省下 {exact_money} 元）時，達標時間可提前 {days_ahead} 天（預計於 {exact_date} 達成）。")
        else:
            st.caption("提示：點擊折線圖上的藍色圓點，可直接解鎖該點的具體數據。")

    with graph_col2:
        st.subheader("每多省 10% 娛樂費的邊際效益")
        fig_marginal = px.bar(df_marginal, x="節省比例變動 (X)", y="邊際提前天數 (Y)", template="plotly_white")
        fig_marginal.update_layout(clickmode='event+select')
        selected_marginal = st.plotly_chart(fig_marginal, on_select="rerun", use_container_width=True, key="marginal_chart")
        
        if selected_marginal and "selection" in selected_marginal and selected_marginal["selection"]["points"]:
            pt = selected_marginal["selection"]["points"][0]
            st.info(f"區間數據：在 {pt['x']} 階段，每多省 10% 娛樂費可讓時間再縮短 {pt['y']} 天。")
        else:
            st.caption("提示：點擊柱狀圖的長條，可查看該區間的詳細邊際效益. ")

    st.write("")
    st.markdown("### **開支優化決策：少花這筆，提早幾天？ (常態儲蓄)**")
    if not active_discretionary.empty:
        for idx, row in active_discretionary.iterrows():
            item_name = row["娛樂事項"]
            item_cost = pd.to_numeric(row["消費金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_total_discretionary = total_discretionary - item_cost
            temp_savings = income - total_essential - temp_total_discretionary
            new_days, _ = simulate_timeline(target_value, total_savings, temp_savings, active_incomes, active_expenses, 0.0)
            st.write(f"如果不購買 **{item_name}**（每月省下 {round(item_cost)} 元），我們的 **{target_name}** 達標時間將提早 **{round(base_days - new_days)}** 天。")

    if not active_expenses.empty:
        for idx, row in active_expenses.iterrows():
            item_name = row["項目名稱"]
            item_cost = pd.to_numeric(row["金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_active_expenses = active_expenses.drop(idx)
            new_days, _ = simulate_timeline(target_value, total_savings, base_savings, active_incomes, temp_active_expenses, 0.0)
            st.write(f"如果取消 **{item_name}** 開支（省下 {round(item_cost)} 元），我們的 **{target_name}** 達標時間將提早 **{round(base_days - new_days)}** 天。")


# =========================================================
# 🌟 第二大板塊：全新理財板塊「理財加持」 (預設鎖定為：微信零錢通)
# =========================================================
st.write("")
st.write("")
st.divider()
st.markdown("# **數據分析第二階段：理財增值策略回測**")

tool_options = [
    "無 (不使用理財，年化 0%)", 
    "微信零錢通 (隨存隨取貨幣基金，預設年化 2.0%)", 
    "自定義隨時存取理財"
]
selected_tool = st.selectbox("請選擇要代入模型測試的理財方式：", tool_options, index=1, key="tool_select_box")

if "無" in selected_tool:
    active_rate = 0.0
elif "微信零錢通" in selected_tool:
    active_rate = 2.0
else:
    active_rate = st.number_input("請輸入自定義工具的預估年化收益率 (%)", min_value=0.0, max_value=20.0, value=3.5, step=0.1, key="custom_rate_input")

st.info(f"模型狀態：已套用 {selected_tool.split(' ')[0]}，將以 {active_rate}% 的年化收益率進行每日複利模擬。")


# =========================================================
# 📊 第三大板塊：理財優化後的「動態回測與邊際效益分析看板」
# =========================================================
st.write("")
st.header("理財策略優化後的數據看板")

if base_savings <= 0:
    st.error("預算超支警告：請先修正上方消費數據。")
else:
    base_days_inv, predicted_date_inv = simulate_timeline(target_value, total_savings, base_savings, active_incomes, active_expenses, active_rate)
    base_months_inv = base_days_inv / 30.4
    days_improved = base_days - base_days_inv
    
    col_kpi1_inv, col_kpi2_inv = st.columns(2)
    with col_kpi1_inv:
        st.metric(label="每月投入本金", value=f"{round(base_savings)} 元")
    with col_kpi2_inv:
        st.metric(
            label="優化後達標時間", 
            value=f"{round(base_days_inv)} 天 ({round(base_months_inv, 1)} 個月)", 
            delta=f"比常態儲蓄提早 {round(days_improved)} 天" if days_improved > 0 else "與常態儲蓄持平", 
            delta_color="inverse"
        )
        st.markdown(f"### **優化後達標日期：{predicted_date_inv.strftime('%Y年%m月%d日')}**")

    # ---------------------------------------------------------
    # ⏳ 專屬理財時間軸指南
    # ---------------------------------------------------------
    with st.expander(f"動態模擬時間軸指南 (套用：{selected_tool.split(' ')[0]})", expanded=True):
        inc_by_date_guide = active_incomes.groupby("預計收入日期")["金額"].sum().to_dict() if not active_incomes.empty else {}
        exp_by_date_guide = active_expenses.groupby("預計開支日期")["金額"].sum().to_dict() if not active_expenses.empty else {}
        
        today_g = datetime.date.today()
        current_savings_g = total_savings
        daily_savings_g = base_savings / 30.4
        daily_rate_g = (active_rate / 100) / 365
        
        guide_records = []
        guide_records.append({
            "日期": today_g.strftime('%Y-%m-%d'),
            "存款變動": "0",
            "帳戶總餘額(元)": round(current_savings_g)
        })
        
        for day in range(1, 3651):
            sim_date_g = today_g + datetime.timedelta(days=day)
            
            current_savings_g += current_savings_g * daily_rate_g
            current_savings_g += daily_savings_g
            
            if sim_date_g in inc_by_date_guide:
                inc_amt = inc_by_date_guide[sim_date_g]
                current_savings_g += inc_amt
                guide_records.append({
                    "日期": sim_date_g.strftime('%Y-%m-%d'),
                    "存款變動": f"+{round(inc_amt)}",
                    "帳戶總餘額(元)": round(current_savings_g)
                })
                
            if sim_date_g in exp_by_date_guide:
                exp_amt = exp_by_date_guide[sim_date_g]
                current_savings_g -= exp_amt
                guide_records.append({
                    "日期": sim_date_g.strftime('%Y-%m-%d'),
                    "存款變動": f"-{round(exp_amt)}",
                    "帳戶總餘額(元)": round(current_savings_g)
                })
                
            if current_savings_g >= target_value:
                guide_records.append({
                    "日期": sim_date_g.strftime('%Y-%m-%d'),
                    "存款變動": "目標達成",
                    "帳戶總餘額(元)": round(current_savings_g)
                })
                break
                
        df_guide = pd.DataFrame(guide_records)
        st.dataframe(df_guide, use_container_width=True, hide_index=True)

    # ---------------------------------------------------------
    
    sensitivity_data_inv = []
    marginal_data_inv = []
    prev_days_inv = base_days_inv 
    
    for i, s in enumerate(s_percentages):
        saved_amount = total_discretionary * s  
        new_discretionary = total_discretionary * (1 - s)
        new_savings = income - total_essential - new_discretionary
        
        new_days_inv, scenario_date_inv = simulate_timeline(target_value, total_savings, new_savings, active_incomes, active_expenses, active_rate)
        days_saved_inv = base_days_inv - new_days_inv
        
        sensitivity_data_inv.append({
            "節省比例": f"{int(s * 100)}%", 
            "累積提前天數": round(days_saved_inv),
            "具體金額數值": round(saved_amount),
            "具體日期": scenario_date_inv.strftime('%Y年%m月%d日')
        })
        if i > 0:
            marginal_data_inv.append({"節省比例變動 (X)": f"{int(s_percentages[i-1]*100)}% → {int(s * 100)}%", "邊際提前天數 (Y)": round(prev_days_inv - new_days_inv, 1)})
        prev_days_inv = new_days_inv

    df_trend_inv = pd.DataFrame(sensitivity_data_inv)
    df_marginal_inv = pd.DataFrame(marginal_data_inv)
    
    graph_col1_inv, graph_col2_inv = st.columns(2)
    
    with graph_col1_inv:
        st.subheader("累積儲蓄效益 (理財優化版)")
        fig_trend_inv = px.line(df_trend_inv, x="節省比例", y="累積提前天數", markers=True, template="plotly_white")
        fig_trend_inv.update_layout(clickmode='event+select')
        selected_trend_inv = st.plotly_chart(fig_trend_inv, on_select="rerun", use_container_width=True, key="trend_chart_invest")
        
        if selected_trend_inv and "selection" in selected_trend_inv and selected_trend_inv["selection"]["points"]:
            pt = selected_trend_inv["selection"]["points"][0]
            click_x = pt['x']
            matched_row = df_trend_inv[df_trend_inv["節省比例"] == click_x].iloc[0]
            exact_money = matched_row["具體金額數值"]
            exact_date = matched_row["具體日期"]
            days_ahead = matched_row["累積提前天數"]
            st.info(f"動態解析：當非必要開支縮減 {click_x} （每月省下 {exact_money} 元）且配合 {selected_tool.split(' ')[0]} 時，總共可提前 {days_ahead} 天（預估於 {exact_date} 達標）。")
        else:
            st.caption("提示：點擊上方折線圖中的藍色圓點，可在這裡動態查看該點的數據。")

    with graph_col2_inv:
        st.subheader("邊際省錢效益 (理財優化版)")
        fig_marginal_inv = px.bar(df_marginal_inv, x="節省比例變動 (X)", y="邊際提前天數 (Y)", template="plotly_white")
        fig_marginal_inv.update_layout(clickmode='event+select')
        selected_marginal_inv = st.plotly_chart(fig_marginal_inv, on_select="rerun", use_container_width=True, key="marginal_chart_invest")
        
        if selected_marginal_inv and "selection" in selected_marginal_inv and selected_marginal_inv["selection"]["points"]:
            pt = selected_marginal_inv["selection"]["points"][0]
            st.info(f"區間數據：在 {pt['x']} 階段，每多省 10% 娛樂費並配合理財，可讓時間再縮短 {pt['y']} 天。")
        else:
            st.caption("提示：點擊上方柱狀圖的長條，可在這裡動態查看該區間的詳細邊際效益。")

    st.write("")
    st.markdown("### **開支優化決策：少花這筆，提早幾天？ (理財增值版)**")
    if not active_discretionary.empty:
        for idx, row in active_discretionary.iterrows():
            item_name = row["娛樂事項"]
            item_cost = pd.to_numeric(row["消費金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_total_discretionary = total_discretionary - item_cost
            temp_savings = income - total_essential - temp_total_discretionary
            new_days_inv, _ = simulate_timeline(target_value, total_savings, temp_savings, active_incomes, active_expenses, active_rate)
            st.write(f"如果減少 **{item_name}** 消費（省下 {round(item_cost)} 元）並配合 **{selected_tool.split(' ')[0]}**，我們的解鎖時間將提早 **{round(base_days_inv - new_days_inv)}** 天。")

    if not active_expenses.empty:
        for idx, row in active_expenses.iterrows():
            item_name = row["項目名稱"]
            item_cost = pd.to_numeric(row["金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_active_expenses = active_expenses.drop(idx)
            new_days_inv, _ = simulate_timeline(target_value, total_savings, base_savings, active_incomes, temp_active_expenses, active_rate)
            st.write(f"如果減少 **{item_name}** 開支（省下 {round(item_cost)} 元）並配合 **{selected_tool.split(' ')[0]}**，我們的解鎖時間將提早 **{round(base_days_inv - new_days_inv)}** 天。")
