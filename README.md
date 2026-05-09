\# AI Behavioral Finance Intelligence Platform



\## Project Overview

This project analyzes user transaction behavior to detect impulse spending, financial stress, marketing-triggered purchases, user risk segments, and anomalous transactions.



It combines:

\- Finance analytics

\- Behavioral finance

\- Marketing psychology

\- SQL database

\- Machine learning

\- Streamlit dashboard



\## Key Features

\- Transaction-level spending analysis

\- Behavioral finance indicators

\- User segmentation using K-Means clustering

\- Financial risk prediction using Logistic Regression

\- Anomaly detection using Isolation Forest

\- SQL Server database integration

\- Interactive Streamlit dashboard

\- Rule-based AI recommendation engine



\## Tech Stack

\- Python

\- Pandas

\- Scikit-learn

\- SQL Server

\- SSMS

\- SQLAlchemy

\- PyODBC

\- Streamlit

\- Matplotlib



\## Dataset

Synthetic finance transaction dataset containing:

\- 500 users

\- 10,000 transactions

\- spending categories

\- payment methods

\- marketing triggers

\- mood score

\- impulse purchase flag

\- financial stress level



\## ML Models Used



\### 1. User Segmentation

Model: K-Means Clustering  

Purpose: Segment users into behavioral groups.



Segments:

\- Stable Saver

\- Emotional Spender

\- Offer Hunter

\- High Risk User



\### 2. Financial Risk Prediction

Model: Logistic Regression  

Purpose: Predict whether a user is financially high-risk.



\### 3. Anomaly Detection

Model: Isolation Forest  

Purpose: Detect unusual or suspicious transaction behavior.



\## Business Insights

\- Electronics shows high spending due to high transaction value.

\- Credit Card and BNPL users show higher impulse purchase behavior.

\- Late-night transactions have higher impulse purchase probability.

\- High-risk users show elevated financial stress and impulse behavior.

\- Anomaly detection identifies unusual high-value risky transactions.



\## Project Architecture

```text

data/raw                 -> raw synthetic datasets

data/processed           -> processed ML outputs

notebooks                -> EDA and ML experiments

src                      -> data generation and SQL loading scripts

dashboard                -> Streamlit dashboard

models                   -> saved ML models

database                 -> SQL schema

