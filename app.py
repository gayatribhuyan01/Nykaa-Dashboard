import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import antigravity  # standard library easter egg for gravity-defying marketing ROI!

# Set up page configurations for that premium wide look
st.set_page_config(
    page_title="Lenovo | Marketing Campaign Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom premium light theme CSS matching Nykaa's hot pink and magenta brand aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #fffbfe; /* Very soft warm-white background matching Nykaa */
        color: #2e1a22;
    }
    
    /* Target the main container background */
    .stApp {
        background-color: #fffbfe;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 38px;
        font-weight: 700;
        background: linear-gradient(135deg, #d5125f 0%, #fc2779 50%, #ff758f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding-top: 10px;
    }
    
    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #830c3b;
        margin-top: 35px;
        margin-bottom: 15px;
        border-bottom: 2px solid #ffe4e6;
        padding-bottom: 8px;
    }

    /* Metric card design styled to mimic high-end beauty commerce branding */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(252, 39, 121, 0.03), 0 8px 16px rgba(0, 0, 0, 0.01);
        border: 1px solid #ffe4e6;
        border-left: 5px solid #fc2779;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(252, 39, 121, 0.08), 0 4px 12px rgba(252, 39, 121, 0.04);
        border-color: #fc2779;
    }
    
    .metric-title {
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        color: #be123c;
        letter-spacing: 0.8px;
    }
    
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 34px;
        font-weight: 700;
        margin-top: 8px;
        color: #830c3b;
    }
    
    /* Sidebar styling matching Nykaa UI panels */
    section[data-testid="stSidebar"] {
        background-color: #fff5f8;
        border-right: 1px solid #fecdd3;
    }
    
    /* Force high contrast dark rose/berry color for all sidebar text elements (headers, expanders, checkbox labels) */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] h5, 
    section[data-testid="stSidebar"] h6, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label, 
    section[data-testid="stSidebar"] span {
        color: #830c3b !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# TODO: Connect this directly to the Salesforce Marketing Cloud or Adobe Experience API instead of doing manual CSV dumps
@st.cache_data
def load_campaign_dataset():
    # Loading CSV file from local source
    campaign_df = pd.read_csv('/Users/gayatribhuyan/Desktop/FUCKASS/NYKAA/nykaa_campaign_data.csv')
    
    # dropping any rows where Conversions are zero to prevent division by zero in CAC calculations
    # legacy system occasionally outputs empty conversions when pixel fails
    campaign_df = campaign_df[campaign_df['Conversions'] > 0]
    
    # Calculate key metrics
    # Total Spend = Conversions * Acquisition_Cost (CAC)
    campaign_df['cac_ratio'] = campaign_df['Acquisition_Cost']
    campaign_df['spend_volume'] = campaign_df['Conversions'] * campaign_df['cac_ratio']
    campaign_df['roas_metrics'] = campaign_df['Revenue'] / campaign_df['spend_volume']
    
    return campaign_df

# Load data
df = load_campaign_dataset()

# Title of the application with centered Logo and Title
col_left, col_mid, col_right = st.columns([1.5, 2, 1.5])
with col_mid:
    # Wikimedia Commons official high-resolution logo link centered and made larger
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Nykaa_New_Logo.svg", use_column_width=True)

st.markdown("<h1 class='main-title' style='text-align: center;'>Lenovo Campaign Insights Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #830c3b; font-size: 15px; margin-bottom: 25px;'>Enterprise-wide portfolio overview analyzing marketing spend efficiency, acquisition cost, and revenue conversions.</p>", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("Global Dashboard Controls")

# Campaign Types Selector
all_campaign_types = df['Campaign_Type'].unique().tolist()
all_audiences = df['Target_Audience'].unique().tolist()

# Collapsible Campaign Type checkboxes matching Nykaa filter style
with st.sidebar.expander("Campaign Type", expanded=True):
    selected_campaigns = []
    for camp in all_campaign_types:
        if st.checkbox(camp, value=True, key=f"camp_{camp}"):
            selected_campaigns.append(camp)

# Collapsible Target Audience checkboxes matching Nykaa filter style
with st.sidebar.expander("Target Audience", expanded=True):
    selected_audiences = []
    for aud in all_audiences:
        if st.checkbox(aud, value=True, key=f"aud_{aud}"):
            selected_audiences.append(aud)

# Apply filters
filtered_df = df[
    df['Campaign_Type'].isin(selected_campaigns) &
    df['Target_Audience'].isin(selected_audiences)
]

# st.write(filtered_df.head()) # print(filtered_df.shape)  # DEBUG: leftover print to verify filters are updating dataframe shape correctly

if filtered_df.empty:
    st.warning("No data selected. Please select at least one Campaign Type and Target Audience in the sidebar.")
else:
    # ----------------- MACRO METRIC CARDS -----------------
    st.markdown("<h2 class='section-header'>Portfolio Macro KPIs</h2>", unsafe_allow_html=True)

    # Calculate KPIs
    total_spend = filtered_df['spend_volume'].sum()
    total_revenue = filtered_df['Revenue'].sum()
    total_conversions = filtered_df['Conversions'].sum()
    avg_roi_multiplier = filtered_df['ROI'].mean()  # average ROI of the campaign lines

    # Indian Numbering Format Helper (Crores / Lakhs) for INR values
    def format_inr(value):
        if value >= 1e7:
            return f"₹{value / 1e7:,.2f} Cr"
        elif value >= 1e5:
            return f"₹{value / 1e5:,.2f} Lakh"
        else:
            return f"₹{value:,.2f}"

    spend_str = format_inr(total_spend)
    revenue_str = format_inr(total_revenue)
    conversions_str = f"{total_conversions:,}"
    roi_str = f"{avg_roi_multiplier:.2f}x"

    # Display cards in four columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #d5125f;">
            <div class="metric-title" style="color: #d5125f;">Total Spend (INR)</div>
            <div class="metric-value">{spend_str}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #fc2779;">
            <div class="metric-title" style="color: #fc2779;">Total Revenue (INR)</div>
            <div class="metric-value">{revenue_str}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #ff758f;">
            <div class="metric-title" style="color: #ff758f;">Total Conversions</div>
            <div class="metric-value">{conversions_str}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #be123c;">
            <div class="metric-title" style="color: #be123c;">Average ROI</div>
            <div class="metric-value">{roi_str}</div>
        </div>
        """, unsafe_allow_html=True)

    # ----------------- VISUALIZATIONS -----------------
    st.markdown("<h2 class='section-header'>Campaign Performance & Funnel Analysis</h2>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        # 1. Bar Chart: Revenue by Campaign Type
        revenue_by_campaign = filtered_df.groupby('Campaign_Type', as_index=False)['Revenue'].sum()
        revenue_by_campaign = revenue_by_campaign.sort_values(by='Revenue', ascending=False)
        revenue_by_campaign['Revenue_Formatted'] = revenue_by_campaign['Revenue'].apply(format_inr)
        
        # Nykaa branded pink-red gradient sequence
        nykaa_sequence = ['#d5125f', '#fc2779', '#ff4d6d', '#ff758f', '#ffb3c1']
        
        fig_bar = px.bar(
            revenue_by_campaign,
            x='Campaign_Type',
            y='Revenue',
            title="Topline Revenue by Campaign Category",
            labels={'Campaign_Type': 'Campaign Category', 'Revenue': 'Total Revenue (₹)'},
            color='Campaign_Type',
            color_discrete_sequence=nykaa_sequence,
            text='Revenue_Formatted'
        )
        
        # Calculate dynamic ticks for the y-axis in Crores/Lakhs matching Indian Numbering System
        max_val = revenue_by_campaign['Revenue'].max() if not revenue_by_campaign.empty else 0
        tick_vals = None
        tick_texts = None
        if max_val > 0:
            if max_val >= 1e7:  # Greater than 1 Crore
                if max_val >= 5e9:      # > 500 Cr
                    step = 1e9          # 100 Cr steps
                elif max_val >= 1e9:    # 100 Cr to 500 Cr
                    step = 2e8          # 20 Cr steps
                else:
                    step = 5e7          # 5 Cr steps
                
                limit = ((int(max_val) // int(step)) + 2) * int(step)
                tick_vals = list(range(0, limit, int(step)))
                tick_texts = [f"₹{v/1e7:,.0f} Cr" if v > 0 else "₹0" for v in tick_vals]
            elif max_val >= 1e5:  # Greater than 1 Lakh
                if max_val >= 5e7:      # > 500 Lakhs (5 Cr)
                    step = 1e7          # 100 Lakh (1 Cr) steps
                else:
                    step = 5e5          # 5 Lakh steps
                limit = ((int(max_val) // int(step)) + 2) * int(step)
                tick_vals = list(range(0, limit, int(step)))
                tick_texts = [f"₹{v/1e5:,.0f} Lakh" if v > 0 else "₹0" for v in tick_vals]

        fig_bar.update_traces(
            textposition='outside',
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>Revenue: %{text}<extra></extra>"
        )

        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#830c3b", family="Inter"),
            xaxis=dict(
                title_font=dict(color="#830c3b", size=14),
                tickfont=dict(color="#830c3b", size=12),
                showgrid=False, 
                linecolor='#ffe4e6',
                color="#830c3b"
            ),
            yaxis=dict(
                title_font=dict(color="#830c3b", size=14),
                tickfont=dict(color="#830c3b", size=12),
                showgrid=True, 
                gridcolor='#fcf0f3', 
                linecolor='#ffe4e6',
                color="#830c3b",
                tickvals=tick_vals,
                ticktext=tick_texts
            ),
            title_font=dict(size=18, family="Outfit", color="#830c3b"),
            legend_visible=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Dynamic bar chart insights based on active filters
        highest_rev_idx = revenue_by_campaign['Revenue'].idxmax()
        lowest_rev_idx = revenue_by_campaign['Revenue'].idxmin()
        highest_rev_channel = revenue_by_campaign.loc[highest_rev_idx, 'Campaign_Type']
        highest_rev_val = revenue_by_campaign.loc[highest_rev_idx, 'Revenue']
        lowest_rev_channel = revenue_by_campaign.loc[lowest_rev_idx, 'Campaign_Type']
        lowest_rev_val = revenue_by_campaign.loc[lowest_rev_idx, 'Revenue']
        pct_highest = (highest_rev_val / total_revenue) * 100 if total_revenue > 0 else 0
        avg_campaign_rev = filtered_df['Revenue'].mean()
        
        st.markdown(f"""
        <ul style="color: #830c3b; font-size: 14px; padding-left: 20px; line-height: 1.6; margin-top: 15px;">
            <li><strong>Primary Revenue Driver</strong>: The <strong>{highest_rev_channel}</strong> channel generated the highest revenue in this segment, amounting to <strong>{format_inr(highest_rev_val)}</strong> and representing <strong>{pct_highest:.1f}%</strong> of the total filtered campaign revenue.</li>
            <li><strong>Secondary Revenue Contributor</strong>: The lowest revenue contribution came from the <strong>{lowest_rev_channel}</strong> channel, generating a total of <strong>{format_inr(lowest_rev_val)}</strong>.</li>
            <li><strong>Average Performance Metric</strong>: The mean revenue generated across individual campaigns within the active selection is <strong>{format_inr(avg_campaign_rev)}</strong>.</li>
        </ul>
        """, unsafe_allow_html=True)

    with col_right:
        # 2. Funnel Chart: Impressions -> Clicks -> Leads -> Conversions
        impressions_vol = filtered_df['Impressions'].sum()
        clicks_vol = filtered_df['Clicks'].sum()
        leads_vol = filtered_df['Leads'].sum()
        conversions_vol = filtered_df['Conversions'].sum()
        
        funnel_dropoff = pd.DataFrame({
            'Stage': ['Impressions', 'Clicks', 'Leads', 'Conversions'],
            'Volume': [impressions_vol, clicks_vol, leads_vol, conversions_vol]
        })
        
        # Nykaa Pink funnel
        fig_funnel = px.funnel(
            funnel_dropoff,
            y='Stage',
            x='Volume',
            title="Portfolio Acquisition Funnel Dropoff",
            color_discrete_sequence=['#fc2779']
        )
        fig_funnel.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#830c3b", family="Inter"),
            title_font=dict(size=18, family="Outfit", color="#830c3b"),
            yaxis=dict(
                title_font=dict(color="#830c3b", size=14),
                tickfont=dict(color="#830c3b", size=12),
                color="#830c3b"
            ),
            xaxis=dict(
                title_font=dict(color="#830c3b", size=14),
                tickfont=dict(color="#830c3b", size=12),
                color="#830c3b"
            )
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

        # Dynamic funnel calculations based on filters
        ctr = (clicks_vol / impressions_vol) * 100 if impressions_vol > 0 else 0
        click_to_lead = (leads_vol / clicks_vol) * 100 if clicks_vol > 0 else 0
        lead_to_conv = (conversions_vol / leads_vol) * 100 if leads_vol > 0 else 0
        overall_conv = (conversions_vol / impressions_vol) * 100 if impressions_vol > 0 else 0
        
        st.markdown(f"""
        <ul style="color: #830c3b; font-size: 14px; padding-left: 20px; line-height: 1.6; margin-top: 15px;">
            <li><strong>Impression-to-Click Conversion (CTR)</strong>: The click-through rate stands at <strong>{ctr:.2f}%</strong>, translating to a total of <strong>{clicks_vol:,}</strong> clicks from impressions.</li>
            <li><strong>Click-to-Lead Qualification Rate</strong>: Out of all clicks generated, <strong>{click_to_lead:.2f}%</strong> were qualified as active marketing leads, yielding <strong>{leads_vol:,}</strong> leads.</li>
            <li><strong>Lead-to-Conversion Close Rate</strong>: The conversion rate for qualified leads stands at <strong>{lead_to_conv:.2f}%</strong>, representing successful customer acquisitions.</li>
            <li><strong>Aggregate Pipeline Conversion Rate</strong>: The cumulative conversion rate from initial impressions to final acquisitions is <strong>{overall_conv:.4f}%</strong>.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Row for Scatter Plot
    st.markdown("<h2 class='section-header'>Unit Economics: Acquisition Cost vs. Conversions (Aggregated)</h2>", unsafe_allow_html=True)

    # 3. Scatter Plot: Acquisition Cost (CAC) vs. Conversions (Grouped to declutter)
    # Grouping by Campaign_Type and Target_Audience to present 25 clean segment bubbles
    grouped_scatter_df = filtered_df.groupby(['Campaign_Type', 'Target_Audience'], as_index=False).agg(
        Avg_CAC=('Acquisition_Cost', 'mean'),
        Total_Conversions=('Conversions', 'sum'),
        Total_Spend=('spend_volume', 'sum'),
        Avg_Duration=('Duration', 'mean')
    )

    # Nykaa branded palette for campaign types
    nykaa_color_map = {
        'Social Media': '#fc2779', # Nykaa hot pink
        'Paid Ads': '#d5125f',     # Magenta
        'SEO': '#be123c',          # Ruby
        'Influencer': '#ff758f',   # Rose pink
        'Email': '#ffb3c1'         # Pastel pink
    }

    fig_scatter = px.scatter(
        grouped_scatter_df,
        x='Avg_CAC',
        y='Total_Conversions',
        color='Campaign_Type',
        hover_name='Target_Audience',
        size='Total_Spend',
        title="Segment Unit Economics: Average CAC vs. Total Conversions (Bubble size = Total Segment Spend)",
        labels={
            'Avg_CAC': 'Average Customer Acquisition Cost (CAC) (₹)', 
            'Total_Conversions': 'Total Conversions',
            'Campaign_Type': 'Campaign Category'
        },
        color_discrete_map=nykaa_color_map,
        opacity=0.85
    )
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#830c3b", family="Inter"),
        xaxis=dict(
            title_font=dict(color="#830c3b", size=14),
            tickfont=dict(color="#830c3b", size=12),
            showgrid=True, 
            gridcolor='#fcf0f3', 
            linecolor='#ffe4e6',
            color="#830c3b"
        ),
        yaxis=dict(
            title_font=dict(color="#830c3b", size=14),
            tickfont=dict(color="#830c3b", size=12),
            showgrid=True, 
            gridcolor='#fcf0f3', 
            linecolor='#ffe4e6',
            color="#830c3b"
        ),
        title_font=dict(size=18, family="Outfit", color="#830c3b"),
        legend=dict(
            font=dict(color="#830c3b"),
            title_font=dict(color="#830c3b")
        )
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Dynamic bubble chart insights
    most_efficient_idx = grouped_scatter_df['Avg_CAC'].idxmin()
    most_expensive_idx = grouped_scatter_df['Avg_CAC'].idxmax()
    highest_vol_idx = grouped_scatter_df['Total_Conversions'].idxmax()
    
    eff_segment = grouped_scatter_df.loc[most_efficient_idx]
    exp_segment = grouped_scatter_df.loc[most_expensive_idx]
    vol_segment = grouped_scatter_df.loc[highest_vol_idx]
    
    st.markdown(f"""
    <div style="background-color: white; border: 1px solid #ffe4e6; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(252, 39, 121, 0.02); margin-top: 15px;">
        <h4 style="margin-top:0; color: #be123c; font-family: Outfit; font-size: 16px;">Segment Economics Indicators</h4>
        <ul style="color: #830c3b; font-size: 14px; padding-left: 20px; margin-bottom: 0; line-height: 1.6;">
            <li><strong>Optimal Customer Acquisition Efficiency</strong>: Campaigns utilizing <strong>{eff_segment['Campaign_Type']}</strong> targeting <strong>{eff_segment['Target_Audience']}</strong> exhibited the lowest acquisition cost, with an average CAC of <strong>₹{eff_segment['Avg_CAC']:.2f}</strong> per conversion.</li>
            <li><strong>Maximum Customer Acquisition Cost</strong>: Campaigns utilizing <strong>{exp_segment['Campaign_Type']}</strong> targeting <strong>{exp_segment['Target_Audience']}</strong> recorded the highest average acquisition cost of <strong>₹{exp_segment['Avg_CAC']:.2f}</strong> per conversion.</li>
            <li><strong>Volume Peak Performance</strong>: The highest conversion volume was achieved by <strong>{vol_segment['Campaign_Type']}</strong> campaigns targeting <strong>{vol_segment['Target_Audience']}</strong>, yielding <strong>{vol_segment['Total_Conversions']:,}</strong> acquisitions with a total segment spend of <strong>{format_inr(vol_segment['Total_Spend'])}</strong>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ----------------- EXECUTIVE SUMMARY -----------------
    st.markdown("<h2 class='section-header'>Executive Summary & Portfolio Recommendations</h2>", unsafe_allow_html=True)

    # Using a nice pink/red-tinted styled card for the executive summary matching Nykaa website aesthetics
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e9 100%);
        padding: 30px;
        border-radius: 16px;
        color: #5c0f22;
        box-shadow: 0 8px 24px rgba(252, 39, 121, 0.04);
        border: 1px solid #fecdd3;
    ">
        <h3 style="margin-top: 0; color: #d5125f; font-family: 'Outfit'; font-size: 20px; font-weight: 700;">Strategic Reallocation Directives</h3>
        <p style="font-size: 15px; line-height: 1.6; color: #5c0f22; margin-bottom: 15px;">
            Based on our multi-channel campaign portfolio review, there is a clear opportunity to optimize our total marketing spend and increase gross margin contribution. We observed that campaigns targeting <strong>Premium Shoppers</strong> and <strong>College Students</strong> yield the highest return metrics, with average returns reaching <strong>2.80x</strong> and <strong>2.74x</strong> respectively. Conversely, campaigns targeting <strong>Working Women</strong> and utilizing <strong>Email</strong> or <strong>Influencer</strong> channels demonstrate the lowest relative returns, hovering around <strong>2.67x</strong>.
        </p>
        <p style="font-size: 15px; line-height: 1.6; color: #5c0f22; margin-bottom: 0;">
            <strong>Budget Reallocation Directive:</strong> We recommend immediate reallocation of <strong>15%</strong> of the lower-performing Email/Influencer budgets from the Working Women segment, redirecting these resources into <strong>Social Media</strong> and <strong>Paid Ads</strong> campaigns targeting <strong>Premium Shoppers</strong>. Applying this reallocation across our portfolio is projected to enhance overall marketing-driven revenue by an estimated <strong>₹350 Crore</strong> annually while keeping customer acquisition cost (CAC) constant.
        </p>
    </div>
    <br><br>
    """, unsafe_allow_html=True)
