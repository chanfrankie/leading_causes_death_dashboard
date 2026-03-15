# 📊 Canada Mortality Trends Dashboard

An interactive data visualization dashboard built with **Python** and **Streamlit** to explore the leading causes of death in Canada. This project pulls real-time data directly from **Statistics Canada (Table 13-10-0394-01)** and allows users to analyze mortality trends across various demographics.

## 🌟 Features
- **Real-time Data Integration:** Automatically downloads and extracts the latest dataset directly from the Statistics Canada Web Data Service.
- **Dynamic Filtering:** 
  - **Geography:** View data for Canada as a whole or drill down into specific provinces.
  - **Demographics:** Filter by Age Group and Sex.
  - **Metrics:** Toggle between "Number of Deaths," "Percentage of Deaths," "Rank," and "Age-specific mortality rate."
- **Interactive Visualizations:**
  - **Top 10 Bar Chart:** See the most prevalent causes for a specific year and group.
  - **Composition Pie Chart:** Visualize the share of each cause relative to the top 10.
  - **Historical Trend Line:** Track how a specific cause of death has evolved from 2000 to the present.
- **Data Cleaning Pipeline:** Handles complex StatCan formatting, including ICD-10 code stripping and date normalization.

## 🛠️ Tech Stack
- **Language:** Python 3.12+
- **Dashboard Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
- **Visualizations:** [Plotly Express](https://plotly.com/python/)
- **Data Source:** [Statistics Canada Table 13-10-0394-01](https://doi.org/10.25318/1310039401-eng)

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python installed. You will also need the following libraries:
```bash
pip install streamlit pandas plotly requests
```

### 2. Installation
Clone this repository or download the `leading_deaths_dashboard.py` script to your local machine.

### 3. Run the Dashboard
Navigate to the folder containing the script in your terminal and run:
```bash
streamlit run leading_deaths_dashboard.py
```
The dashboard will automatically open in your default web browser.

## 📂 Project Structure
- `leading_deaths_dashboard.py`: The main application script.
- `README.md`: Project documentation.
- *(Generated)* `13100394-eng.zip`: The raw data downloaded during the first run.

## 📊 Data Attribution
The data used in this application is provided by Statistics Canada under the [Statistics Canada Open Licence](https://www.statcan.gc.ca/en/reference/licence). 

---
*Created as a data visualization project to help make Canadian public health data more accessible.*
