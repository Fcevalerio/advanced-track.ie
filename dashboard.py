import streamlit as st
import pandas as pd
import plotly.express as px
from db2_connector import DB2Connector

st.set_page_config(
    page_title="SkyHigh Insights - Airline Executive Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("✈️ SkyHigh Insights")
st.markdown("### Executive Command Center for Airline Operations")
st.markdown("---")

if "connector" not in st.session_state:
    st.session_state.connector = DB2Connector()

st.success("✓ Connected to IBM DB2 database - IEMASTER")

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
st.sidebar.info("🗄️ IBM DB2 - IEMASTER\n\n✓ Connection Status: Active\n\n📊 Live Data Only")

# Add caching decorator
@st.cache_data(ttl=3600)
def get_total_revenue():
    return st.session_state.connector.get_total_revenue()

@st.cache_data(ttl=3600)
def get_load_factor():
    return st.session_state.connector.get_load_factor()

@st.cache_data(ttl=3600)
def get_fleet_utilization():
    return st.session_state.connector.get_fleet_utilization()

@st.cache_data(ttl=3600)
def get_passenger_demographics():
    return st.session_state.connector.get_passenger_demographics()

@st.cache_data(ttl=3600)
def get_financial_trends():
    return st.session_state.connector.get_financial_trends()

@st.cache_data(ttl=3600)
def get_revenue_by_route():
    return st.session_state.connector.get_revenue_by_route()

@st.cache_data(ttl=3600)
def get_fuel_efficiency():
    return st.session_state.connector.get_fuel_efficiency()

@st.cache_data(ttl=3600)
def get_maintenance_alerts():
    return st.session_state.connector.get_maintenance_alerts()

@st.cache_data(ttl=3600)
def get_route_network():
    return st.session_state.connector.get_route_network()

@st.cache_data(ttl=3600)
def get_hr_metrics():
    return st.session_state.connector.get_hr_metrics()

if page == "Executive Summary":
    st.header("📊 Executive Summary - High-Level Overview")

    col1, col2, col3, col4 = st.columns(4)

    with st.spinner("Loading key metrics..."):
        # Load all metrics in parallel
        total_rev_df = get_total_revenue()
        load_factor_df = get_load_factor()
        fleet_util_df = get_fleet_utilization()
        pax_demo_df = get_passenger_demographics()

    with col1:
        if not total_rev_df.empty:
            col_name = "TOTAL_REVENUE" if "TOTAL_REVENUE" in total_rev_df.columns else "total_revenue"
            total_revenue = total_rev_df.iloc[0][col_name]
            try:
                total_revenue = float(total_revenue)
                st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
            except (ValueError, TypeError):
                st.metric("💰 Total Revenue", "N/A")
        else:
            st.metric("💰 Total Revenue", "N/A")

    with col2:
        if not load_factor_df.empty:
            load_col = "LOAD_FACTOR" if "LOAD_FACTOR" in load_factor_df.columns else "load_factor"
            try:
                avg_load_factor = float(load_factor_df[load_col].mean())
                st.metric("🎯 Avg Load Factor", f"{avg_load_factor:.1f}%")
            except (ValueError, TypeError):
                st.metric("🎯 Avg Load Factor", "N/A")
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
            pax_col = "PASSENGER_COUNT" if "PASSENGER_COUNT" in pax_demo_df.columns else "passenger_count"
            try:
                total_passengers = int(pax_demo_df[pax_col].sum())
                st.metric("👥 Total Passengers", f"{total_passengers:,.0f}")
            except (ValueError, TypeError):
                st.metric("👥 Total Passengers", "N/A")
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

    financial_trends = get_financial_trends()
    if not financial_trends.empty:
        date_col = "FLIGHT_DATE" if "FLIGHT_DATE" in financial_trends.columns else "flight_date"
        rev_col = "DAILY_REVENUE" if "DAILY_REVENUE" in financial_trends.columns else "daily_revenue"
        
        financial_trends[rev_col] = pd.to_numeric(financial_trends[rev_col], errors='coerce')
        financial_trends = financial_trends.sort_values(date_col)
        
        fig = px.line(
            financial_trends,
            x=date_col,
            y=rev_col,
            title="Daily Revenue Trend",
            labels={date_col: "Date", rev_col: "Revenue ($)"},
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No financial trend data available.")


elif page == "Financial Performance":
    st.header("💰 Financial Performance - The Bottom Line")

    tab1, tab2, tab3 = st.tabs(["Revenue Overview", "Route Profitability", "Ticket Analysis"])

    with tab1:
        st.subheader("Total Revenue & Ticket Metrics")

        total_rev_df = get_total_revenue()
        if not total_rev_df.empty:
            col_name = "TOTAL_REVENUE" if "TOTAL_REVENUE" in total_rev_df.columns else "total_revenue"
            total_revenue = total_rev_df.iloc[0][col_name]
            try:
                total_revenue = float(total_revenue)
                st.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
            except (ValueError, TypeError):
                st.metric("💰 Total Revenue", "N/A")

        col1, col2 = st.columns(2)

        with col1:
            revenue_by_route = get_revenue_by_route()
            if not revenue_by_route.empty:
                origin_col = "ORIGIN" if "ORIGIN" in revenue_by_route.columns else "origin"
                dest_col = "DESTINATION" if "DESTINATION" in revenue_by_route.columns else "destination"
                rev_col = "TOTAL_REVENUE" if "TOTAL_REVENUE" in revenue_by_route.columns else "total_revenue"
                fig = px.bar(
                    revenue_by_route.head(10),
                    x=origin_col,
                    y=rev_col,
                    color=dest_col,
                    title="Top 10 Routes by Revenue",
                    labels={rev_col: "Revenue ($)", origin_col: "Origin"},
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            if not revenue_by_route.empty:
                origin_col = "ORIGIN" if "ORIGIN" in revenue_by_route.columns else "origin"
                rev_col = "TOTAL_REVENUE" if "TOTAL_REVENUE" in revenue_by_route.columns else "total_revenue"
                fig = px.pie(
                    revenue_by_route.head(8),
                    values=rev_col,
                    names=origin_col,
                    title="Revenue Distribution by Origin",
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Route Profitability Analysis")

        revenue_by_route = get_revenue_by_route()
        if not revenue_by_route.empty:
            # Convert numeric columns to float
            rev_col = "TOTAL_REVENUE" if "TOTAL_REVENUE" in revenue_by_route.columns else "total_revenue"
            ticket_col = "TICKET_COUNT" if "TICKET_COUNT" in revenue_by_route.columns else "ticket_count"
            price_col = "AVG_TICKET_PRICE" if "AVG_TICKET_PRICE" in revenue_by_route.columns else "avg_ticket_price"
            
            revenue_by_route[rev_col] = pd.to_numeric(revenue_by_route[rev_col], errors='coerce')
            revenue_by_route[ticket_col] = pd.to_numeric(revenue_by_route[ticket_col], errors='coerce')
            revenue_by_route[price_col] = pd.to_numeric(revenue_by_route[price_col], errors='coerce')
            
            origin_col = "ORIGIN" if "ORIGIN" in revenue_by_route.columns else "origin"
            dest_col = "DESTINATION" if "DESTINATION" in revenue_by_route.columns else "destination"
            
            st.dataframe(
                revenue_by_route[
                    [origin_col, dest_col, rev_col, ticket_col, price_col]
                ].sort_values(rev_col, ascending=False),
                use_container_width=True,
                height=500,
            )
        else:
            st.info("No route profitability data available.")

    with tab3:
        st.subheader("Avg Ticket Price by Route")

        revenue_by_route = get_revenue_by_route()
        if not revenue_by_route.empty:
            ticket_col = "TICKET_COUNT" if "TICKET_COUNT" in revenue_by_route.columns else "ticket_count"
            price_col = "AVG_TICKET_PRICE" if "AVG_TICKET_PRICE" in revenue_by_route.columns else "avg_ticket_price"
            rev_col = "TOTAL_REVENUE" if "TOTAL_REVENUE" in revenue_by_route.columns else "total_revenue"
            origin_col = "ORIGIN" if "ORIGIN" in revenue_by_route.columns else "origin"
            
            # Convert to numeric - IMPORTANT for plotting
            revenue_by_route[ticket_col] = pd.to_numeric(revenue_by_route[ticket_col], errors='coerce')
            revenue_by_route[price_col] = pd.to_numeric(revenue_by_route[price_col], errors='coerce')
            revenue_by_route[rev_col] = pd.to_numeric(revenue_by_route[rev_col], errors='coerce')
            
            # Remove rows with NaN values
            revenue_by_route = revenue_by_route.dropna(subset=[ticket_col, price_col, rev_col])
            
            if not revenue_by_route.empty:
                fig = px.scatter(
                    revenue_by_route,
                    x=ticket_col,
                    y=price_col,
                    size=rev_col,
                    hover_name=origin_col,
                    title="Ticket Volume vs Price",
                    labels={
                        ticket_col: "Tickets Sold",
                        price_col: "Average Price ($)",
                    },
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No valid data to display scatter plot.")
        else:
            st.info("No route profitability data available.")

elif page == "Fleet Operations":
    st.header("🛠️ Fleet Operations & Efficiency")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Fleet Utilization", "Fuel Efficiency", "Load Factor", "Maintenance Status"]
    )

    with tab1:
        st.subheader("Fleet Utilization Metrics")

        fleet_util = get_fleet_utilization()
        if not fleet_util.empty:
            dist_col = "TOTAL_FLIGHT_DISTANCE" if "TOTAL_FLIGHT_DISTANCE" in fleet_util.columns else "total_flight_distance"
            flights_col = "TOTAL_FLIGHTS" if "TOTAL_FLIGHTS" in fleet_util.columns else "total_flights"
            reg_col = "AIRCRAFT_REGISTRATION" if "AIRCRAFT_REGISTRATION" in fleet_util.columns else "aircraft_registration"
            model_col = "MODEL" if "MODEL" in fleet_util.columns else "model"
            seats_col = "TOTAL_SEATS" if "TOTAL_SEATS" in fleet_util.columns else "total_seats"
            
            # Convert to numeric
            fleet_util[dist_col] = pd.to_numeric(fleet_util[dist_col], errors='coerce')
            fleet_util[flights_col] = pd.to_numeric(fleet_util[flights_col], errors='coerce')
            
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Aircraft", len(fleet_util))

            with col2:
                avg_distance = fleet_util[dist_col].mean()
                st.metric("Avg Flight Distance", f"{avg_distance:,.0f} miles")

            with col3:
                avg_flights = fleet_util[flights_col].mean()
                st.metric("Avg Flights per Aircraft", f"{avg_flights:.0f}")

            st.dataframe(
                fleet_util[
                    [
                        reg_col,
                        model_col,
                        seats_col,
                        dist_col,
                        flights_col,
                    ]
                ].sort_values(flights_col, ascending=False),
                use_container_width=True,
                height=400,
            )

    with tab2:
        st.subheader("Fuel Efficiency Leaderboard")

        fuel_eff = get_fuel_efficiency()
        if not fuel_eff.empty:
            model_col = "MODEL" if "MODEL" in fuel_eff.columns else "model"
            fuel_col = "AVG_FUEL_CONSUMPTION" if "AVG_FUEL_CONSUMPTION" in fuel_eff.columns else "avg_fuel_consumption"
            aircraft_col = "AIRCRAFT_COUNT" if "AIRCRAFT_COUNT" in fuel_eff.columns else "aircraft_count"
            
            # Convert to numeric
            fuel_eff[fuel_col] = pd.to_numeric(fuel_eff[fuel_col], errors='coerce')
            fuel_eff[aircraft_col] = pd.to_numeric(fuel_eff[aircraft_col], errors='coerce')
            
            fig = px.bar(
                fuel_eff.sort_values(fuel_col),
                x=model_col,
                y=fuel_col,
                color=aircraft_col,
                title="Fuel Consumption by Aircraft Model (Lower is Better)",
                labels={
                    fuel_col: "Avg Fuel (gal/hr)",
                    model_col: "Aircraft Model",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                fuel_eff.sort_values(fuel_col),
                use_container_width=True,
            )

    with tab3:
        st.subheader("Load Factor Analysis")

        load_factor = get_load_factor()
        if not load_factor.empty:
            load_col = "LOAD_FACTOR" if "LOAD_FACTOR" in load_factor.columns else "load_factor"
            cap_col = "CAPACITY" if "CAPACITY" in load_factor.columns else "capacity"
            pax_col = "PASSENGERS_BOOKED" if "PASSENGERS_BOOKED" in load_factor.columns else "passengers_booked"
            flight_col = "FLIGHT_ID" if "FLIGHT_ID" in load_factor.columns else "flight_id"
            origin_col = "ORIGIN" if "ORIGIN" in load_factor.columns else "origin"
            dest_col = "DESTINATION" if "DESTINATION" in load_factor.columns else "destination"
            
            # Convert to numeric
            load_factor[load_col] = pd.to_numeric(load_factor[load_col], errors='coerce')
            load_factor[cap_col] = pd.to_numeric(load_factor[cap_col], errors='coerce')
            load_factor[pax_col] = pd.to_numeric(load_factor[pax_col], errors='coerce')
            
            col1, col2, col3 = st.columns(3)

            with col1:
                avg_lf = load_factor[load_col].mean()
                st.metric("Average Load Factor", f"{avg_lf:.1f}%")

            with col2:
                max_lf = load_factor[load_col].max()
                st.metric("Max Load Factor", f"{max_lf:.1f}%")

            with col3:
                min_lf = load_factor[load_col].min()
                st.metric("Min Load Factor", f"{min_lf:.1f}%")

            fig = px.histogram(
                load_factor,
                x=load_col,
                nbins=20,
                title="Load Factor Distribution",
                labels={load_col: "Load Factor (%)"},
            )
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                load_factor[
                    [flight_col, origin_col, dest_col, cap_col, pax_col, load_col]
                ].sort_values(load_col, ascending=False).head(20),
                use_container_width=True,
            )

    with tab4:
        st.subheader("Maintenance Status Alerts")

        maintenance = get_maintenance_alerts()
        if not maintenance.empty:
            status_col = "MAINTENANCE_STATUS" if "MAINTENANCE_STATUS" in maintenance.columns else "maintenance_status"
            reg_col = "AIRCRAFT_REGISTRATION" if "AIRCRAFT_REGISTRATION" in maintenance.columns else "aircraft_registration"
            model_col = "MODEL" if "MODEL" in maintenance.columns else "model"
            takeoffs_col = "MAINTENANCE_TAKEOFFS" if "MAINTENANCE_TAKEOFFS" in maintenance.columns else "maintenance_takeoffs"
            
            status_colors = {
                "CRITICAL": "🔴 CRITICAL",
                "HIGH": "🟡 HIGH",
                "MEDIUM": "🟠 MEDIUM",
                "LOW": "🟢 LOW",
            }

            maintenance["Status"] = maintenance[status_col].map(status_colors)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                critical = len(maintenance[maintenance[status_col] == "CRITICAL"])
                st.metric("🔴 Critical", critical)

            with col2:
                high = len(maintenance[maintenance[status_col] == "HIGH"])
                st.metric("🟡 High", high)

            with col3:
                medium = len(maintenance[maintenance[status_col] == "MEDIUM"])
                st.metric("🟠 Medium", medium)

            with col4:
                low = len(maintenance[maintenance[status_col] == "LOW"])
                st.metric("🟢 Low", low)

            st.dataframe(
                maintenance[
                    [reg_col, model_col, takeoffs_col, "Status"]
                ],
                use_container_width=True,
            )

elif page == "Route Network":
    st.header("🗺️ Commercial & Route Network Analysis")

    tab1, tab2, tab3 = st.tabs(["Route Heatmap", "Load Factor by Route", "Passenger Demographics"])

    with tab1:
        st.subheader("Route Network Visualization")

        route_network = get_route_network()
        if not route_network.empty:
            st.info("🔍 Interactive Map: Shows busiest routes with flight counts and passenger volumes")

            origin_lat_col = "ORIGIN_LAT" if "ORIGIN_LAT" in route_network.columns else "origin_lat"
            origin_lon_col = "ORIGIN_LON" if "ORIGIN_LON" in route_network.columns else "origin_lon"
            flight_col = "FLIGHT_COUNT" if "FLIGHT_COUNT" in route_network.columns else "flight_count"
            pax_col = "PASSENGER_COUNT" if "PASSENGER_COUNT" in route_network.columns else "passenger_count"
            origin_col = "ORIGIN" if "ORIGIN" in route_network.columns else "origin"
            dest_col = "DESTINATION" if "DESTINATION" in route_network.columns else "destination"
            
            # Convert to numeric
            route_network[flight_col] = pd.to_numeric(route_network[flight_col], errors='coerce')
            route_network[pax_col] = pd.to_numeric(route_network[pax_col], errors='coerce')
            route_network[origin_lat_col] = pd.to_numeric(route_network[origin_lat_col], errors='coerce')
            route_network[origin_lon_col] = pd.to_numeric(route_network[origin_lon_col], errors='coerce')

            fig = px.scatter_geo(
                route_network,
                lat=origin_lat_col,
                lon=origin_lon_col,
                size=flight_col,
                color=pax_col,
                hover_name=origin_col,
                title="Airport Activity Distribution",
                scope="world",
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Top Routes by Volume")
            st.dataframe(
                route_network[
                    [origin_col, dest_col, flight_col, pax_col]
                ].sort_values(flight_col, ascending=False).head(20),
                use_container_width=True,
            )

    with tab2:
        st.subheader("Load Factor by Route")

        load_factor = get_load_factor()
        if not load_factor.empty:
            origin_col = "ORIGIN" if "ORIGIN" in load_factor.columns else "origin"
            load_col = "LOAD_FACTOR" if "LOAD_FACTOR" in load_factor.columns else "load_factor"
            flight_col = "FLIGHT_ID" if "FLIGHT_ID" in load_factor.columns else "flight_id"
            
            load_factor[load_col] = pd.to_numeric(load_factor[load_col], errors='coerce')
            
            route_lf = (
                load_factor.groupby(origin_col)
                .agg({load_col: "mean", flight_col: "count"})
                .reset_index()
                .rename(columns={flight_col: "flight_count"})
            )

            fig = px.bar(
                route_lf.sort_values(load_col, ascending=False).head(15),
                x=origin_col,
                y=load_col,
                color="flight_count",
                title="Average Load Factor by Origin Airport",
                labels={load_col: "Avg Load Factor (%)", origin_col: "Origin"},
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Passenger Demographics")

        pax_demo = get_passenger_demographics()
        if not pax_demo.empty:
            gender_col = "GENDER" if "GENDER" in pax_demo.columns else "gender"
            pax_col = "PASSENGER_COUNT" if "PASSENGER_COUNT" in pax_demo.columns else "passenger_count"
            age_col = "AVG_AGE" if "AVG_AGE" in pax_demo.columns else "avg_age"
            
            pax_demo[pax_col] = pd.to_numeric(pax_demo[pax_col], errors='coerce')
            pax_demo[age_col] = pd.to_numeric(pax_demo[age_col], errors='coerce')
            
            col1, col2 = st.columns(2)

            with col1:
                fig = px.pie(
                    pax_demo,
                    values=pax_col,
                    names=gender_col,
                    title="Passenger Gender Distribution",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(
                    pax_demo,
                    x=gender_col,
                    y=age_col,
                    title="Average Age by Gender",
                    labels={age_col: "Average Age", gender_col: "Gender"},
                )
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                pax_demo,
                use_container_width=True,
            )

elif page == "HR Analytics":
    st.header("👔 Human Resources Analytics")

    st.subheader("Headcount & Budget by Department")

    hr_metrics = get_hr_metrics()
    if not hr_metrics.empty:
        deptname_col = "DEPTNAME" if "DEPTNAME" in hr_metrics.columns else "deptname"
        headcount_col = "HEADCOUNT" if "HEADCOUNT" in hr_metrics.columns else "headcount"
        salary_col = "TOTAL_SALARY" if "TOTAL_SALARY" in hr_metrics.columns else "total_salary"
        avg_salary_col = "AVG_SALARY" if "AVG_SALARY" in hr_metrics.columns else "avg_salary"
        
        # Convert numeric columns
        hr_metrics[headcount_col] = pd.to_numeric(hr_metrics[headcount_col], errors='coerce')
        hr_metrics[salary_col] = pd.to_numeric(hr_metrics[salary_col], errors='coerce')
        hr_metrics[avg_salary_col] = pd.to_numeric(hr_metrics[avg_salary_col], errors='coerce')
        
        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                hr_metrics.sort_values(headcount_col, ascending=False),
                x=deptname_col,
                y=headcount_col,
                title="Headcount by Department",
                labels={headcount_col: "Number of Employees", deptname_col: "Department"},
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                hr_metrics,
                values=salary_col,
                names=deptname_col,
                title="Salary Budget Distribution",
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Department Details")

        total_employees = int(hr_metrics[headcount_col].sum())
        total_budget = float(hr_metrics[salary_col].sum())
        avg_salary = float(hr_metrics[avg_salary_col].mean())

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
