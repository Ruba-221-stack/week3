import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Telco Churn Dashboard", layout="wide")
st.title("📊 لوحة متابعة مغادرة عملاء الاتصالات (Telco Churn)")

df = pd.read_csv("telco_clean.csv")

services = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]
df["Total_AddOn_Services"] = (df[services] == "Yes").sum(axis=1)
df["Churn_Flag"] = (df["Churn"] == "Yes").astype(int)

# فلاتر الـ Sidebar
st.sidebar.header("الفلاتر")
contract = st.sidebar.selectbox(
    "نوع العقد (Contract)", ["الكل"] + sorted(df["Contract"].unique().tolist())
)
internet = st.sidebar.selectbox(
    "خدمة الإنترنت (InternetService)",
    ["الكل"] + sorted(df["InternetService"].unique().tolist()),
)
churn_filter = st.sidebar.selectbox(
    "حالة المغادرة (Churn)", ["الكل", "Yes", "No"]
)

filtered = df.copy()
if contract != "الكل":
  filtered = filtered[filtered["Contract"] == contract]
if internet != "الكل":
  filtered = filtered[filtered["InternetService"] == internet]
if churn_filter != "الكل":
  filtered = filtered[filtered["Churn"] == churn_filter]

# 4 أرقام رئيسية (st.metric)
c1, c2, c3, c4 = st.columns(4)
total = len(filtered)
churn_rate = (filtered["Churn_Flag"].mean() * 100) if total > 0 else 0
avg_tenure = filtered["tenure"].mean() if total > 0 else 0
avg_monthly = filtered["MonthlyCharges"].mean() if total > 0 else 0

c1.metric("إجمالي العملاء", f"{total:,}")
c2.metric("معدل المغادرة", f"{churn_rate:.1f}%")
c3.metric("متوسط مدة الاشتراك", f"{avg_tenure:.1f}")
c4.metric("متوسط الفاتورة الشهرية", f"{avg_monthly:.2f}")

st.markdown("---")

# رسمتان من أهم الاكتشافات
g1, g2 = st.columns(2)

with g1:
  st.subheader("المغادرة حسب نوع العقد")
  fig1, ax1 = plt.subplots(figsize=(6, 4))
  if total > 0:
    sns.countplot(data=filtered, x="Contract", hue="Churn", ax=ax1)
  st.pyplot(fig1)

with g2:
  st.subheader("معدل المغادرة حسب الخدمات الإضافية")
  fig2, ax2 = plt.subplots(figsize=(6, 4))
  if total > 0:
    sns.barplot(
        data=filtered, x="Total_AddOn_Services", y="Churn_Flag", ax=ax2
    )
  st.pyplot(fig2)

st.markdown("---")

# أهم 3 اكتشافات بالأرقام
st.subheader("أهم 3 اكتشافات")
st.markdown("""
* *1. العقود الشهرية:* إجمالي العملاء *7,043* عميل، وأصحاب العقود الشهرية (Month-to-month) هم الأكثر عرضة للمغادرة.
* *2. الخدمات الإضافية:* العملاء أصحاب *خدمة إضافية واحدة فقط* يصل معدل مغادرتهم إلى حوالي *46%، ثم يقل تدريجياً بزيادة الخدمات حتى **6* خدمات.
* *3. جاهزية النمذجة:* تم تجهيز ملف telco_model_ready.csv بأبعاد *7,043* صف و*26* عمود لاستهداف العملاء الأكثر خطورة.
""")