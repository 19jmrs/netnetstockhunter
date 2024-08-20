import yfinance as yf
import pandas as pd

print("Starting...\n")

filename = "netnetstocks.txt"

#read excel file with tickers
tickerSheet = pd.read_excel('tickersSmall.xlsx')
#create list with all the ticker
tickerList = tickerSheet.iloc[:,0].tolist()
#list to store result
value = []
#counter of iteration just for debugging
counter = 0
#iterate through each ticker
for ticker in tickerList:
    #get the YF data
    ticker_object = yf.Ticker(ticker) 

    
    balancesheet = ticker_object.balance_sheet

    if not(balancesheet.empty):
        marketcap = ticker_object.info.get('marketCap')

        #get the most recent data column header
        end = balancesheet.columns.max()

        balancesheet_df = pd.DataFrame(balancesheet)
        #select all the value for the most recent header 
        ttmbalancesheet= balancesheet_df[end]

        if("Current Assets" in ttmbalancesheet):
            selected_data = ttmbalancesheet.loc[['Current Assets', 'Total Liabilities Net Minority Interest']]

            ncav = selected_data.get('Current Assets') - selected_data.get('Total Liabilities Net Minority Interest')
            if marketcap != None:
                if ((float(marketcap)/ncav) <= 0.66 and (float(marketcap)/ncav) > 0):
                    value.append(ticker)
                    print(value)
    counter += 1
print("/n counter: " + str(counter))    
with open(filename, 'w') as file:
    for item in value:
        file.write(str(item) + '\n')

print("Finished!")


