import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# ==========================================
# PART 1: GRAPHS FROM data.json
# ==========================================

with open("data.json", "r") as file:
    data = json.load(file)

planets = data["planets"]

planetNames = []
diameters = []

for planet in planets:
    planetNames.append(planet["name"])
    diameters.append(planet["diameter_km"])


st.header("Solar System Explorer")

tab1, tab2 = st.tabs([
    "Planet Diameters",
    "Interactive Comparison"
])


# STATIC BAR CHART
with tab1:

    st.subheader("Planet Diameters in the Solar System")

    chart_data = {
        "Planet": planetNames,
        "Diameter (km)": diameters
    }

    st.bar_chart(
        chart_data,
        x="Planet",
        y="Diameter (km)"
    )


# DYNAMIC SCATTER PLOT
with tab2:

    attribute_options = {
        "Diameter (km)": "diameter_km",
        "Distance from Sun (AU)": "distance_from_sun_au",
        "Orbital Period (days)": "orbital_period_days"
    }

    selected_label = st.selectbox(
        "Choose a planet attribute:",
        list(attribute_options.keys()),
        key="planet_attribute"
    )

    selected_attribute = attribute_options[selected_label]

    selected_values = []

    for planet in planets:
        selected_values.append(planet[selected_attribute])

    if selected_attribute == "diameter_km":
        y_label = "Diameter (km)"

    elif selected_attribute == "distance_from_sun_au":
        y_label = "Distance from Sun (AU)"

    else:
        y_label = "Orbital Period (days)"

    fig, ax = plt.subplots()

    ax.scatter(planetNames, selected_values)

    ax.set_xlabel("Planet")
    ax.set_ylabel(y_label)
    ax.set_title("Planet Comparison")

    plt.xticks(rotation=45)

    st.pyplot(fig)


# ==========================================
# PART 2: GRAPHS FROM data.csv
# ==========================================

st.header("Space Exploration Survey 🌌")


# Check whether survey data exists
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    # Read survey data
    survey_data = pd.read_csv("data.csv")

    # Convert Value column into numerical data
    survey_data["Value"] = pd.to_numeric(
        survey_data["Value"],
        errors="coerce"
    )

    survey_data = survey_data.dropna(subset=["Value"])

    if not survey_data.empty:

        tab3, tab4 = st.tabs([
            "Favorite Planets",
            "Space Exploration Interest"
        ])


        # ----------------------------------
        # STATIC BAR CHART
        # ----------------------------------

        with tab3:

            st.subheader("Most Popular Planets")

            # Count the number of responses for each planet
            planet_counts = survey_data["Category"].value_counts()

            st.bar_chart(
                planet_counts,
                x_label="Planet",
                y_label="Number of Responses"
            )


        # ----------------------------------
        # DYNAMIC SCATTER PLOT
        # ----------------------------------

        with tab4:

            st.subheader("Interest in Space Exploration")

            # Initialize session state
            if "previous_mean" not in st.session_state:
                st.session_state.previous_mean = None

            if "previous_median" not in st.session_state:
                st.session_state.previous_median = None


            # Slider to filter survey responses
            minimum_interest = st.slider(
                "Show responses with at least this interest level:",
                min_value=1,
                max_value=10,
                value=1,
                key="interest_slider"
            )


            # Filter the survey data
            filtered_data = survey_data[
                survey_data["Value"] >= minimum_interest
            ]


            if not filtered_data.empty:

                # Calculate mean and median
                mean_interest = filtered_data["Value"].mean()

                median_interest = filtered_data["Value"].median()


                # Calculate the change from previous values
                mean_change = None
                median_change = None

                if st.session_state.previous_mean is not None:

                    mean_change = round(
                        mean_interest - st.session_state.previous_mean,
                        2
                    )

                if st.session_state.previous_median is not None:

                    median_change = round(
                        median_interest - st.session_state.previous_median,
                        2
                    )


                # Display statistics
                col1, col2 = st.columns(2)

                col1.metric(
                    "Mean Interest",
                    round(mean_interest, 2),
                    delta=mean_change
                )

                col2.metric(
                    "Median Interest",
                    round(median_interest, 2),
                    delta=median_change
                )


                # Save current values in session state
                st.session_state.previous_mean = mean_interest

                st.session_state.previous_median = median_interest


                # Create scatter plot
                fig, ax = plt.subplots()

                ax.scatter(
                    filtered_data["Category"],
                    filtered_data["Value"]
                )

                ax.set_xlabel("Favorite Planet")
                ax.set_ylabel("Interest Level (1-10)")
                ax.set_title("Space Exploration Interest")

                plt.xticks(rotation=45)

                st.pyplot(fig)


            else:

                st.warning(
                    "No responses match this interest level."
                )


    else:

        st.warning(
            "Your CSV does not contain valid numerical data."
        )


else:

    st.warning(
        "No survey responses yet! Please submit some data using Survey.py."
    )
