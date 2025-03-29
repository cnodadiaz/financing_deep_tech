import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
#import umami

st.set_page_config(page_title="Capital Raising Toolkit", page_icon="logo.png", layout="centered", initial_sidebar_state="expanded", menu_items=None)

#umami.set_url_base("https://umami.gregotsch.com")
#umami.set_website_id('cbca9cc7-e956-4df9-b92c-591973e74e26')
#umami.set_hostname('convertiblenotecalculator.gregotsch.com')


# log page view
# page_view_resp = umami.new_page_view(
#     page_title='Page Reload', # Defaults to event_name if omitted.
#     url='/',
#     referrer='https://convertiblenotecalculator.gregotsch.com')


# Function to perform the calculations
def calculate_valuation(raise_amount, alimit, interest, time_months, next_round_capital, equity_trade_next_round, discount_rate):
    gov_contribution = min(raise_amount, alimit)
    total_capital = raise_amount + gov_contribution
    convertible_note_value = raise_amount * (1 + (interest * (time_months / 12)))
    pre_money_valuation = next_round_capital / equity_trade_next_round
    post_money_valuation = pre_money_valuation + next_round_capital

    # Adjust the convertible note value for the discount rate
    discounted_value = convertible_note_value / (1 - discount_rate)
    equity_ownership_investors = discounted_value / post_money_valuation
    
    # Calculate the additional working capital after the next funding round
    additional_working_capital = next_round_capital - (convertible_note_value + discounted_value)

    return {
    'gov_contribution': gov_contribution,
    'total_capital': total_capital,
    'convertible_note_value': convertible_note_value,
    'pre_money_valuation': pre_money_valuation,
    'post_money_valuation': post_money_valuation,
    'equity_ownership_investors': equity_ownership_investors,
    'additional_working_capital': additional_working_capital
    }

def get_image_base64(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Streamlit app layout
st.title('Capital Raising Toolkit')
# st.write('A simple tool for startups to communicate effectively with investors about their financial planning and valuation.')

with st.expander("Description and Explanation"):
    st.markdown("""
    **Startup Fundraising Financial Model**

    The tool clarifies the company's valuation by focusing on capital needs rather than relying on speculative or arbitrary factors. 
    Startups can transparently demonstrate how their projected capital requirements align with their strategic growth plans and fundraising goals using this tool.

    **Purpose**
    
    The primary purpose of this website is as follows:

    - **Calculate Initial Capital**: Determine the total initial capital raised from investors and supplemented by government contributions.
    
    - **Accrue Interest on Convertible Notes**: Compute the future value of convertible notes, considering the interest accrued over a specified period until the next funding round.
    
    - **Determine Capital Needs for Next Round**: Project the capital requirements for the next fundraising round.
    
    - **Establish Pre-Money Valuation**: Calculate the company's valuation before raising new funds based on the projected capital needs and the percentage of equity to be traded.
    
    - **Determine Post-Money Valuation**: Calculate the company's valuation immediately after raising the new capital, providing a clear picture of the company's worth post-investment.
    
    - **Equity Distribution**: Explain the distribution of equity ownership, mainly focusing on the impact of converting notes on investors' equity.

    **About the Process**

    - **Initial Capital and Government Contribution**: The form gathers input on the initial capital raised from investors and any additional government contributions, like innovation grants, establishing the startup's base financial status.
    
    - **Equity Ownership:** The tool calculates investors' equity ownership after the convertible notes convert, clarifies the ownership dilution, and ensures the impact on existing and future investors is clear and justifiable, making the investment process transparent and fair.
    
    - **Pre-Round Gains:** The money invested starts growing as soon as it is received, continuing to appreciate as the company develops further. This unique feature provides early investors immediate gains, rewarding their early commitment and support. It's our way of showing appreciation for their trust in the startup.
    
    - **Interest on Convertible Notes:** We calculate the future value of convertible notes using the interest rate and the period until the next funding round. Transparently accounts for the impact of interest accrual, ensuring investors understand how their investment appreciates over time.
    
    - **Next Round Capital Needs:** By inputting the projected capital needs for the next round, startups can base their valuation on actual financial requirements, shifting the focus from speculative valuation methods to a needs-based approach.
    
    - **Pre-Money Valuation Calculation:** We divide the capital needed by the equity fraction to be traded away in the next round, resulting in the pre-money valuation. This is a transparent, straightforward, and easy-to-understand starting point. The valuation should be adjusted as due diligence progresses, refining market opportunity, competitive landscape, revenue projections, and cost structure. A comprehensive analysis of the valuation could lead to a higher value.
                
    - **Post-Money Valuation:** The post-money valuation results from adding the new capital raised in the next round to the pre-money valuation. This figure reflects the company's worth immediately after securing new investments, providing a transparent and honest valuation to present to potential investors.
                
    - **Additional Working Capital:** The funds raised include capital received in advance from successful fundraising rounds. The additional working capital is the fraction of the total capital raised available for immediate use, after accounting for previously advanced funds and the discounts provided to early investors. This extra working capital ensures the startup has the necessary liquidity to achieve its following milestones, making the investment more secure and appealing to investors. It's reassuring that your investment is in safe hands and a testament to the startup's potential.
    """)

# Sidebar with input parameters
st.sidebar.header('Input Parameters')
raise_amount = st.sidebar.number_input('Amount raised from investors ($)', value=350000.0, min_value=0.0, format='%f')
alimit = st.sidebar.number_input('Upper limit for the gov. innovation grant ($)', value=250000.0, min_value=0.0, format='%f')
interest = st.sidebar.number_input('Bank loan (or note) interest rate (%)', value=7.0, min_value=0.0, format='%f') / 100
time_months = st.sidebar.number_input('Time (in months) until the next funding round', value=24, min_value=1, step=1)
next_round_capital = st.sidebar.number_input('Projected capital needs for the next round ($)', value=2000000.0, min_value=0.0, format='%f')
equity_trade_next_round = st.sidebar.number_input('Equity Trade for next round (%)', value=20.0, min_value=0.0, format='%f') / 100
discount_rate = st.sidebar.number_input('Discount for early investors upon conversion (%)', value=20.0, min_value=0.0, max_value=100.0, format='%f') / 100


results = calculate_valuation(raise_amount, alimit, interest, time_months, next_round_capital, equity_trade_next_round, discount_rate)


investment_value_after = results['equity_ownership_investors'] * results['post_money_valuation']
interest_accrued = results['convertible_note_value'] - raise_amount
discount_gain = investment_value_after - results['convertible_note_value']
total_growth = investment_value_after - raise_amount
valuation_gain = total_growth - interest_accrued - discount_gain

# Round for presentation
interest = round(interest_accrued, 2)
discount = round(discount_gain, 2)
pre_to_post_money_gain = round(valuation_gain, 2)
growth = round(total_growth, 2)



logdata = {
    "input":
    {
        "raise_amount": raise_amount,
        "alimit": alimit,
        "interest": interest,
        "time_months": time_months,
        "next_round_capital": next_round_capital,
        "equity_trade_next_round": equity_trade_next_round,
        "discount_rate": discount_rate
    },
    "results": results
}


#event_resp = umami.new_event(
#    event_name='Calculation-Data',
#    title='Calculation-Data', # Defaults to event_name if omitted.
#    url='/',
#    custom_data=logdata,
#    referrer='https://convertiblenotecalculator.gregotsch.com')

# st.write('Value of the convertible note after interest:')
# st.subheader(f"USD {round(results['convertible_note_value'],2):.2f}")
st.write('Equity ownership for investors after conversion:')
st.subheader(str(round(results['equity_ownership_investors'] * 100, 2)) + '%')
st.write('Value of investment after next round:')
st.subheader(f"USD {round(discount + pre_to_post_money_gain + interest + raise_amount,2):.2f}")

st.write('Investment growth:')
col_left, col_right = st.columns(2)
with col_left:
    st.subheader(f"USD {round(growth,2):.2f}")

with col_right:
    st.subheader(f"{round((growth / (raise_amount/100)),2):.2f}%")

data = pd.DataFrame([
    ["Pre-round gains", "Investment", raise_amount, 0],
    ["Pre-round gains", "Interest", interest, 1],
    ["Pre-round gains", "Discount", discount, 2],
    ["Pre-round gains", "Valuation Gains", pre_to_post_money_gain, 3]
], columns=['type', 'name', 'value', 'order'])


chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('type', axis=alt.Axis(title='', labelAngle=0), sort=['Pre-round gains']),
    y=alt.Y('value', axis=alt.Axis(title='Amount ($)')),
    color=alt.Color('name', legend=alt.Legend(title="Legend"),
                    scale=alt.Scale(range=['gold', 'lightgreen', 'lightblue', 'orange'])),
    order=alt.Order("order", sort='ascending'),
)


st.write('Pre-round gains')
st.altair_chart(chart, theme="streamlit", use_container_width=True)


#Pre-money and post-money valuation
source = pd.DataFrame({
    'Metrics': ['Pre-money', 'Post-money'],
    'Amount ($)': [results['pre_money_valuation'], results['post_money_valuation']],
})

bar_chart = alt.Chart(source).mark_bar().encode(
    y='Amount ($)',
    x=alt.X('Metrics', axis=alt.Axis(labelAngle=0, title=None), sort=['Pre-money', 'Post-money']),
    color=alt.Color('Metrics',scale=alt.Scale(range=['gold', 'lightgreen']), legend=None)
)

st.write('Pre-money and Post-money valuation')
st.altair_chart(bar_chart, use_container_width=True)

# Amount available money
source = pd.DataFrame({
    'Metrics': ['Investors', 'Government', 'Working Capital'],
    'Amount ($)': [raise_amount, results['gov_contribution'], results['total_capital']],
})


bar_chart = alt.Chart(source).mark_bar().encode(
    y=alt.Y('Amount ($)'),
    x=alt.X('Metrics', axis=alt.Axis(labelAngle=0, title=None)),
    color=alt.Color('Metrics',scale=alt.Scale(range=['lightgreen', 'lightblue', 'gold']), legend=None)
)

st.write('Pre-round Contributions')
st.altair_chart(bar_chart, use_container_width=True)


#Next round capital needs
source = pd.DataFrame({
    'Metrics': ['Next round', 'Add. working capital'],
    'Amount ($)': [next_round_capital, results['additional_working_capital']],
})

bar_chart = alt.Chart(source).mark_bar().encode(
    y='Amount ($)',
    x=alt.X('Metrics', axis=alt.Axis(labelAngle=0, title=None, labelLimit=200), sort=['Next round', 'Add. working capital']),
    color=alt.Color('Metrics',scale=alt.Scale(range=['gold', 'lightblue']), legend=None)
)

st.write('Next round capital needs and additional working capital')
st.altair_chart(bar_chart, use_container_width=True)



# st.write("*Featuring ALMIs Innovationstöd")

# st.subheader('Results')
# st.write(f"Initial capital raised from investors, e.g. convertible note: ${raise_amount:.2f}")
# st.write(f"Government's contribution (e.g., Tillväxtverket): ${results['gov_contribution']:.2f}")
# st.write(f"Total capital for the startup: ${results['total_capital']:.2f}")
# st.write(f"Pre-money valuation for the next round: ${results['pre_money_valuation']:.2f}")
# st.write(f"Post-money valuation after next round: ${results['post_money_valuation']:.2f}")
# st.write(f"Value of the convertible note after interest: ${results['convertible_note_value']:.2f}")
# st.write(f"Equity ownership for investors after conversion: {results['equity_ownership_investors'] * 100:.2f}%")
# st.write(f"Amount to be raised in the next funding round: ${next_round_capital:.2f}")
# st.write(f"Additional working capital after the next funding round: ${results['additional_working_capital']:.2f}")

# Convert the QR code image to base64
# qr_code_image_base64 = get_image_base64('bit.ly_financingx.png')

# Display the QR code image with CSS styling
# st.markdown(
#     f"""
#     <div style="text-align: right;">
#         <img src="data:image/png;base64,{qr_code_image_base64}" style="width: 25%; margin-right: 0;">
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# To run the app, use the following command in the terminal: streamlit run app.py

if st.sidebar.button('Calculate'):
    st.rerun()
