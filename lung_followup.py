import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="肺癌術後フォローアップ支援アプリ v1")

st.title("🫁 肺癌術後フォローアップ 支援アプリ v1")

# --- 手術日入力 ---
surgery_date = st.date_input("📅 手術日を入力してください", value=datetime.date(2024, 7, 1))
today = datetime.date.today()
months_after_surgery = (today.year - surgery_date.year) * 12 + (today.month - surgery_date.month)

st.markdown(f"🗓️ 術後：**{months_after_surgery}ヶ月** 経過")

# --- 入力項目 ---
st.header("🔬 病理・術式情報の入力")

stage = st.selectbox("病期 (Stage)", ["IA", "IB", "IIA", "IIB", "IIIA", "IIIB", "IV"])
surgical_method = st.selectbox("術式", ["部分切除", "区域切除", "葉切除", "肺全摘"])
stas = st.selectbox("STAS（air space浸潤）", ["なし", "あり"])
v1 = st.selectbox("V因子（血管侵襲）", ["V0", "V1"])
pl1 = st.selectbox("PL因子（胸膜侵襲）", ["PL0", "PL1"])
margin_positive = st.selectbox("切除断端陽性", ["なし", "あり"])
tkis = st.multiselect("現在の内服薬（該当するものを選択）", ["オシメルチニブ（タグリッソ）", "免疫チェックポイント阻害薬", "なし"])

# --- リスク判定 ---
high_risk_factors = 0
if surgical_method in ["部分切除", "区域切除"]:
    high_risk_factors += 1
if stas == "あり":
    high_risk_factors += 1
if v1 == "V1":
    high_risk_factors += 1
if pl1 == "PL1":
    high_risk_factors += 1
if margin_positive == "あり":
    high_risk_factors += 1

risk_level = "低リスク"
if high_risk_factors >= 3:
    risk_level = "高リスク"
elif high_risk_factors >= 1:
    risk_level = "中リスク"

# --- 出力 ---
st.header("📋 フォローアップ推奨")

st.markdown(f"**再発リスク分類： `{risk_level}`**")

st.subheader("📅 今月の推奨検査")
recommendations = []

recommendations.append("✅ 診察：再発チェック・内服確認")
recommendations.append("✅ 採血：腫瘍マーカー、肝腎機能など")

# CTの頻度（簡易ルール）
if risk_level == "高リスク":
    ct_months = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
elif risk_level == "中リスク":
    ct_months = [6, 12, 18, 24, 36, 48, 60]
else:
    ct_months = [12, 24, 36, 48, 60]

if months_after_surgery in ct_months:
    recommendations.append("✅ CT検査：今月実施推奨")

# X線
if months_after_surgery % 6 == 0:
    recommendations.append("✅ 胸部X線：定期確認")

# 薬剤別の追加検査
if "オシメルチニブ（タグリッソ）" in tkis:
    recommendations.append("✅ 心電図：QT延長確認")
if "免疫チェックポイント阻害薬" in tkis:
    recommendations.append("✅ 甲状腺機能・血糖・尿検査")

for item in recommendations:
    st.markdown(f"- {item}")

st.info("🔄 次回の検査予定は、手術日とリスク分類に基づいて自動調整されます。")
