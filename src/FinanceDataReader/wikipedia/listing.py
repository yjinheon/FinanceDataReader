import pandas as pd
import requests
from io import StringIO

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

class WikipediaStockListing:
    def __init__(self, market):
        self.market = market

    def read(self):
        url ="https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        try:
           response = requests.get(url, headers=headers)
           response.raise_for_status()  

           df_list = pd.read_html(StringIO(response.text), match="Symbol", header=0)

           if not df_list:
                print("페이지에서 'Symbol'을 포함한 테이블을 찾을 수 없습니다.")
           else:
                df = df_list[0]
                cols_ren = {
                "Security": "Name",
                "Ticker symbol": "Symbol",
                "GICS Sector": "Sector",
                "GICS Sub-Industry": "Industry",
                }
                df = df.rename(columns=cols_ren)
                df = df[["Symbol", "Name", "Sector", "Industry"]]
                df["Symbol"] = df["Symbol"].str.replace(".", "", regex=False)
 
                print("데이터를 성공적으로 불러왔습니다.")
                #print(df.head()) 
                #print(len(df))

                return df

        except Exception as e:
            print(f"HTTP 요청 중 에러 발생: {e}")
        except IndexError:
            print("리스트에서 테이블을 찾는 데 실패했습니다. (IndexError)")
        except Exception as e:
 



