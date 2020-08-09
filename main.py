import yfinance as yf
from datetime import datetime
import time
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse


def ReadCurrentProfile(input_path):
    if (len(input_path) == 0):
        input_path = "~/stock.xlsx"
    input_data = pd.read_excel(input_path, index_col=0)
    d = {'number': input_data['number'], 'unit_cost': input_data['unit_cost']}
    df = pd.DataFrame(data=d)
    return df;

def ReadLastestInfo(input_path):
    df = ReadCurrentProfile(input_path)
    latest_price = []
    for code in df.index:
        cur_company = yf.Ticker(code)
        hist = cur_company.history(period = "1d")
        latest_price.append(hist['Close'][-1])
    df['latest_price'] = latest_price
    return df

def GetSummaryDf(input_path):
    df = ReadLastestInfo(input_path);
    df['cost'] = df['unit_cost']*df['number']
    df['value'] = df['latest_price'] * df['number']
    df['revenue'] = df['value'] - df['cost']
    return df

def get_current_timestamp():
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S");

def output_to_csv(df, output_path):
    if (len(output_path) == 0):
        output_path = "~/my_stock"
    file_name = output_path + "/summary_" + get_current_timestamp() + ".csv"
    df.to_csv(file_name, index=True)

def draw_pie(df, type):
    sizes = list(df[type])
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.pie(sizes, labels=df.index, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


def generate_report(input_path, output_path, is_export):
    df = GetSummaryDf(input_path)
    print("Total Value: ", sum(df['value']))
    print("Total Cost: ", sum(df['cost']))
    print("Total Revenue: ", sum(df['revenue']))
    if is_export:
        output_to_csv(df, output_path)
    draw_pie(df, 'cost')
    draw_pie(df, 'value')
    plt.show()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate personal stock report.')
    parser.add_argument("-ip", '--input_path', type=str, default="~/stock.xlsx",
                        help='Input path with personal purchase info.')
    parser.add_argument("-op", '--output_path', type=str, default="~/my_stock",
                        help='Output path for the generated summary.')
    parser.add_argument("-e", '--export', type=bool, default=True,
                        help='Determine if export the generated summary.')
    args = parser.parse_args()
    generate_report(args.input_path, args.output_path, args.export)
