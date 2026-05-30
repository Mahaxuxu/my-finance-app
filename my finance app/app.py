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

# ---- 預計開支 摺疊區 ----
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
custom_target_value = st.number_input("👉 另外想測試的自定義儲存金額 (元，不測試請設為 0)", min_value=0, value=0, step=500, key="custom_target_input")


# --- 6. 核心計量算法：全功能高精準雙向現金流時序模擬器 ---
def simulate_timeline(target_val, initial_savings, monthly_savings, active_inc_df, active_exp_df, rate_annual=0.0, fd_amount=0.0, fd_months=0):
    today = datetime.date.today()
    
    # 科學分流：區分可用活期資金與定期鎖定資金
    current_available = initial_savings - fd_amount
    current_locked = fd_amount
    fd_days = int(fd_months * 30.4)
    
    daily_savings = monthly_savings / 30.4
    
    if initial_savings >= target_val:
        return 0, today
        
    inc_dict = active_inc_df.groupby("預計收入日期")["金額"].sum().to_dict() if not active_inc_df.empty else {}
    exp_dict = active_exp_df.groupby("預計開支日期")["金額"].sum().to_dict() if not active_exp_df.empty else {}
    
    daily_rate = (rate_annual / 100) / 365
    
    for day in range(1, 3651):
        sim_date = today + datetime.timedelta(days=day)
        
        if day <= fd_days:
            # 定存鎖定期間：只有定存本金享受複利，常態儲蓄存入活期可用資金
            current_locked += current_locked * daily_rate
            current_available += daily_savings
        else:
            # 定存到期日：當天瞬間釋放本息解鎖入活期
            if day == fd_days + 1 and fd_days > 0:
                current_available += current_locked
                current_locked = 0
            
            if fd_days == 0:
                # 零錢通/活期模式：全額本息每天利滾利
                total_pool = current_available + current_locked
                current_available += (total_pool * daily_rate) + daily_savings
            else:
                # 定存解鎖後不再享有定期高利率
                current_available += daily_savings
                
        # 單筆現金流衝擊皆由可用資金帳戶承擔
        if sim_date in inc_dict:
            current_available += inc_dict[sim_date]
        if sim_date in exp_dict:
            current_available -= exp_dict[sim_date]
            
        # 核心流動性判定：定存期間只能用可用活期資金購買目標；解鎖後可用全部資金
        total_accessible = current_available if day <= fd_days else (current_available + current_locked)
        
        if total_accessible >= target_val:
            return day, sim_date
            
    return 3650, today + datetime.timedelta(days=3650)


# =========================================================
# 📊 第一大板塊：基礎現狀回測（純儲蓄現狀）
# =========================================================
st.write("")
st.header("第二步：動態回測與邊際效益分析看板 (純儲蓄現狀)")

base_savings = income - total_essential - total_discretionary

if base_savings <= 0:
    st.error("預算超支警告：你每月的總開銷已經超過了你的收入！請點開上方摺疊盒刪減非必須開支。")
else:
    base_days, predicted_date = simulate_timeline(target_value, total_savings, base_savings, active_incomes, active_expenses, 0.0, 0.0, 0)
    base_months = base_days / 30.4
    
    col_kpi1, col_kpi2 = st.columns(2)
    with col_kpi1:
        st.metric(label="每月淨儲蓄", value=f"{round(base_savings)} 元")
    with col_kpi2:
        st.metric(label="預計解鎖時間", value=f"{round(base_days)} 天 ({round(base_months, 1)} 個月)")
        st.markdown(f"### **預測實現日期：{predicted_date.strftime('%Y年%m月%d日')}**")
    
    if custom_target_value > 0:
        cust_days_base, cust_date_base = simulate_timeline(custom_target_value, total_savings, base_savings, active_incomes, active_expenses, 0.0, 0.0, 0)
        st.write(f"自定義金額儲蓄時間：儲存滿 {custom_target_value} 元預計需要 {cust_days_base} 天（預計於 {cust_date_base.strftime('%Y年%m月%d日')} 達成）。")
        
    s_percentages = [i / 10.0 for i in range(0, 11)]
    sensitivity_data = []
    marginal_data = []
    prev_days = base_days 
    
    for i, s in enumerate(s_percentages):
        saved_amount = total_discretionary * s  
        new_discretionary = total_discretionary * (1 - s)
        new_savings = income - total_essential - new_discretionary
        
        new_days, scenario_date = simulate_timeline(target_value, total_savings, new_savings, active_incomes, active_expenses, 0.0, 0.0, 0)
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

    st.write("")
    st.markdown("### **💡 減法理財：省下這筆，提早幾天？ (純儲蓄現狀)**")
    if not active_discretionary.empty:
        for idx, row in active_discretionary.iterrows():
            item_name = row["娛樂事項"]
            item_cost = pd.to_numeric(row["消費金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_total_discretionary = total_discretionary - item_cost
            temp_savings = income - total_essential - temp_total_discretionary
            new_days, _ = simulate_timeline(target_value, total_savings, temp_savings, active_incomes, active_expenses, 0.0, 0.0, 0)
            st.write(f"🔸 如果你這個月不 **{item_name}**（省 {round(item_cost)} 元），你的 **{target_name}** 解鎖時間會立刻提早 **{round(base_days - new_days)}** 天！")

    if not active_expenses.empty:
        for idx, row in active_expenses.iterrows():
            item_name = row["項目名稱"]
            item_cost = pd.to_numeric(row["金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_active_expenses = active_expenses.drop(idx)
            new_days, _ = simulate_timeline(target_value, total_savings, base_savings, active_incomes, temp_active_expenses, 0.0, 0.0, 0)
            st.write(f"🔸 如果你這個月不 **{item_name}**（省 {round(item_cost)} 元），你的 **{target_name}** 解鎖時間會立刻提早 **{round(base_days - new_days)}** 天！")


# =========================================================
# 🌟 第二大板塊：全新理財板塊「理財加持」
# =========================================================
st.write("")
st.write("")
st.divider()
st.markdown("# **理財加持 🚀**")

st.caption("請在下方表格自定義您關注的理財工具及其預估年化收益率：")
default_tools = pd.DataFrame([
    {"理財方式名稱": "微信零錢通", "年化收益率(%)": 2.0},
    {"理財方式名稱": "數位帳戶高利活存", "年化收益率(%)": 3.5},
    {"理財方式名稱": "銀行定期存款", "年化收益率(%)": 2.2}
])
edited_tools_df = st.data_editor(default_tools, num_rows="dynamic", use_container_width=True, key="tools_table")

tool_options = ["無 (不使用理財，年化 0%)"] + edited_tools_df["理財方式名稱"].tolist()
selected_tool = st.selectbox("🎯 請選擇目前要加入計算的理財方式：", tool_options, key="tool_select_box")

# 初始化流動性鎖定參數
fd_amount = 0.0
fd_months = 0

if "無 (不使用理財" in selected_tool:
    active_rate = 0.0
else:
    try:
        active_rate = edited_tools_df[edited_tools_df["理財方式名稱"] == selected_tool]["年化收益率(%)"].values[0]
    except:
        active_rate = 0.0

# 🌟 全新交互：若選取定期存款，引導輸入期限與定存本金，並動態運算可動用資金
if "定期存款" in selected_tool:
    col_fd1, col_fd2 = st.columns(2)
    with col_fd1:
        fd_amount = st.number_input("請輸入要投入定期存款的本金金額 (元)", min_value=0.0, max_value=float(total_savings), value=float(total_savings), step=100.0)
    with col_fd2:
        fd_months = st.number_input("請輸入該定期存款的時間周期 (個月)", min_value=1, value=6, step=1)
    
    available_funds = total_savings - fd_amount
    st.metric("💡 下方額外顯示當前活期可動用資金", f"{round(available_funds)} 元")
else:
    st.info(f"💡 目前已套用理財方案：**{selected_tool}**，正在以 **{active_rate}%** 的每日複利回報更新動態分析。")


# =========================================================
# 📊 第三大板塊：理財優化後的「動態回測與邊際效益分析看板」
# =========================================================
st.write("")
st.header("第二步：動態回測與邊際效益分析看板 (加入理財優化後)")

if base_savings <= 0:
    st.error("預算超支警告：請先修正上方消費數據。")
else:
    # 注入定存與利率參數進入高階演算法
    base_days_inv, predicted_date_inv = simulate_timeline(target_value, total_savings, base_savings, active_incomes, active_expenses, active_rate, fd_amount, fd_months)
    base_months_inv = base_days_inv / 30.4
    days_improved = base_days - base_days_inv
    
    col_kpi1_inv, col_kpi2_inv = st.columns(2)
    with col_kpi1_inv:
        st.metric(label="每月淨儲蓄 (投入本金)", value=f"{round(base_savings)} 元")
    with col_kpi2_inv:
        st.metric(
            label="預計解鎖時間 (理財加持版)", 
            value=f"{round(base_days_inv)} 天 ({round(base_months_inv, 1)} 個月)", 
            delta=f"比純儲蓄縮短 {round(days_improved)} 天" if days_improved > 0 else "與純儲蓄持平", 
            delta_color="inverse"
        )
        st.markdown(f"### **預測實現日期：{predicted_date_inv.strftime('%Y年%m月%d日')}**")
        
    if custom_target_value > 0:
        cust_days_base, _ = simulate_timeline(custom_target_value, total_savings, base_savings, active_incomes, active_expenses, 0.0, 0.0, 0)
        cust_days_inv, cust_date_inv = simulate_timeline(custom_target_value, total_savings, base_savings, active_incomes, active_expenses, active_rate, fd_amount, fd_months)
        cust_improved = cust_days_base - cust_days_inv
        st.write(f"自定義金額儲蓄時間 (理財加持版)：儲存滿 {custom_target_value} 元需要 {cust_days_inv} 天（預計於 {cust_date_inv.strftime('%Y年%m月%d日')} 達成），比不理財提早了 {round(cust_improved)} 天！")

    # ---------------------------------------------------------
    # ⏳ 時間軸存錢指南（極簡版：移除 Emoji 且統一命名為帳戶總餘額）
    # ---------------------------------------------------------
    with st.expander(f"您的專屬理財時間軸指南 (套用：{selected_tool})", expanded=True):
        inc_by_date_guide = active_incomes.groupby("預計收入日期")["金額"].sum().to_dict() if not active_incomes.empty else {}
        exp_by_date_guide = active_expenses.groupby("預計開支日期")["金額"].sum().to_dict() if not active_expenses.empty else {}
        
        today_g = datetime.date.today()
        current_available_g = total_savings - fd_amount
        current_locked_g = fd_amount
        fd_days_g = int(fd_months * 30.4)
        daily_savings_g = base_savings / 30.4
        daily_rate_g = (active_rate / 100) / 365
        
        guide_records = []
        
        # 初始點
        guide_records.append({
            "日期": today_g.strftime('%Y-%m-%d'),
            "存款變動": "0",
            "帳戶總餘額(元)": round(current_available_g + current_locked_g)
        })
        
        for day in range(1, 3651):
            sim_date_g = today_g + datetime.timedelta(days=day)
            
            if day <= fd_days_g:
                current_locked_g += current_locked_g * daily_rate_g
                current_available_g += daily_savings_g
            else:
                if day == fd_days_g + 1 and fd_days_g > 0:
                    current_available_g += current_locked_g
                    current_locked_g = 0
                
                if fd_days_g == 0:
                    total_pool = current_available_g + current_locked_g
                    current_available_g += (total_pool * daily_rate_g) + daily_savings_g
                else:
                    current_available_g += daily_savings_g
            
            if sim_date_g in inc_by_date_guide:
                inc_amt = inc_by_date_guide[sim_date_g]
                current_available_g += inc_amt
                guide_records.append({
                    "日期": sim_date_g.strftime('%Y-%m-%d'),
                    "存款變動": f"+{round(inc_amt)}",
                    "帳戶總餘額(元)": round(current_available_g + current_locked_g)
                })
                
            if sim_date_g in exp_by_date_guide:
                exp_amt = exp_by_date_guide[sim_date_g]
                current_available_g -= exp_amt
                guide_records.append({
                    "日期": sim_date_g.strftime('%Y-%m-%d'),
                    "存款變動": f"-{round(exp_amt)}",
                    "帳戶總餘額(元)": round(current_available_g + current_locked_g)
                })
                
            total_accessible_g = current_available_g if day <= fd_days_g else (current_available_g + current_locked_g)
            if total_accessible_g >= target_value:
                guide_records.append({
                    "日期": sim_date_g.strftime('%Y-%m-%d'),
                    "存款變動": "目標達成",
                    "帳戶總餘額(元)": round(total_accessible_g)
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
        
        new_days_inv, scenario_date_inv = simulate_timeline(target_value, total_savings, new_savings, active_incomes, active_expenses, active_rate, fd_amount, fd_months)
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
        st.subheader("累積儲蓄效益 (理財加持版)")
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
            st.info(f"已選中點數據：當省錢比例為 {click_x} （即每個月省下 {exact_money} 元）並加入 {selected_tool} 加持時，總共可提前 {days_ahead} 天（即在 {exact_date} ）實現目標。")
        else:
            st.caption("提示：點擊上方折線圖中的藍色圓點，可在這裡動態查看該點的數據。")

    with graph_col2_inv:
        st.subheader("邊際省錢效益 (理財加持版)")
        fig_marginal_inv = px.bar(df_marginal_inv, x="節省比例變動 (X)", y="邊際提前天數 (Y)", template="plotly_white")
        fig_marginal_inv.update_layout(clickmode='event+select')
        selected_marginal_inv = st.plotly_chart(fig_marginal_inv, on_select="rerun", use_container_width=True, key="marginal_chart_invest")
        
        if selected_marginal_inv and "selection" in selected_marginal_inv and selected_marginal_inv["selection"]["points"]:
            pt = selected_marginal_inv["selection"]["points"][0]
            st.info(f"已選中區間數據：{pt['x']} 階段，每多省10%並配合理財，可額外縮短 {pt['y']} 天。")
        else:
            st.caption("提示：點擊上方柱狀圖的長條，可在這裡動態查看該區間的詳細邊際效益。")

    st.write("")
    st.markdown("### **💡 減法理財：省下這筆，提早幾天？ (含理財增值收益)**")
    if not active_discretionary.empty:
        for idx, row in active_discretionary.iterrows():
            item_name = row["娛樂事項"]
            item_cost = pd.to_numeric(row["消費金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_total_discretionary = total_discretionary - item_cost
            temp_savings = income - total_essential - temp_total_discretionary
            new_days_inv, _ = simulate_timeline(target_value, total_savings, temp_savings, active_incomes, active_expenses, active_rate, fd_amount, fd_months)
            st.write(f"🔸 如果你這個月不 **{item_name}**（省 {round(item_cost)} 元），並配合 **{selected_tool}**，你的解鎖時間會提早 **{round(base_days_inv - new_days_inv)}** 天！")

    if not active_expenses.empty:
        for idx, row in active_expenses.iterrows():
            item_name = row["項目名稱"]
            item_cost = pd.to_numeric(row["金額"], errors='coerce')
            if pd.isna(item_cost) or item_cost <= 0: continue
            temp_active_expenses = active_expenses.drop(idx)
            new_days_inv, _ = simulate_timeline(target_value, total_savings, base_savings, active_incomes, temp_active_expenses, active_rate, fd_amount, fd_months)
            st.write(f"🔸 如果你這個月不 **{item_name}**（省 {round(item_cost)} 元），並配合 **{selected_tool}**，你的解鎖時間會提早 **{round(base_days_inv - new_days_inv)}** 天！")
