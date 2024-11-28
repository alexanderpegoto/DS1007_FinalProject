# DS1007_FinalProject

This is the GitHub repository for the Course Project of the 2024 DS-GA 1007 - Programming for Data Science course from the MSDS from New York University.

We use the dataset from the NYC Taxi and Limousine Commision (TLC) about taxi fares in New York City for the year 2023, obtained from the official TLC data page.  Additional datasets: NYC 2023 Weather Dataset (Open Meteo Weather API), NYC Uber Rides (NYC Open Data - Rideshare dataset)

This dataset provides valuable insights into taxi fare distribution across different zones, distribution across hours, components of fares, and trip distances.

Objective:  The primary objective of this project is to analyze the patterns in NYC taxi fares throughout 2023, identifying key factors that influence fare amounts. By assessing the impact of each variable, we aim to provide taxi drivers insights that would help them optimize their service strategy.

# Project Structure

* Data Preprocessing (preprocess.py):
    •	This script handles all the functions for preparation and cleaning of raw data.
    •	The goal is to ensure the data is consistent, clean, and ready for analysis.
* Modeling (modeling.py):
    •	This script focuses on data analysis and modeling tasks.
    •	It includes tools for time series analysis, such as seasonal-trend decomposition, to extract insights from temporal data.
    •	It prepares the processed data for visualizations and further analysis.
* Visualization (visualize.py):
    •	This script provides customized visualizations for exploring and presenting data.
    •	It includes reusable functions like boxplots to compare and analyze categorical vs numerical relationships.
* Final Integration (ds_1007_notebook_q3.ipynb):
    •	This jupyter notebook answers the 5 topic questions for our project, importing the necessary functions from the previous script files.
