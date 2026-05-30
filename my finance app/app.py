import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="中學生智慧理財系統", layout="wide")

# ---- 1. 每個月的收入 ----
st.markdown("### **1. 每個月的收入 / 零花錢總額 (元)**")
income = st.number_input("", min_value=0, value=1500, step=50, label_visibility="collapsed", key="income_input")

# ---- 2. 目前個人總存款 摺疊區 ----
with st.expander("2. 點開填寫：目前個人總存款 (元)", expanded=True):
    savings_total_placeholder = st.empty()
    default_savings = pd.DataFrame([
        {"存款項目": "銀行/郵局帳戶", "金額": 1000, "選入計算": True},
        {"存款項目": "存錢筒現鈔", "金額": 200, "選入計算": True},
    ])
    edited_savings_df = st.data_editor(default_savings, num_rows="dynamic", use_container_width=True, key="savings_table")
    edited_savings_df["選入計算"] = edited_savings_df["選入計算"].fillna(False).astype(bool)
    active_savings = edited_savings_df[edited_savings_df["選入計算"] == True]
    total_savings = pd.to_numeric(active_savings["金額"], errors='coerce').fillna(0).sum()
    savings_total_placeholder.metric("總存款總計 (已選入)", f"{total_savings} 元")

# ---- 預計收入 / 預計開支 摺疊區 ----
with st.expander("未來單筆現金流 (預計收入與開支)", expanded=True):
    col_in, col_ex = st.columns(2)
    with col_in:
        st.write("📈 預計收入")
        default_incomes = pd.DataFrame([{"項目名稱": "過年紅包", "金額": 1000, "日期": datetime.date.today() + datetime.timedelta(days=60), "選入": True}])
        edited_incomes_df = st.data_editor(default_incomes, num_rows="dynamic", use_container_width=True, column_config={"日期": st.column_config.DateColumn("日期", format="YYYY-MM-DD")}, key="in_table")
    with col_ex:
        st.write("📉 預計開支")
        default_expenses = pd.DataFrame([{"項目名稱": "教材費", "金額": 500, "日期": datetime.date.today() + datetime.timedelta(days=30), "選入": True}])
        edited_expenses_df = st.data_editor(default_expenses, num_rows="dynamic", use_container_width=True, column_config={"日期": st.column_config.DateColumn("日期", format="YYYY-MM-DD")}, key="ex_table")

# ---- 3. 每月消費摺疊區 (剛需 & 娛樂) ----
with st.expander("3 & 4. 每月消費清單 (必定開支 & 娛樂開支)", expanded=True):
    col_ess, col_dis = st.columns(2)
    with col_ess:
        st.write("🏠 必定消費 (剛需)")
        default_ess = pd.DataFrame([{"必備事項": "交通/午餐", "金額": 600, "選入": True}])
        edited_ess_df = st.data_editor(default_ess, num_rows="dynamic", use_container_width=True, key="ess_table")
    with col_dis:
        st.write("🎮 自我意願 (娛樂)")
        default_dis = pd.DataFrame([{"娛樂事項": "手搖飲/遊戲", "金額": 350, "選入": True}])
        edited_dis_df = st.data_editor(default_dis, num_rows="dynamic", use_container_width=True, key="dis_table")

st.divider()

# ---- 5. 夢想目標 ----
st.markdown("### **5. 存錢想買的東西以及金額**")
target_name = st.text_input("夢想物品名稱", value="最新款降噪耳機")
target_value = st.number_input("目標價值 (元)", min_value=1, value=3000, step=100)

# --- 核心模擬器算法 ---
def simulate_timeline(target_val, initial_savings, monthly_savings, inc_df, exp_df, rate_annual):
    today = datetime.date.today()
    current_savings = initial_savings
    daily_savings = monthly_savings / 30.4
    if current_savings >= target_val: return 0, today
    
    inc_dict = inc_df[inc_df["選入"]==True].groupby("日期")["金額"].sum().to_dict() if not inc_df.empty else {}
    exp_dict = exp_df[exp_df["選入"]==True].groupby("日期")["金額"].sum().to_dict() if not exp_df.empty else {}
    
    daily_rate = (rate_annual / 100) / 365
    for day in range(1, 3651):
        sim_date = today + datetime.timedelta(days=day)
        current_savings += current_savings * daily_rate # 複利增值
        current_savings += daily_savings
        if sim_date in inc_dict: current_savings += inc_dict[sim_date]
        if sim_date in exp_dict: current_savings -= exp_dict[sim_date]
        if current_savings >= target_val: return day, sim_date
    return 3650, today + datetime.timedelta(days=3650)

# --- 數據預處理 ---
total_ess = pd.to_numeric(edited_ess_df[edited_ess_df["選入"]==True]["金額"], errors='coerce').sum()
total_dis = pd.to_numeric(edited_dis_df[edited_dis_df["選入"]==True]["金額"], errors='coerce').sum()
base_savings_no_logic = income - total_ess - total_dis

# ---------------------------------------------------------
# 🌟 全新理財板塊：理財加持
# ---------------------------------------------------------
st.write("")
st.write("")
st.markdown("# **理財加持 🚀**")

# 1. 自定義輸入理財工具數據的表格
st.caption("請在下方表格列出您關注的理財產品及其預期年化收益率：")
default_tools = pd.DataFrame([
    {"理財方式名稱": "微信零錢通", "年化收益率(%)": 2.0},
    {"理財方式名稱": "高利活存帳戶", "年化收益率(%)": 3.5},
    {"理財方式名稱": "銀行定期存款", "年化收益率(%)": 2.2}
])
edited_tools_df = st.data_editor(default_tools, num_rows="dynamic", use_container_width=True, key="tools_table")

# 2. 理財方式選項欄
tool_options = ["不使用理財 (0%)"] + edited_tools_df["理財方式名稱"].tolist()
selected_tool = st.selectbox("🎯 請選擇目前要套用的理財方式進行回測：", tool_options)

# 3. 抓取選中方式的年化收益率
if "不使用理財" in selected_tool:
    active_rate = 0.0
else:
    # 從表格中反查對應名稱的收益率
    try:
        active_rate = edited_tools_df[edited_tools_df["理財方式名稱"] == selected_tool]["年化收益率(%)"].values[0]
    except:
        active_rate = 0.0

st.info(f"💡 目前已啟用：**{selected_tool}**，正在以 **{active_rate}%** 的年化收益率進行複利增值模擬。")

# ---------------------------------------------------------
# 📊 加上理財計算的動態回測與看板
# ---------------------------------------------------------
st.write("")
st.header("理財優化後的動態分析看板")

if base_savings_no_logic <= 0:
    st.error("預算超支！請先調整上方開支。")
else:
    # 進行理財後的模擬
    base_days, predicted_date = simulate_timeline(target_value, total_savings, base_savings_no_logic, edited_incomes_df, edited_expenses_df, active_rate)
    
    kpi_col1, kpi_col2 = st.columns(2)
    with kpi_col1:
        st.metric("每月淨儲蓄 (本金)", f"{round(base_savings_no_logic)} 元")
    with kpi_col2:
        st.metric("解鎖時間 (理財加持後)", f"{round(base_days)} 天", delta=f"{round(base_days/30.4, 1)} 個月", delta_color="inverse")
        st.markdown(f"### **實現日期：{predicted_date.strftime('%Y年%m月%d日')}**")

    # 繪製理財後的圖表
    s_percentages = [i / 10.0 for i in range(0, 11)]
    sensitivity_data = []
    marginal_data = []
    prev_days = base_days 
    
    for i, s in enumerate(s_percentages):
        item_saved = total_dis * s
        new_dis = total_dis * (1 - s)
        new_sav = income - total_ess - new_dis
        d, dt = simulate_timeline(target_value, total_savings, new_sav, edited_incomes_df, edited_expenses_df, active_rate)
        
        sensitivity_data.append({
            "節省比例": f"{int(s * 100)}%", "累積提前天數": round(base_days - d),
            "每當月省下金額": round(item_saved), "預測日期": dt.strftime('%Y年%m月%d日')
        })
        if i > 0: marginal_data.append({"區間": f"{int(s_percentages[i-1]*100)}%→{int(s*100)}%", "邊際天數": round(prev_days - d, 1)})
        prev_days = d

    df_t = pd.DataFrame(sensitivity_data)
    df_m = pd.DataFrame(marginal_data)
    
    g1, g2 = st.columns(2)
    with g1:
        st.subheader("理財累積效益趨勢")
        fig1 = px.line(df_t, x="節省比例", y="累積提前天數", markers=True, template="plotly_white")
        sel1 = st.plotly_chart(fig1, on_select="rerun", use_container_width=True, key="c1")
        if sel1 and sel1["selection"]["points"]:
            p = sel1["selection"]["points"][0]
            row = df_t[df_t["節省比例"]==p['x']].iloc[0]
            st.info(f"當省錢 {p['x']} (每月省{row['每當月省下金額']}元) 並配合 {selected_tool}，可提前 {row['累積提前天數']} 天於 {row['預測日期']} 達成！")
    with g2:
        st.subheader("理財邊際省錢效益")
        st.plotly_chart(px.bar(df_m, x="區間", y="邊際天數", template="plotly_white"), use_container_width=True)

# ---- 🚀 底部：減法理財小精靈 ----
st.write("")
st.divider()
st.markdown("### **💡 減法理財：省下這筆，提早幾天？ (含理財收益)**")
active_dis = edited_dis_df[edited_dis_df["選入"]==True]
if not active_dis.empty:
    for _, r in active_dis.iterrows():
        cost = pd.to_numeric(r["金額"], errors='coerce')
        if cost > 0:
            d_new, _ = simulate_timeline(target_value, total_savings, (income-total_ess-(total_dis-cost)), edited_incomes_df, edited_expenses_df, active_rate)
            st.write(f"🔸 如果不 **{r['娛樂事項']}** (省{round(cost)}元)，配合 **{selected_tool}**，將提早 **{round(base_days-d_new)}** 天解鎖！")
