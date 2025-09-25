import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

PERIOD = '4mo'

def data_retriever(Ticker:str, period_val:str):

    data = yf.Ticker(Ticker)
    history = data.history(period=period_val)    
    history.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)

    return history

def get_correlations(data:str):
    df = pd.read_csv(data)

    numeric_data = df.select_dtypes(include=['number'])
    spearman_corr_matrix = numeric_data.corr(method='pearson')

    fig, ax = plt.subplots(figsize=(12, 12))
    cax = ax.matshow(spearman_corr_matrix, cmap='coolwarm')

    # Add colorbar
    fig.colorbar(cax)

    # Set ticks
    ax.set_xticks(range(len(spearman_corr_matrix.columns)))
    ax.set_yticks(range(len(spearman_corr_matrix.columns)))
    ax.set_xticklabels(spearman_corr_matrix.columns, rotation=90)
    ax.set_yticklabels(spearman_corr_matrix.columns)

    # Loop over data dimensions and create text annotations
    for (i, j), val in np.ndenumerate(spearman_corr_matrix):
        ax.text(j, i, f"{val:.2f}", va='center', ha='center', fontsize=8)

    plt.show()



def label(data: str):
    import pandas as pd

    repos = pd.read_csv(data)

    repos["label"] = 0

    for i, ticker in enumerate(repos["ticker"]):
        df = data_retriever(ticker, PERIOD)

        difference = df.iloc[-1]["Close"] - df.iloc[0]["Close"]

        tag = 1 if difference > 0 else 0

        repos.loc[i, "label"] = tag

    repos.to_csv(data, index=False)

label('github_org_stats.csv')





