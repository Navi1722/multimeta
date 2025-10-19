import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import json
from groq import Groq
import re

# --- Load environment variables ---
load_dotenv()
client = Groq()

st.title("📊 AI Data Visualization & Insights Assistant")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding="latin1")
    st.success("✅ File loaded successfully!")
    st.write("**Available Columns:**", list(df.columns))
    
    # --- User query ---
    query = st.text_input("Enter your query (e.g., 'show me total sales by country')")

    if query:
        with st.spinner("Analyzing your query with Groq..."):
            plot_prompt = f"""
            You are a data visualization assistant.
            Available dataset columns: {list(df.columns)}.
            User query: "{query}".

            Extract a JSON with:
            - plot_type: one of [line, bar, scatter, pie]
            - x_col: x-axis column
            - y_col: y-axis column (if applicable)
            - group_col: optional grouping column
            """
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": plot_prompt}],
                temperature=0,
                max_completion_tokens=1024,
                top_p=1,
                reasoning_effort="medium",
            )
            response_text = completion.choices[0].message.content

            try:
                instructions = json.loads(response_text)
            except Exception:
                json_str = re.search(r"\{.*\}", response_text, re.S)
                instructions = json.loads(json_str.group()) if json_str else None

            if not instructions:
                st.error("❌ Could not parse Groq response.")
            else:
                plot_type = instructions.get("plot_type", "bar")
                x_col = instructions.get("x_col")
                y_col = instructions.get("y_col")
                group_col = instructions.get("group_col")

                # --- Validate columns ---
                missing_cols = [c for c in [x_col, y_col, group_col] if c and c not in df.columns]
                if missing_cols:
                    st.error(f"⚠️ Columns not found: {missing_cols}")
                else:
                    # --- Plot ---
                    fig, ax = plt.subplots(figsize=(8, 5))
                    if plot_type == "line":
                        if group_col:
                            for key, grp in df.groupby(group_col):
                                ax.plot(grp[x_col], grp[y_col], marker='o', label=str(key))
                            ax.legend()
                        else:
                            ax.plot(df[x_col], df[y_col], marker='o')
                    elif plot_type == "bar":
                        if group_col:
                            df.groupby(group_col)[y_col].mean().plot(kind="bar", ax=ax)
                        else:
                            df.groupby(x_col)[y_col].sum().plot(kind="bar", ax=ax)
                    elif plot_type == "scatter":
                        ax.scatter(df[x_col], df[y_col])
                    elif plot_type == "pie":
                        df.groupby(x_col)[y_col].sum().plot.pie(autopct='%1.1f%%', ax=ax)

                    ax.set_title(f"{plot_type.capitalize()} Plot of {y_col} vs {x_col}")
                    ax.set_xlabel(x_col)
                    if plot_type != "pie":
                        ax.set_ylabel(y_col)
                    st.pyplot(fig)

                    # --- Summary ---
                    st.subheader("📋 Dataset Summary")
                    st.dataframe(df.describe(include='all'))
                    st.write("**Missing Values per Column:**", df.isnull().sum())

                    # --- Anomaly detection ---
                    st.subheader("🚨 Anomaly Detection")
                    numeric_cols = df.select_dtypes(include='number').columns
                    anomalies = {}
                    for col in numeric_cols:
                        mean, std = df[col].mean(), df[col].std()
                        upper, lower = mean + 3 * std, mean - 3 * std
                        anomaly_rows = df[(df[col] < lower) | (df[col] > upper)]
                        if not anomaly_rows.empty:
                            anomalies[col] = anomaly_rows[[col]]
                            st.warning(f"Column '{col}' has {len(anomaly_rows)} anomalies.")
                    if anomalies:
                        for col, rows in anomalies.items():
                            st.write(f"Sample anomalies in '{col}':", rows.head())

                    # --- Insights via Groq ---
                    st.subheader("💡 Actionable Takeaways (via Groq)")
                    dataset_summary = {
                        "numeric_summary": df.describe(include='number').to_dict(),
                        "categorical_summary": df.describe(include='object').to_dict(),
                        "missing_values": df.isnull().sum().to_dict(),
                        "numeric_columns": list(df.select_dtypes(include='number').columns),
                        "categorical_columns": list(df.select_dtypes(include='object').columns)
                    }
                    summary_text = json.dumps(dataset_summary, indent=2)

                    groq_prompt = f"""
                    You are a data analyst assistant.
                    Given the following dataset statistics:

                    {summary_text}

                    Generate a numbered list of actionable takeaways for a business user.
                    Include insights about:
                    - Missing values
                    - Numeric anomalies
                    - Highly correlated numeric columns
                    - Interesting patterns from categorical columns

                    Output in plain English.
                    """
                    completion_takeaways = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[{"role": "user", "content": groq_prompt}],
                        temperature=0,
                        max_completion_tokens=1024,
                        top_p=1,
                        reasoning_effort="medium",
                    )

                    actionable_text = completion_takeaways.choices[0].message.content
                    st.markdown(actionable_text)
