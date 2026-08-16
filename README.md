# Nykaa Marketing Campaign Analytics Dashboard

A premium, interactive Streamlit analytics application designed for enterprise marketing executives to analyze portfolio campaign performance, spend efficiency, and acquisition dropoffs.

## Project Structure
- `app.py`: Main Streamlit application file containing UI logic, filters, and Plotly visualizations.
- `nykaa_campaign_data.csv`: Marketing dataset containing 55,000+ campaign lines.
- `requirements.txt`: Python package dependencies.
- `README.md`: Setup and usage guide.

## Prerequisites
Ensure you have Python 3.8+ installed. You can install all dependencies using the following commands.

## Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/gayatribhuyan/Desktop/FUCKASS/NYKAA
   ```

2. **Set up a Virtual Environment (Optional but recommended)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Dashboard**:
   ```bash
   streamlit run app.py
   ```
   This will start a local server and automatically open the application in your default web browser (typically at `http://localhost:8501`).

## Visualizations and Key Performance Indicators (KPIs)
- **Top KPI Cards**: Total Spend (calculated from Conversions × Acquisition Cost), Total Revenue, Conversions, and Average ROI.
- **Topline Revenue by Campaign Category**: Bar chart showing total revenue breakdown across Social Media, Paid Ads, SEO, Influencer, and Email campaigns.
- **Portfolio Acquisition Funnel**: Step-down funnel outlining volume progression from Impressions → Clicks → Leads → Conversions.
- **CAC vs. Conversion Volume**: Scatter plot showing individual campaign unit economics to highlight sweet-spots and outliers.
- **Strategic Reallocation Directives**: Data-backed recommendation detailing the reallocation of budgets to maximize revenue contribution.
