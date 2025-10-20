import streamlit as st
from utils.Jio import CallRecordsExtractor
from utils.csvPlottyVisualizer import top_contacts_chart, top_usage_chart, usage_distribution_pie, calls_over_time,total_call_time_over_time,number_call_summary

st.set_page_config(layout="wide")
st.title("Call Records Dashboard 📞")


extractor = CallRecordsExtractor()

uploaded_files = st.file_uploader(
    "Upload PDF(s) of call records",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    pdf_paths = [f.name for f in uploaded_files]  # Streamlit file object has .read()
    # Save uploaded PDFs temporarily to process
    temp_files = []
    import tempfile
    for f in uploaded_files:
        t = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        t.write(f.read())
        t.close()
        temp_files.append(t.name)
    df = extractor.process_pdfs(temp_files)

    top_n = st.sidebar.number_input("Top N Contacts/Usage", min_value=1, max_value=50, value=10)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Most Contacted Numbers", 
        "Top Used Usage (Seconds)",
        "Calls Over Time",
        "Total Call Time",
        "Search by Number"
    ])

    with tab1:
        st.plotly_chart(top_contacts_chart(df, top_n), use_container_width=True)
    with tab2:
        st.plotly_chart(top_usage_chart(df, top_n), use_container_width=True)
    with tab3:
        st.plotly_chart(calls_over_time(df), use_container_width=True)
    with tab4:
        st.plotly_chart(total_call_time_over_time(df), use_container_width=True)
    with tab5:
        number_to_search = st.text_input("Enter Number to Search")
        if number_to_search:
            result = number_call_summary(df, number_to_search)
            summary = result["summary"]
            fig = result["fig"]

            st.subheader(f"Summary for {number_to_search}")
            st.write(f"Total Calls: {summary['Total Calls']}")
            st.write(f"Total Duration (min): {summary['Total Duration (min)']:.2f}")
            st.write(f"Average Duration (min): {summary['Average Duration (min)']:.2f}")

            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No calls found for this number.")
    

st.markdown(
    """
    <hr>
    <p style='text-align: center; 
    font-size: 14px; 
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    text-align: center;'>Made by <strong>Vinay</strong> | <a href='https://github.com/vinay-ghate/CallRecordsVisualizer' target='_blank'>GitHub</a>
    </p>
    """, 
    unsafe_allow_html=True
)

