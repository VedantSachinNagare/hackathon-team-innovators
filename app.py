import gradio as gr
import math

def calculate_financial_plan(income, expenses, savings, debt, goal_amount, goal_years):
    try:
        # Validate inputs
        if any(x <= 0 for x in [income, expenses, savings, debt, goal_amount, goal_years]):
            return "<p style='color: #e74c3c;'><strong>Error:</strong> All values must be positive.</p>"

        # Basic financial calculations
        monthly_disposable = income - expenses
        if monthly_disposable < 0:
            return "<p style='color: #e74c3c;'><strong>Error:</strong> Your expenses exceed your income. Reduce expenses to proceed.</p>"

        # Calculate amount needed to save to reach goal
        amount_needed = goal_amount - savings
        if amount_needed <= 0:
            return """
            <div style='background-color: #2a2a3b; padding: 20px; border-radius: 8px; color: #e0e0e0;'>
                <h2 style='color: #ffffff;'>Your Financial Plan</h2>
                <p>You've already reached or exceeded your goal! Consider setting a new goal or investing your savings.</p>
                """ + get_tips(0, debt) + "</div>"

        months = goal_years * 12
        monthly_savings_required = amount_needed / months
        yearly_savings_required = monthly_savings_required * 12

        if monthly_savings_required > monthly_disposable:
            shortfall = monthly_savings_required - monthly_disposable
            plan = f"""
            <p><strong>Goal Analysis:</strong> To reach ${goal_amount:,.2f} in {goal_years} years, you need to save ${monthly_savings_required:,.2f} per month.</p>
            <p><strong>Issue:</strong> Your disposable income (${monthly_disposable:,.2f}/month) is not enough. You're short by ${shortfall:,.2f}/month.</p>
            <p><strong>Recommendation:</strong></p>
            <ul>
                <li>Reduce monthly expenses by at least ${shortfall:,.2f}. Consider cutting non-essential spending (e.g., dining out, subscriptions).</li>
                <li>Increase income through side hustles or a raise to cover the shortfall.</li>
                <li>Extend your goal timeline to reduce the monthly savings needed.</li>
            </ul>
            """
        else:
            surplus = monthly_disposable - monthly_savings_required
            plan = f"""
            <p><strong>Goal Analysis:</strong> To reach ${goal_amount:,.2f} in {goal_years} years, you need to save ${monthly_savings_required:,.2f} per month.</p>
            <p><strong>Good News:</strong> You have ${monthly_disposable:,.2f} available each month, leaving a surplus of ${surplus:,.2f}.</p>
            <p><strong>Recommendation:</strong></p>
            <ul>
                <li>Save ${monthly_savings_required:,.2f} each month to meet your goal.</li>
                <li>Consider investing the surplus (${surplus:,.2f}/month) to grow your wealth faster.</li>
                <li>Automate savings to stay consistent.</li>
            </ul>
            """

        # Investment suggestion
        plan += f"""
        <p><strong>Investment Options:</strong></p>
        <ul>
            <li><strong>High-Yield Savings Account:</strong> Safe, earns 3-5% annually. Good for short-term goals.</li>
            <li><strong>Mutual Funds:</strong> Diversified, moderate risk, 6-8% average returns. Suitable for 5+ years.</li>
            <li><strong>Emergency Fund:</strong> Save 3-6 months of expenses (${expenses*3:,.2f}-${expenses*6:,.2f}) before investing.</li>
        </ul>
        """

        # Debt management advice
        if debt > 0:
            monthly_debt_payment = min(debt / (goal_years * 12), monthly_disposable * 0.3)  # Cap at 30% of disposable
            plan += f"""
            <p><strong>Debt Management:</strong> You have ${debt:,.2f} in debt.</p>
            <ul>
                <li>Pay at least ${monthly_debt_payment:,.2f}/month toward debt to reduce it steadily.</li>
                <li>Prioritize high-interest debt (e.g., credit cards) to save on interest.</li>
                <li>Avoid new debt to focus on your goal.</li>
            </ul>
            """

        return f"""
        <div style='background-color: #2a2a3b; padding: 20px; border-radius: 8px; color: #e0e0e0;'>
            <h2 style='color: #ffffff;'>Your Financial Plan</h2>
            {plan}
            <div style='background-color: #1b3a4b; padding: 15px; border-left: 4px solid #4a90e2; margin-top: 20px;'>
                {get_tips(monthly_savings_required, debt)}
            </div>
        </div>
        """

    except Exception as e:
        return "<p style='color: #e74c3c;'><strong>Error:</strong> An error occurred. Please try again.</p>"

def get_tips(monthly_savings, debt):
    tips = """
    <h3>Financial Education Tips</h3>
    <ul>
        <li><strong>Budgeting:</strong> Track your spending with a simple app or spreadsheet to identify savings opportunities.</li>
        <li><strong>Saving:</strong> Set up automatic transfers to a savings account each payday to build discipline.</li>
        <li><strong>Investing:</strong> Start small with low-risk options like index funds. Avoid get-rich-quick schemes.</li>
    """
    if debt > 0:
        tips += "<li><strong>Debt:</strong> Pay more than the minimum on debts to reduce interest costs over time.</li>"
    if monthly_savings > 0:
        tips += f"<li><strong>Goal Tracking:</strong> Check your progress monthly to stay motivated toward your ${monthly_savings:,.2f}/month savings target.</li>"
    tips += "</ul>"
    return tips

# Gradio dark theme
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="slate",
    text_size="lg",
).set(
    body_background_fill="*neutral_900",
    body_background_fill_dark="*neutral_900",
    body_text_color="*neutral_50",
    body_text_color_dark="*neutral_50",
    input_background_fill="*neutral_800",
    input_background_fill_dark="*neutral_800",
    input_border_color="*neutral_600",
    input_border_color_dark="*neutral_600",
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_dark="*primary_500",
    button_primary_text_color="*neutral_50",
    button_primary_text_color_dark="*neutral_50",
    panel_background_fill="*neutral_800",
    panel_background_fill_dark="*neutral_800",
    panel_border_color="*neutral_600",
    panel_border_color_dark="*neutral_600",
)

# Gradio interface setup
with gr.Blocks(theme=theme, title="Conversational Financial Advisor") as demo:
    gr.Markdown("# Conversational Financial Advisor")
    with gr.Row():
        with gr.Column():
            income = gr.Number(label="Monthly Income ($)", precision=2, minimum=0)
            expenses = gr.Number(label="Monthly Expenses ($)", precision=2, minimum=0)
            savings = gr.Number(label="Current Savings ($)", precision=2, minimum=0)
            debt = gr.Number(label="Total Debt ($)", precision=2, minimum=0)
            goal_amount = gr.Number(label="Financial Goal Amount ($)", precision=2, minimum=0)
            goal_years = gr.Number(label="Time to Reach Goal (Years)", precision=0, minimum=0)
            submit = gr.Button("Get Financial Plan")
    output = gr.HTML()
    submit.click(
        fn=calculate_financial_plan,
        inputs=[income, expenses, savings, debt, goal_amount, goal_years],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch(server_port=7860)