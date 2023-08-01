import pandas as pd
import matplotlib.pyplot as plt

def drop_c(df, columns):
    df=df.copy()
    for c in columns:
        if c in df.columns:
            df.drop(c,inplace=True,axis=1)
    return df
def quick_analysis(df):
    print("Row:{:>6},Col:{:>6}".format(df.shape[0], df.shape[1]))
    for c in df.columns:
        print("============================")
        print("Col:" + c)
        vc = df.loc[:, c].value_counts()
        print(vc)

def draw_column_count(columns):
    counts=columns.value_counts()
    counts.plot()