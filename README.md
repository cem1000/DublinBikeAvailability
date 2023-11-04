# Dublin Bikes Availability Analysis

This repository contains a detailed analysis of Dublin Bikes data to understand usage patterns and availability across different stations and districts within Dublin. The project is structured into three main components: data retrieval, explorative analysis, and an interactive Streamlit application.

## Repository Structure

- `ExplorativeAnalysis.ipynb`: This Jupyter notebook file holds all the exploratory data analysis, visualizations, and statistical inferences. It serves as the core of the analysis, where patterns are identified, and hypotheses are tested to derive insights about bike station activity.

- `DublinBikeDataPull.py`: This Python script is designed as a workflow to automatically fetch the last 14 days of bike data. The data pulled by this script is used to feed into the Streamlit app, ensuring the app has the latest information to provide accurate availability forecasts.

- `app.py`: The Streamlit app code is contained within this file. It utilizes the data obtained from `DublinBikeDataPull.py` to present an interactive web application that predicts bike availability over a day and 30-minute intervals based on historical usage data.

## Streamlit Application

The Streamlit app is a user-friendly interface that allows users to quickly gauge the expected bike availability at different stations. It is designed for both planners looking to optimize the bike-sharing network and users planning their commutes. The app updates daily with fresh data to ensure accurate predictions.

Check out the app here: [Dublin Bikes Streamlit App](https://dublinbikes.streamlit.app/)

## Getting Started

To run the analysis or app on your local machine, clone the repository and install the necessary dependencies as listed in the `requirements.txt` file.

## Contributions + Usage

Feel free to fork the project! :) 
