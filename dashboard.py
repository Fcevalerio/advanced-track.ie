import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db2_connector import DB2Connector
import time

# Page configuration
st.set_page_config(
    page_title="SkyHigh Insights - Airline Executive Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Title and branding
st.title("✈️ SkyHigh Insights")
st.markdown("### Executive Command Center for Airline Operations")
st.markdown("---")

# Initialize session state
if "connector" not in st.session_state:
    try:
        st.session_state.connector = DB2Connector()
        st.session_state.connector.test_connection()
        st.session_state.use_mock = st.session_state.connector.use_mock
    except Exception as e:
        st.session_state.use_mock = True
        st.session_state.connector = DB2Connector()
        st.session_state.connector.use_mock = True

# Display mode indicator
if st.session_state.use_mock:
    st.warning("📊 Running in Mock Data Mode - Database unavailable. All features work with sample data.")
else:
    st.success("✓ Connected to IBM DB2 database")


# Sidebar for navigation
st.sidebar.title("📍 Navigation")
page = st.sidebar.radio(
    "Select Dashboard Page:",
    [
        "Executive Summary",
        "Financial Performance",
        "Fleet Operations",
        "Route Network",
        "HR Analytics",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Database Info")
if st.session_state.use_mock:
    st.sidebar.warning("🗄️ IBM DB2 - IEMASTER\n\n⚠️ Using Mock Data")
else:
    st.sidebar.info("🗄️ IBM DB2 - IEMASTER\n\n✓ Connection Status: Active")


# PAGE 1: Executive Summary
if page == "Executive Summary":
    st.header("📊 Executive Summary - High-Level Overview")

    col1, col2, col3, col4 = st.columns(4)

    # Fetch key metrics
    with st.spinner("Loading key metrics..."):
        total_rev_df = st.session_state.connector.get_total_revenue()
        load_factor_df = st.session_state.connector.get_load_factor()
        fleet_util_df = st.session_state.connector.get_fleet_utilization()
        pax_demo_df = st.session_state.connector.get_passenger_demographics()

    # Display KPI cards
    with col1:
        if not total_rev_df.empty:
            total_revenue = total_rev_df.iloc[0]["total_revenue"]
            st.metric("💰 Total Revenue", f"${total_revenue:,.2f}" if total_revenue else "N/A")
        else:
            st.metric("💰 Total Revenue", "N/A")

    with col2:
        if not load_factor_df.empty:
            avg_load_factor = load_factor_df["load_factor"].mean()
            st.metric("🎯 Avg Load Factor", f"{avg_load_factor:.1f}%")
        else:
            st.metric("🎯 Avg Load Factor", "N/A")

    with col3:
        if not fleet_util_df.empty:
            active_fleet = len(fleet_util_df)
            st.metric("✈️ Active Fleet", f"{active_fleet} aircraft")
        else:
            st.metric("✈️ Active Fleet", "N/A")

    with col4:
        if not pax_demo_df.empty:
            total_passengers = pax_demo_df["passenger_count"].sum()
            st.metric("👥 Total Passengers", f"{total_passengers:,.0f}")
        else:
            st.metric("👥 Total Passengers", "N/A")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💡 Key Insights")
        insights = [
            "Monitor revenue trends to optimize pricing strategies",
            "High load factors indicate good seat utilization",
            "Fleet utilization drives operational efficiency",
            "Passenger demographics guide marketing initiatives",
        ]
        for insight in insights:
            st.markdown(f"• {insight}")

    with col2:
        st.subheader("⚡ Quick Actions")
        actions = [
            "📊 View detailed financial reports",
            "🔧 Check fleet maintenance status",
            "🗺️ Analyze route profitability",
            "👔 Review HR metrics by department",
        ]
        for action in actions:
            st.markdown(f"• {action}")

    st.markdown("---")
    st.subheader("📈 Revenue Trends")

    financial_trends = st.session_state.connector.get_financial_trends()
    if not financial_trends.empty:
        financial_trends = financial_trends.sort_values("flight_date")
        fig = px.line(
            financial_trends,
            x="flight_date",
            y="daily_revenue",
            title="Daily Revenue Trend",
            labels={"flight_date": "Date", "daily_revenue": "Revenue ($)"},
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No financial trend data available.")


# PAGE 2: Financial Performance
elif page == "Financial Performance":
    st.header("💰 Financial Performance - The Bottom Line")

    tab1, tab2, tab3 = st.tabs(["Revenue Overview", "Route Profitability", "Ticket Analysis"])

    with tab1:
        st.subheader("Total Revenue & Ticket Metrics")

        total_rev_df = st.session_state.connector.get_total_revenue()
        if not total_rev_df.empty:
            total_revenue = total_rev_df.iloc[0]["total_revenue"]
            st.metric("💰 Total Revenue", f"${total_revenue:,.2f}" if total_revenue else "N/A")

        col1, col2 = st.columns(2)

        with col1:
            revenue_by_route = st.session_state.connector.get_revenue_by_route()
            if not revenue_by_route.empty:
                fig = px.bar(
                    revenue_by_route.head(10),
                    x="origin",
                    y="total_revenue",
                    color="destination",
                    title="Top 10 Routes by Revenue",
                    labels={"total_revenue": "Revenue ($)", "origin": "Origin"},
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if not revenue_by_route.empty:
                fig = px.pie(
                    revenue_by_route.head(8),
                    values="total_revenue",
                    names="origin",
                    title="Revenue Distribution by Origin",
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Route Profitability Analysis")

        revenue_by_route = st.session_state.connector.get_revenue_by_route()
        if not revenue_by_route.empty:
            st.dataframe(
                revenue_by_route[
                    ["origin", "destination", "total_revenue", "ticket_count", "avg_ticket_price"]
                ].sort_values("total_revenue", ascending=False),
                use_container_width=True,
                height=500,
            )
        else:
            st.info("No route profitability data available.")

    with tab3:
        st.subheader("Avg Ticket Price by Route")

        revenue_by_route = st.session_state.connector.get_revenue_by_route()
        if not revenue_by_route.empty:
            fig = px.scatter(
                revenue_by_route,
                x="ticket_count",
                y="avg_ticket_price",
                size="total_revenue",
                hover_name="origin",
                title="Ticket Volume vs Price",
                labels={
                    "ticket_count": "Tickets Sold",
                    "avg_ticket_price": "Average Price ($)",
                },
            )
            st.plotly_chart(fig, use_container_width=True)


# PAGE 3: Fleet Operations
elif page == "Fleet Operations":
    st.header("🛠️ Fleet Operations & Efficiency")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Fleet Utilization", "Fuel Efficiency", "Load Factor", "Maintenance Status"]
    )

    with tab1:
        st.subheader("Fleet Utilization Metrics")

        fleet_util = st.session_state.connector.get_fleet_utilization()
        if not fleet_util.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Aircraft", len(fleet_util))

            with col2:
                avg_distance = fleet_util["TOTAL_FLIGHT_DISTANCE"].mean()
                st.metric("Avg Flight Distance", f"{avg_distance:,.0f} miles")

            with col3:
                avg_flights = fleet_util["total_flights"].mean()
                st.metric("Avg Flights per Aircraft", f"{avg_flights:.0f}")

            # Display fleet table
            st.dataframe(
                fleet_util[
                    [
                        "AIRPLANE_ID",
                        "MODEL",
                        "REGISTRATION_NUMBER",
                        "TOTAL_FLIGHT_DISTANCE",
                        "total_flights",
                    ]
                ].sort_values("total_flights", ascending=False),
                use_container_width=True,
                height=400,
            )

    with tab2:
        st.subheader("Fuel Efficiency Leaderboard")

        fuel_eff = st.session_state.connector.get_fuel_efficiency()
        if not fuel_eff.empty:
            fig = px.bar(
                fuel_eff.sort_values("avg_fuel_consumption"),
                x="MODEL",
                y="avg_fuel_consumption",
                color="aircraft_count",
                title="Fuel Consumption by Aircraft Model (Lower is Better)",
                labels={
                    "avg_fuel_consumption": "Avg Fuel (gal/hr)",
                    "MODEL": "Aircraft Model",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                fuel_eff.sort_values("avg_fuel_consumption"),
                use_container_width=True,
            )

    with tab3:
        st.subheader("Load Factor Analysis")

        load_factor = st.session_state.connector.get_load_factor()
        if not load_factor.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                avg_lf = load_factor["load_factor"].mean()
                st.metric("Average Load Factor", f"{avg_lf:.1f}%")

            with col2:
                max_lf = load_factor["load_factor"].max()
                st.metric("Max Load Factor", f"{max_lf:.1f}%")

            with col3:
                min_lf = load_factor["load_factor"].min()
                st.metric("Min Load Factor", f"{min_lf:.1f}%")

            # Load factor distribution
            fig = px.histogram(
                load_factor,
                x="load_factor",
                nbins=20,
                title="Load Factor Distribution",
                labels={"load_factor": "Load Factor (%)"},
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                load_factor[
                    ["FLIGHT_ID", "origin", "destination", "CAPACITY", "passengers_booked", "load_factor"]
                ].sort_values("load_factor", ascending=False).head(20),
                use_container_width=True,
            )

    with tab4:
        st.subheader("Maintenance Status Alerts")

        maintenance = st.session_state.connector.get_maintenance_alerts()
        if not maintenance.empty:
            # Color code maintenance status
            status_colors = {
                "CRITICAL": "🔴 CRITICAL",
                "HIGH": "🟡 HIGH",
                "MEDIUM": "🟠 MEDIUM",
                "LOW": "🟢 LOW",
            }

            maintenance["Status"] = maintenance["maintenance_status"].map(status_colors)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                critical = len(maintenance[maintenance["maintenance_status"] == "CRITICAL"])
                st.metric("🔴 Critical", critical)

            with col2:
                high = len(maintenance[maintenance["maintenance_status"] == "HIGH"])
                st.metric("🟡 High", high)

            with col3:
                medium = len(maintenance[maintenance["maintenance_status"] == "MEDIUM"])
                st.metric("🟠 Medium", medium)

            with col4:
                low = len(maintenance[maintenance["maintenance_status"] == "LOW"])
                st.metric("🟢 Low", low)

            st.dataframe(
                maintenance[
                    ["AIRPLANE_ID", "MODEL", "REGISTRATION_NUMBER", "MAINTENANCE_TAKEOFFS", "Status"]
                ],
                use_container_width=True,
            )


# PAGE 4: Route Network
elif page == "Route Network":
    st.header("🗺️ Commercial & Route Network Analysis")

    tab1, tab2, tab3 = st.tabs(["Route Heatmap", "Load Factor by Route", "Passenger Demographics"])

    with tab1:
        st.subheader("Route Network Visualization")

        route_network = st.session_state.connector.get_route_network()
        if not route_network.empty:
            st.info("🔍 Interactive Map: Shows busiest routes with flight counts and passenger volumes")

            # Create scatter plot on map
            fig = px.scatter_geo(
                route_network,
                lat="origin_lat",
                lon="origin_lon",
                size="flight_count",
                color="passenger_count",
                hover_name="origin",
                title="Airport Activity Distribution",
                scope="world",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Top routes table
            st.subheader("Top Routes by Volume")
            st.dataframe(
                route_network[
                    ["origin", "destination", "flight_count", "passenger_count"]
                ].sort_values("flight_count", ascending=False).head(20),
                use_container_width=True,
            )

    with tab2:
        st.subheader("Load Factor by Route")

        load_factor = st.session_state.connector.get_load_factor()
        if not load_factor.empty:
            # Aggregate by route
            route_lf = (
                load_factor.groupby("origin")
                .agg({"load_factor": "mean", "FLIGHT_ID": "count"})
                .reset_index()
                .rename(columns={"FLIGHT_ID": "flight_count"})
            )

            fig = px.bar(
                route_lf.sort_values("load_factor", ascending=False).head(15),
                x="origin",
                y="load_factor",
                color="flight_count",
                title="Average Load Factor by Origin Airport",
                labels={"load_factor": "Avg Load Factor (%)", "origin": "Origin"},
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Passenger Demographics")

        pax_demo = st.session_state.connector.get_passenger_demographics()
        if not pax_demo.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig = px.pie(
                    pax_demo,
                    values="passenger_count",
                    names="GENDER",
                    title="Passenger Gender Distribution",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(
                    pax_demo,
                    x="GENDER",
                    y="avg_age",
                    title="Average Age by Gender",
                    labels={"avg_age": "Average Age", "GENDER": "Gender"},
                )
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                pax_demo,
                use_container_width=True,
            )


# PAGE 5: HR Analytics
elif page == "HR Analytics":
    st.header("👔 Human Resources Analytics")

    st.subheader("Headcount & Budget by Department")

    hr_metrics = st.session_state.connector.get_hr_metrics()
    if not hr_metrics.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                hr_metrics.sort_values("headcount", ascending=False),
                x="DEPARTMENT_NAME",
                y="headcount",
                title="Headcount by Department",
                labels={"headcount": "Number of Employees", "DEPARTMENT_NAME": "Department"},
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                hr_metrics,
                values="total_salary",
                names="DEPARTMENT_NAME",
                title="Salary Budget Distribution",
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Department Details")

        # Add summary metrics
        total_employees = hr_metrics["headcount"].sum()
        total_budget = hr_metrics["total_salary"].sum()
        avg_salary = hr_metrics["avg_salary"].mean()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Employees", f"{total_employees:,.0f}")

        with col2:
            st.metric("Total Salary Budget", f"${total_budget:,.0f}")

        with col3:
            st.metric("Average Salary", f"${avg_salary:,.2f}")

        st.dataframe(
            hr_metrics,
            use_container_width=True,
        )

st.markdown("---")
st.caption("© 2026 SkyHigh Insights - Airline Executive Dashboard")
