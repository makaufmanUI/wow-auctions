

if __name__ == "__main__":
    import streamlit as st
    from streamlit.components.v1 import html
    from plots import price, price_and_quantity, price_and_region
    
    st.set_page_config(
        page_title="AH Prices",
        layout="centered",
        #page_icon=":heavy_dollar_sign:"
        page_icon=":currency_exchange:"
    )
    
    with open("style/style.css") as f:      # load css file
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    javascript = """
    <script>
        function OnPageLoad() {
            var a = document.querySelectorAll('[data-baseweb="select"]');
            console.log(a);
            var all = document.getElementsByTagName("*");
            for (var i=0, max=all.length; i < max; i++) {
                console.log(all[i]);
            }
        }

        window.addEventListener ? 
        window.addEventListener("load",OnPageLoad,false)  : 
        window.attachEvent && window.attachEvent("onload",OnPageLoad);
    </script>
    """
    

    st.title("Auction House Plots")
    st.write("Simple tool for plotting price & quantity of items.")

    st.write("")

    item = st.text_input("Item name", "Saronite Ore")
    numDays = st.number_input("Number of days", 1, 40, 7)

    server = st.selectbox("Server", ["Skyfury", "Faerlina", "Whitemane"])
    faction = st.selectbox("Faction", ["Alliance", "Horde"])

    chartType = st.selectbox("Chart type", ["Price", "Price & Quantity", "Price & Region"], help="Select the type of chart you want to view.")

    st.write("")

    # replaceOutliers = st.checkbox("Replace outliers", False)
    # threshold = st.number_input("Outlier threshold", 1, 5, 2)
    # html(javascript, height=0)

    if st.button("Plot"):
        if chartType == "Price":
            st.pyplot(price(item, numDays, server, faction))
            # disable the view fullscreen button (button title="View fullscreen" class="css-e370rw e191ei0e1")
            # st.markdown("""<style>button[title="View fullscreen"]{display: none;}</style>""", unsafe_allow_html=True)
        elif chartType == "Price & Quantity":
            st.pyplot(price_and_quantity(item, numDays, server, faction))
        elif chartType == "Price & Region":
            st.pyplot(price_and_region(item, numDays, server, faction, replaceOutliers=True, threshold=3))
