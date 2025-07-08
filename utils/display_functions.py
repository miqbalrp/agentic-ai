import streamlit as st
import pandas as pd
import plotly.express as px
from schemas.finance_app import TextOnlyOutput, AnalysisWithPlotOutput, GeneralizedOutput

def set_title(title_text= "IDX AI Assistant", title_icon= "📈"):
    """Set the title and configuration for the Streamlit app."""

    st.set_page_config(
        page_title=title_text,
        page_icon=title_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Title and description
    st.title(f"{title_icon} {title_text}")

def set_sidebar():
    """Set the sidebar content for the Streamlit app.
    This function provides an overview of the app's capabilities and links to relevant resources."""

    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.markdown("""
    You can ask about:

    - 📄 **Company overview**
    - 📈 **Daily transaction trends** , including:
        - Closing price
        - Transaction volume
        - Market cap
    - 🏆 **Top-ranked companies** by metrics like:
        - Dividend yield
        - Earnings
        - Market cap
        - Revenue
        - Total dividend
        - PB / PE / PS ratios
    - 🔁 You can also ask **multi-step questions** that combine any of the topics above 
                        
    **Currently supports companies listed on the Indonesia Stock Exchange (IDX) only.**
    **Data is retrieved from [Sectors.app](https://sectors.app) API.**
                        """)
    st.sidebar.markdown("""
    ---
    🔧 **Powered by**:  
    [OpenAI API](https://platform.openai.com/docs) | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | [Plotly](https://plotly.com/python/) | [Sectors.app API](https://sectors.app) | [Streamlit](https://streamlit.io)

    💻 **Source Code**: [GitHub Repository](https://github.com/miqbalrp/agentic-ai)
    """)

def initialize_session_state():
    """Initialize session state variables for user input and query execution."""
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    if "run_query" not in st.session_state:
        st.session_state.run_query = False
    if "example_query_pills" not in st.session_state:
        st.session_state.example_query_pills = None

def initialize_chat_history():
    """Initialize chat history in the session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def generate_chat_id():
        """Generate a unique chat ID for the session."""
        import uuid
        if "chat_id" not in st.session_state:
            st.session_state.chat_id = uuid.uuid4().hex[:16]
            return "New chat session started with ID: " + st.session_state.chat_id
        else:
            return "Chat session ID: " + st.session_state.chat_id

def display_clear_chat_button():
    """Display a button to clear the chat history in the Streamlit app.
    This function allows users to reset the chat history, which can be useful for starting a new conversation or clearing previous interactions."""
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()  # Rerun the app to reflect the cleared chat history

def display_example_queries():
    """Display example queries as selectable pills in the Streamlit app.
    This function provides a set of predefined example queries that users can select to see how the app responds.
    It includes a callback function to update the user input when an example query is selected.
    """
    
    def on_pill_change():
        """Callback function to handle pill selection change."""
        st.session_state.user_input = st.session_state.example_query_pills

    example_queries = [
        "Show me summary of TLKM", 
        "Analyze daily closing price of BBCA in the last 14 days!",
        "Top 5 Indonesia companies by earning in 2024",
        "Provide summary of top 3 companies in Indonesia by market cap in 2023!"        
    ]

    st.pills(
        label="Try an example query:",
        options=example_queries,
        selection_mode="single",
        key="example_query_pills",
        on_change=on_pill_change
    )

def display_user_input_area():
    """Display a text area for user input in the Streamlit app.
    This function provides a text area where users can enter their queries or questions about financial data.
    It initializes the text area with any existing user input from the session state.
    """
    
    user_input = st.text_area(
        "💬 What would you like to know?", 
        value=st.session_state.user_input,
        key="user_input",
        help="E.g., 'Show me daily transaction of BBCA in the past month'"
    )
    
    return user_input

def set_run_query_state():
    """Set the session state to indicate that a query should be run."""
    st.session_state.run_query = True


def display_agent_response_title():
    st.markdown("### 🤖 Agent's Response")

def display_text_only_output(text_output: TextOnlyOutput):
    display_agent_response_title()
    st.write(text_output.summary)

def display_analysis_with_plot_output(plot_data):
    import uuid
    for dataset in plot_data:
        plot_title = dataset.plot_title
        x_axis_label = dataset.x_axis_title
        y_axis_label = dataset.y_axis_title

        df = pd.DataFrame({
            "x_data": dataset.x,
            "y_data": dataset.y
            }
        )

        if dataset.chart_type == 'line_chart':
            fig = px.line(
                df, 
                x="x_data", 
                y="y_data", 
                markers=True, 
                labels={'x_data': x_axis_label, 'y_data': y_axis_label},
                title=plot_title
                )
            st.plotly_chart(fig, key=str(uuid.uuid4()))  # Use a unique key to avoid Streamlit caching issues

        elif dataset.chart_type == 'bar_horizontal_chart':
            y_label_order = df['y_data'].tolist()
            fig = px.bar(
                df, 
                x="x_data", 
                y="y_data", 
                orientation="h",
                labels={'x_data': x_axis_label, 'y_data': y_axis_label},
                title=plot_title,
                category_orders={'y_data': y_label_order}
                )
            st.plotly_chart(fig, key=str(uuid.uuid4()))  # Use a unique key to avoid Streamlit caching issues
