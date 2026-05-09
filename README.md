<img width="1918" height="971" alt="Screenshot 2026-05-09 195917" src="https://github.com/user-attachments/assets/bc74843c-0413-4dd4-a04c-8d91294229f8" />\# AI Behavioral Finance Intelligence Platform



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


### Global Markets Tracker
- Tracks global stocks and indices using live market data
- Supports US stocks, Indian stocks, and major indices
- Shows latest price, 6-month return, volatility, and price trend

### Investment Behavior Engine
- Analyzes how much users invest compared to spending
- Calculates investment rate, average investment, and investing users
- Compares investment discipline across behavioral segments
- Flags low investment allocation risk



\## Business Insights

\- Electronics shows high spending due to high transaction value.

\- Credit Card and BNPL users show higher impulse purchase behavior.

\- Late-night transactions have higher impulse purchase probability.

\- High-risk users show elevated financial stress and impulse behavior.

\- Anomaly detection identifies unusual high-value risky transactions.

## Live Demo

Deployed App: <https://behavioral-finance-ai-platform-ama92keuw5bogg66hy3xeu.streamlit.app/>

## Screenshots


### Executive Overview

<img width="1918" height="971" alt="Screenshot 2026-05-09 195917" src="https://github.com/user-attachments/assets/988e1ea6-4a3a-46b7-ad5a-46122f339cb0" />


### Global Markets Tracker
<img width="1917" height="967" alt="image" src="https://github.com/user-attachments/assets/f0d271df-7f31-4452-9952-83de64e145e3" />


### Investment Behavior Engine
<img width="1912" height="971" alt="image" src="https://github.com/user-attachments/assets/5c56c47b-812c-4bb7-b208-e6ce936c99fc" />


### Financial Advisor Chatbot
<img width="1917" height="966" alt="image" src="https://github.com/user-attachments/assets/da2abef2-57cc-439c-b764-ca0e7012f1c5" />




\## Project Architecture

```text

data/raw                 -> raw synthetic datasets

data/processed           -> processed ML outputs

notebooks                -> EDA and ML experiments

src                      -> data generation and SQL loading scripts

dashboard                -> Streamlit dashboard

models                   -> saved ML models

database                 -> SQL schema

