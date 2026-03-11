{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \{\\rtf1\\ansi\\ansicpg1252\\cocoartf2867\
\\cocoatextscaling0\\cocoaplatform0\{\\fonttbl\\f0\\fswiss\\fcharset0 Helvetica;\}\
\{\\colortbl;\\red255\\green255\\blue255;\}\
\{\\*\\expandedcolortbl;;\}\
\\margl1440\\margr1440\\vieww11520\\viewh8400\\viewkind0\
\\pard\\tx720\\tx1440\\tx2160\\tx2880\\tx3600\\tx4320\\tx5040\\tx5760\\tx6480\\tx7200\\tx7920\\tx8640\\pardirnatural\\partightenfactor0\
\
\\f0\\fs24 \\cf0 import streamlit as st\\\
import pandas as pd\\\
\\\
st.title("Texas Tax-Sale Land Scoring Tool")\\\
\\\
# Upload CSV\\\
uploaded_file = st.file_uploader("Upload county GIS / tax-sale CSV", type="csv")\\\
if uploaded_file:\\\
    df = pd.read_csv(uploaded_file)\\\
    \\\
    # Define scoring function\\\
    def score_parcel(row):\\\
        score = 0\\\
        # Lot size scoring\\\
        if 1 <= row['LotSize'] <= 3:\\\
            score += 2\\\
        elif 3 < row['LotSize'] <= 5:\\\
            score += 1\\\
        # Road scoring\\\
        if row['RoadType'].lower() == 'paved':\\\
            score += 1\\\
        # Utilities\\\
        if row['ElectricityNearby']:\\\
            score += 2\\\
        # Flood risk\\\
        if row['Floodplain']:\\\
            score -= 2\\\
        # Slope\\\
        if row.get('Slope', 0) <= 15:\\\
            score += 1\\\
        return score\\\
\\\
    # Apply scoring\\\
    df['Score'] = df.apply(score_parcel, axis=1)\\\
    \\\
    # Calculate max bid\\\
    def max_bid(row, discount=0.6):\\\
        return row['MarketValue'] * discount\\\
    \\\
    df['MaxBid'] = df.apply(max_bid, axis=1)\\\
    \\\
    # Filter parcels with score >= threshold\\\
    threshold = st.slider("Minimum Score", 0, 10, 5)\\\
    filtered_df = df[df['Score'] >= threshold].sort_values(by='Score', ascending=False)\\\
    \\\
    st.subheader("Ranked Parcels")\\\
    st.dataframe(filtered_df)\\\
    \\\
    # Optional: download filtered list\\\
    st.download_button(\\\
        "Download Filtered Parcels",\\\
        filtered_df.to_csv(index=False),\\\
        file_name="filtered_parcels.csv",\\\
        mime="text/csv"\\\
    )\}}