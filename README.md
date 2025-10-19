
#  AI Data Visualization & Insights Assistant

An **interactive AI-powered data analysis tool** that transforms **natural language queries** into insightful visualizations and **business takeaways** — powered by **Groq’s LLM reasoning** and a **Streamlit dashboard**.

Upload your dataset, ask questions like

> “Show me total sales by country”
> and the app automatically:

* Understands your query via Groq
* Generates the correct plot (bar, line, scatter, pie)
* Performs anomaly detection
* Provides actionable business insights

---

##  Features

 **Natural Language Query to Visualization**
Ask in plain English — Groq interprets and returns the appropriate plot structure.

 **Interactive Dashboard (Streamlit)**
Upload your CSV, view plots, dataset summaries, and AI insights instantly in your browser.

 **Automatic Data Summary**
Displays statistics, missing values, and numeric summaries.

 **Anomaly Detection**
Identifies outliers using the **3σ (three standard deviation)** rule.

**AI-Generated Actionable Insights**
Groq analyzes patterns, missing values, correlations, and anomalies — delivering **plain-English takeaways**.


## Tech Stack

| Component      | Purpose                                         |
| -------------- | ----------------------------------------------- |
| **Streamlit**  | Interactive web UI                              |
| **Groq API**   | Natural language reasoning & insight generation |
| **Python**     | Core scripting                                  |
| **Pandas**     | Data processing                                 |
| **Matplotlib** | Chart rendering                                 |
| **dotenv**     | Secure API key management                       |




## Setup Instructions

### 1️ Clone the Repository

### 2 Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```
streamlit
groq
pandas
matplotlib
python-dotenv
```

### 3 Configure Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

### 5️ Run the App

```bash
streamlit run app.py
```

---

##  Example Usage

### Upload:

Upload your dataset (e.g., `sales_data_sample.csv`).

### Query Examples:

| Type          | Example Query                                 |
| ------------- | --------------------------------------------- |
| **Sales**     | “Show me total sales by country”              |
| **Trends**    | “Sales trend over months”                     |
| **Products**  | “Compare average order value by product line” |
| **Customers** | “Top customers by revenue”                    |
| **Anomalies** | “Find unusual order values”                   |

### Output:

* Interactive chart (bar/line/scatter/pie)
* Data summary table
* Anomaly detection report
* AI-generated business insights (via Groq)

---

## Example Output

**Sample Query:**

```
show me total sales by country
```

**Expected Behavior:**

* Groq generates:

  ```json
  {
    "plot_type": "bar",
    "x_col": "COUNTRY",
    "y_col": "SALES"
  }
  ```
* Streamlit displays:

  * Bar chart of total sales per country
  * Summary statistics
  * Anomaly warnings
  * AI-generated insights, e.g.:

>  *USA and France lead in total sales. There are missing entries in DealSize. Consider addressing anomalies in OrderValue to improve forecasting accuracy.*

---

##  How It Works

1. **User Uploads CSV**

   * Streamlit reads data using `pandas.read_csv()`.

2. **Natural Language Query**

   * User types a query.
   * Groq interprets it and returns structured JSON.

3. **Plot Generation**

   * Python parses Groq’s response and visualizes the chart with `matplotlib`.

4. **Dataset Summary**

   * Automatically displays descriptive statistics and missing values.

5. **Anomaly Detection**

   * Finds numeric values outside `mean ± 3σ`.

6. **Actionable Takeaways**

   * Groq analyzes summary stats and returns business insights in natural language.

---
