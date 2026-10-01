import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CEP - Monitoring & Feedback", layout="wide")
st.title("🤝 Community Engagement Program")
st.subheader("Project: Monitoring and Feedback Mechanisms")
st.divider()

# Auto create file
if not os.path.exists("cep_data.csv"):
    pd.DataFrame(columns=["Date","Student_Name","Village","Activity","Hours","Beneficiaries","Status","Feedback_Score","Feedback_Text"]).to_csv("cep_data.csv", index=False)

tab1, tab2, tab3 = st.tabs(["📝 Monitoring", "💬 Feedback", "📊 Report"])

# TAB 1 - MONITORING
with tab1:
    st.subheader("Monitoring System - Add Daily Activity")
    with st.form("mon"):
        c1, c2 = st.columns(2)
        with c1:
            student = st.text_input("👤 Student Name (Manual Entry)", placeholder="e.g. Aditya Patil")
            village = st.text_input("🏘️ Village / Area Name", placeholder="e.g. Pohegaon")
            activity = st.selectbox("Activity", ["Awareness Camp", "Cleanliness Drive", "Teaching", "Health Camp", "Digital Literacy", "Tree Plantation", "Survey"])
            date = st.date_input("Date")
        with c2:
            hours = st.number_input("Hours Spent", 1, 10, 2)
            beneficiaries = st.number_input("Beneficiaries Count", 1, 500, 15)
            status = st.selectbox("Status", ["Planned", "In-Progress", "Completed", "Follow-up Needed"])
            remarks = st.text_area("Monitoring Observations")

        btn = st.form_submit_button("✅ Save Monitoring Data", use_container_width=True)
        if btn:
            if student == "" or village == "":
                st.error("Enter Student Name and Village!")
            else:
                df_old = pd.read_csv("cep_data.csv")
                new = {"Date": str(date), "Student_Name": student, "Village": village, "Activity": activity, "Hours": hours, "Beneficiaries": beneficiaries, "Status": status, "Feedback_Score": 0, "Feedback_Text": remarks}
                pd.concat([df_old, pd.DataFrame([new])]).to_csv("cep_data.csv", index=False)
                st.success(f"Monitored: {activity} at {village} by {student}")
                st.rerun()

    df = pd.read_csv("cep_data.csv")
    st.dataframe(df, use_container_width=True)

# TAB 2 - FEEDBACK
with tab2:
    st.subheader("Feedback Mechanism")
    df = pd.read_csv("cep_data.csv")

    if len(df) == 0:
        st.warning("Add monitoring data first")
    else:
        st.write("Collect feedback from community people")
        with st.form("fb"):
            act_list = [f"{i} | {row['Activity']} - {row['Village']} by {row['Student_Name']}" for i, row in df.iterrows()]
            sel = st.selectbox("Select Activity to give Feedback", act_list)
            idx = int(sel.split("|")[0])

            c1, c2 = st.columns(2)
            with c1:
                person = st.text_input("Community Person Name")
                score = st.slider("Satisfaction (1-10)", 1, 10, 8)
            with c2:
                useful = st.selectbox("Usefulness", ["Very Useful", "Useful", "Average", "Not Useful"])
                fb_text = st.text_area("Feedback / Suggestion")

            fb_btn = st.form_submit_button("Submit Feedback")
            if fb_btn:
                df.loc[idx, "Feedback_Score"] = score
                df.loc[idx, "Feedback_Text"] = df.loc[idx, "Feedback_Text"] + f" | FEEDBACK by {person}: {fb_text} [{useful} - {score}/10]"
                df.to_csv("cep_data.csv", index=False)
                st.success("Feedback Saved!")

        st.divider()
        # Show feedback
        st.dataframe(df[["Village","Activity","Student_Name","Feedback_Score","Feedback_Text"]], use_container_width=True)

# TAB 3 - REPORT
with tab3:
    st.subheader("Monitoring & Feedback Report")
    df = pd.read_csv("cep_data.csv")

    if len(df) == 0:
        st.info("No data")
    else:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Activities", len(df))
        k2.metric("Total Hours", int(df["Hours"].sum()))
        k3.metric("Beneficiaries", int(df["Beneficiaries"].sum()))
        avg = df[df["Feedback_Score"]>0]["Feedback_Score"].mean()
        k4.metric("Avg Feedback", f"{avg:.1f}/10" if pd.notna(avg) else "Pending")

        st.bar_chart(df, x="Activity", y="Beneficiaries")
        st.bar_chart(df, x="Village", y="Feedback_Score")

        st.download_button("📥 Download Full Report CSV", df.to_csv(index=False).encode(), "CEP_Monitoring_Feedback_Report.csv")

        if st.button("🗑️ Clear All Data"):
            os.remove("cep_data.csv")
            st.rerun()

st.caption("Community Engagement Program | Monitoring via Status Tracking | Feedback via Community Rating")
