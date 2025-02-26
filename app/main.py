# main.py

import streamlit as st
import lasio
from io import StringIO
# from app.preprocessing import clean_data
# from app.visualization import plot_logs
# from app.clustering import apply_kmeans

def load_file():
    """Loads a .las file and returns a LASFile object."""
    file = st.file_uploader("Upload a .las file", type=[".las"])
    if file is not None:
        try:
            bytes_data = file.read()
            str_io = StringIO(bytes_data.decode('Windows-1252'))
            las = lasio.read(str_io)
            return las

        except UnicodeDecodeError as e:
            st.error(f"error loading log.las: {e}")
    return None

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.read()
            str_io = StringIO(bytes_data.decode('Windows-1252'))
            las_file = lasio.read(str_io)
            well_data = las_file.df()
            well_data['DEPTH'] = well_data.index

        except UnicodeDecodeError as e:
            st.error(f"error loading log.las: {e}")
    else:
        las_file = None
        well_data = None

    return las_file, well_data

def display_metadata(las):
    """Displays the metadata of the .las file."""
    st.subheader(".las File Metadata")
    st.write("Well Information:", las.well)
    st.write("Parameters:", las.params)
    st.write("Available Curves:", [curve.mnemonic for curve in las.curves])

def app():
    """Main function to run the Streamlit application."""
    st.title("Well Logs Analysis")
    st.write("Welcome to the interactive well logs analysis tool.")

    las = load_file()

    if las:
        display_metadata(las)

        if st.checkbox("Show Curve Data"):
            st.dataframe(las.df())

        selected_curves = st.multiselect(
            "Select curves to plot:",
            options=[curve.mnemonic for curve in las.curves]
        )

        # if selected_curves:
        #     plot_logs(las.df(), selected_curves)

        # if st.checkbox("Apply Clustering"):
        #     n_clusters = st.slider("Number of clusters:", min_value=2, max_value=10, value=3)
        #     clustered_data = apply_kmeans(las.df(), selected_curves, n_clusters)
        #     st.dataframe(clustered_data)

if __name__ == "__main__":
    app()
