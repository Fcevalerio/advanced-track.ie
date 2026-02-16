# Project Proposal: "SkyHigh Insights" - Executive Airline Dashboard

## Overview
Build a comprehensive **Executive Command Center** for the airline's CEO. This dashboard will provide real-time visibility into the airline's financial health, operational efficiency, and fleet status.

## Key Pillars & KPIs

### 1. Financial Performance (The Bottom Line)
*   **Total Revenue**: Aggregated from `TICKETS.total_amount`.
*   **Revenue per Available Seat Mile (RASM)**: A standard airline metric.
    *   *Formula*: Total Revenue / (Total Seats * Distance Flown).
*   **Route Profitability**: Identify the "Cash Cows" and "Money Pits".
    *   Compare Ticket Revenue against estimated costs (Fuel burn from `AIRPLANES` * Distance).
*   **Ancillary Revenue**: Analysis of `airport_tax` vs base `price`.

### 2. Fleet Operations & Efficiency
*   **Fleet Utilization**: Analysis of `AIRPLANES.total_flight_distance` and `flight_hours`.
*   **Maintenance Health**:
    *   Alert system for aircraft approaching maintenance thresholds (`maintenance_last_acheck`, `maintenance_takeoffs`).
*   **Fuel Efficiency Leaderboard**: Compare `fuel_gallons_hour` across different `models` to optimize fleet composition.

### 3. Commercial & Route Network
*   **Load Factor**: The percentage of seats filled.
    *   *Calculation*: Join `TICKETS` (count) with `FLIGHTS` and `AIRPLANES` (capacity).
*   **Route Heatmap**: Visualizing the busiest connections using `AIRPORTS` (lat/long) and `ROUTES`.
*   **Passenger Demographics**: Age and gender distribution from `PASSENGERS` to tailor marketing.

### 4. Human Resources
*   **Headcount & Budget**: `EMPLOYEE` counts and `salary` sums grouped by `DEPARTMENT`.
*   **Staffing Efficiency**: Ratio of `crew_members` (from Fleet) to total operational staff.

## Technical Architecture

### Data Pipeline
1.  **Extraction**: `SQLAlchemy` to pull raw data from DB2.
2.  **Transformation**: `Pandas` & `DuckDB` for complex joins (e.g., calculating Load Factor requires joining 3 tables).
3.  **Visualization**: `Streamlit` or `Plotly Dash` for the interactive web interface.

### Proposed Dashboard Pages
1.  **Executive Summary**: High-level cards (Total Revenue, Avg Load Factor, Active Fleet).
2.  **Route Network Map**: Interactive geospatial map of flights.
3.  **Fleet Manager**: Detailed table of aircraft status and maintenance needs.
4.  **Financial Deep Dive**: Revenue trends over time and by ticket class.

## Next Steps
1.  Write SQL queries to calculate **Load Factor** (the most complex metric).
2.  Create a basic Streamlit app structure.
3.  Implement the "Route Heatmap" using Plotly.
