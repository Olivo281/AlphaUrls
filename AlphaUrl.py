import requests
import csv 
import os 
import io 

class Alpha_url:
    def __init__(self,api_key=None):
        self.api_key = api_key or os.getenv("ALPHA_API_KEY")
        self.base_url = 'https://www.alphavantage.co/query?function='

    def get_intraday_data(self, ticker, interval, adjusted=True, extended_hours=True, month=None, outputsize='full', datatype='csv'):
        """ Get intraday data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_INTRADAY"
        
        params = {
            'symbol': ticker,
            'interval': interval,
            'apikey': self.api_key,
            'adjusted': 'true' if adjusted else 'false',
            'extended_hours': 'true' if extended_hours else 'false',
            'outputsize': outputsize,
            'datatype': datatype
        }
        
        if month:
            params['month'] = month

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def get_daily_data(self, ticker, outputsize='full', datatype='csv'):
        """ Get daily data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_DAILY"
        
        params = {
            'symbol': ticker,
            'apikey': self.api_key,
            'outputsize': outputsize,
            'datatype': datatype
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def get_daily_adjusted_data(self, ticker, outputsize='full', datatype='csv'):
        """ Get daily adjusted data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_DAILY_ADJUSTED"
        
        params = {
            'symbol': ticker,
            'apikey': self.api_key,
            'outputsize': outputsize,
            'datatype': datatype
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def get_weekly_data(self, ticker, datatype='csv'):
        """ Get weekly data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_WEEKLY"
        
        params = {
            'symbol': ticker,
            'apikey': self.api_key,
            'datatype': datatype
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def get_weekly_adjusted_data(self, ticker, datatype='csv'):
        """ Get weekly adjusted data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_WEEKLY_ADJUSTED"
        
        params = {
            'symbol': ticker,
            'apikey': self.api_key,
            'datatype': datatype
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def get_monthly_data(self, ticker, datatype='csv'):
        """ Get monthly data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_MONTHLY"
        
        params = {
            'symbol': ticker,
            'apikey': self.api_key,
            'datatype': datatype
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def get_monthly_adjusted_data(self, ticker, datatype='csv'):
        """ Get monthly adjusted data for a given ticker """
        url = f"{self.base_url}?function=TIME_SERIES_MONTHLY_ADJUSTED"
        
        params = {
            'symbol': ticker,
            'apikey': self.api_key,
            'datatype': datatype
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            if datatype == 'csv':
                return response.text  # Return the CSV data as text
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code} - {response.text}")

    def realtime_bulk_quotes(self,tickers):
        """ live price for multiple tickers """
        if isinstance(tickers, str):
                    tickers = [tickers]

        # Validate input
        if not tickers or not isinstance(tickers, list):
            raise ValueError("Tickers must be a non-empty string or list of strings.")

        # Ensure no more than 100 tickers are used
        tickers_str = ",".join(tickers[:100])

        # Construct the URL
        url = f"{self.base_url}REALTIME_BULK_QUOTES&symbol={tickers_str}&apikey={self.api_key}"

        try:
            # Make the request
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Check for valid data in the response
            if not data or "error" in data:
                raise ValueError(f"Invalid response: {data}")

            return data

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to fetch data: {e}")
        

    def search_endpoint(self,datatype='&datatype=csv'):
        """ search query for identifying tickers"""
        url = f'{self.base_url}SYMBOL_SEARCH&keywords=tesco&apikey={self.api_key}{datatype}'
        r = requests.get(url)
        r.raise_for_status()
        if datatype == '&datatype=csv':
            # Process CSV data
            csv_data = r.text  # Get the raw text of the CSV response
            reader = csv.DictReader(io.StringIO(csv_data))  # Parse the CSV data
            
            # Convert to a list of dictionaries (optional, for easier handling)
            data = [row for row in reader]
        else:
            # Process JSON data
            data = r.json()
        
        print(data)
        return data

    def global_market_open_and_close_status(self):
        url = f'{self.base_url}MARKET_STATUS&apikey={self.api_key}{self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def realtime_options(self,ticker,datatype='&datatype=csv'):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}REALTIME_OPTIONS{ticker}&apikey={self.api_key}{datatype}'
        r = requests.get(url)
        r.raise_for_status()
        if datatype == '&datatype=csv':
            # Process CSV data
            csv_data = r.text  # Get the raw text of the CSV response
            reader = csv.DictReader(io.StringIO(csv_data))  # Parse the CSV data
            
            # Convert to a list of dictionaries (optional, for easier handling)
            data = [row for row in reader]
        else:
            # Process JSON data
            data = r.json()
        
        print(data)
        return data
    
    def historical_options(self,ticker,datatype='&datatype=csv',date=None):
        """ Any date later than 2008-01-01 is accepted. For example, date=2017-11-15 """
        ticker = f'&symbol={ticker}'
        if date:
            url.append(f'&date={date}')
        
        url = f'{self.base_url}HISTORICAL_OPTIONS{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        r.raise_for_status()
        if datatype == '&datatype=csv':
            # Process CSV data
            csv_data = r.text  # Get the raw text of the CSV response
            reader = csv.DictReader(io.StringIO(csv_data))  # Parse the CSV data
            
            # Convert to a list of dictionaries (optional, for easier handling)
            data = [row for row in reader]
        else:
            # Process JSON data
            data = r.json()
        
        print(data)
        return data

    def market_news_and_sentiment(self,topics=None, time_from = None , time_to = None, sort='&sort=LATEST',limit=None):
        """ ex: time_from = 20220410T0130

        sort= EARLIEST or RELEVANCE

        topics = 
        Blockchain: blockchain
        Earnings: earnings
        IPO: ipo
        Mergers & Acquisitions: mergers_and_acquisitions
        Financial Markets: financial_markets
        Economy - Fiscal Policy (e.g., tax reform, government spending): economy_fiscal
        Economy - Monetary Policy (e.g., interest rates, inflation): economy_monetary
        Economy - Macro/Overall: economy_macro
        Energy & Transportation: energy_transportation
        Finance: finance
        Life Sciences: life_sciences
        Manufacturing: manufacturing
        Real Estate & Construction: real_estate
        Retail & Wholesale: retail_wholesale
        Technology: technology
        """
        url = f'{self.base_url}NEWS_SENTIMENT&tickers=AAPL&apikey={self.api_key}'

        if topics:
            url += f'&topics={topics}'
        if time_from:
            url += f'&time_from={time_from}'
        if time_to:
            url += f'&time_to={time_to}'
        if 0 < limit < 1000:
            url += f'&limit={limit}'
        if sort:
            url += sort

        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        print(data)
        return data

    def top_gainers_losers_and_mostly_actively_traded_tickers_us(self):
        url = f'{self.base_url}TOP_GAINERS_LOSERS&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def insider_transactions(self,ticker):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}INSIDER_TRANSACTIONS{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def advanced_analytics_fixed_window(self,tickers,range1,range2,calculations,ohlc='&OHLC=close',interval='&INTERVAL=DAILY'):
        """ premium = 50 tickers per api request
        RANGE can take certain text values as inputs. They are:
        full
        {N}day
        {N}week
        {N}month
        {N}year
        
        For intraday time series, the following RANGE values are also accepted:
        {N}minute
        {N}hour

        ex: RANGE=2023-07-01&RANGE=2023-08-31 or RANGE=2020-12-01T00:04:00&RANGE=2020-12-06T23:59:59 

        ex OHLC= open / high / low / close

        ex: INTERVAL='{timeframe}min /// timeframes = [1,5,15,30,60] else DAILY , WEEKLY, MONTHLY

        CALCULATIONS=
        A comma separated list of the analytics metrics you would like to calculate:
        MIN: The minimum return (largest negative or smallest positive) for all values in the series
        MAX: The maximum return for all values in the series
        MEAN: The mean of all returns in the series
        MEDIAN: The median of all returns in the series
        CUMULATIVE_RETURN: The total return from the beginning to the end of the series range
        VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalized the output to an annual value. By default, the variance is not annualized.
        STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalized the output to an annual value. By default, the standard deviation is not annualized.
        MAX_DRAWDOWN: Largest peak to trough interval for each symbol in the series range
        HISTOGRAM: For each symbol, place the observed total returns in bins. By default, bins=10. Use HISTOGRAM(bins=20) to specify a custom bin value (e.g., 20).
        AUTOCORRELATION: For each symbol place, calculate the autocorrelation for the given lag (e.g., the lag in neighboring points for the autocorrelation calculation). By default, lag=1. Use AUTOCORRELATION(lag=2) to specify a custom lag value (e.g., 2).
        COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalized the output to an annual value. By default, the covariance is not annualized.
        CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.
        """
        tickers = f'&SYMBOLS={tickers}'
        calculations = f'&CALCULATIONS={calculations}'
        range1= f'&RANGE={range1}'
        range2= f'&RANGE={range2}'

        url = f'https://alphavantageapi.co/timeseries/analytics?{tickers}{range1}{range2}{interval}{ohlc}{calculations}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def advanced_analytics_sliding_window(self,tickers,range1,range2,calculations,ohlc='&OHLC=close',interval='&INTERVAL=DAILY', window_size= '&WINDOW_SIZE=20'):
        """ same as def advanced_analytics_fixed_window 
        except
        CALCULATIONS   
        MEAN: The mean of all returns in the series
        MEDIAN: The median of all returns in the series
        CUMULATIVE_RETURN: The total return from the beginning to the end of the series range
        VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalized the output to an annual value. By default, the variance is not annualized.
        STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalized the output to an annual value. By default, the standard deviation is not annualized.
        COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalized the output to an annual value. By default, the covariance is not annualized.
        CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.
        """
        tickers = f'&SYMBOLS={tickers}'
        calculations = f'&CALCULATIONS={calculations}'
        range1= f'&RANGE={range1}'
        range2= f'&RANGE={range2}'

        url = f'https://alphavantageapi.co/timeseries/running_analytics?{tickers}{range1}{range2}{interval}{ohlc}{calculations}{window_size}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def company_overview(self,ticker):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}OVERVIEW{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def etf_profile_and_holdings(self,ticker):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}ETF_PROFILE&{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def corporate_action_dividends(self,ticker):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}DIVIDENDS{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def corporate_action_splits(self,ticker):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}SPLITS{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def income_statement(self):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}INCOME_STATEMENT{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def balance_sheet(self):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}BALANCE_SHEET{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def cash_flow(self):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}CASH_FLOW{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def earnings(self):
        ticker = f'&symbol={ticker}'
        url = f'{self.base_url}EARNINGS{ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def listing_and_delisting_status(self,date=None,state=None):
        """
        list of active or delisted symbols on that particular date in history. Any YYYY-MM-DD date later than 2010-01-01 is supported. For example, date=2013-08-03
        By default, state=active and the API will return a list of actively traded stocks and ETFs. Set state=delisted
        """
        CSV_URL = f'{self.base_url}LISTING_STATUS&apikey={self.api_key}'
        if date:
            CSV_URL +=f'&date={date}'
        if state:
            CSV_URL +=f'&state={state}'
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                print(row)

    def earnings_calendar(self,horizon='&horizion=3month',symbol=None):
        """
        horizon=3month and the API will return a list of expected company earnings in the next 3 months. You may set horizon=6month or horizon=12month to query the earnings scheduled for the next 6 months or 12 months, respectively.
        if symbol only for specific symbol
        """
        CSV_URL = f'{self.base_url}EARNINGS_CALENDAR&{horizon}&apikey={self.api_key}'
        if symbol:
            CSV_URL += f'&symbol={symbol}'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                print(row)

    def ipo_calendar(self):
        CSV_URL = f'{self.base_url}IPO_CALENDAR&apikey={self.api_key}'

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            for row in my_list:
                print(row)

### FOREX
    def currency_exchange_rate(self,from_currency,to_currency,):
        """ ex: from_currency=USD
                to_currency=BTC
        """
        url = f'{self.base_url}CURRENCY_EXCHANGE_RATE&{from_currency}&{to_currency}=JPY&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()

        print(data)

    def fx_intraday(self, from_symbol, to_symbol, interval, output_size='full', datatype='csv'):
        """
        Get intraday forex data for a specific currency pair.

        Parameters:
            from_symbol (str): The base currency (e.g., 'USD').
            to_symbol (str): The target currency (e.g., 'EUR').
            interval (str): The time interval for the data (e.g., '1min', '5min', etc.).
            output_size (str): 'compact' for the last 100 data points, 'full' for the entire available dataset. Default is 'compact'.
            datatype (str): The output format, default is 'json'. Can also be 'csv'.

        Returns:
            dict or str: The response data from the API in the requested format.
        """
        url = f'{self.base_url}FX_INTRADAY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={self.api_key}'

        if output_size:
            url += f'&outputsize={output_size}' 
        if datatype:
            url += f'&datatype={datatype}' 

        try:
            r = requests.get(url)
            r.raise_for_status() 
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text  
        else:
            return r.json() 
        
    def fx_daily(self, from_symbol='EUR', to_symbol='USD', datatype='&datatype=csv'):
        """
        Get daily forex data for a specific currency pair.
        
        Parameters:
            from_symbol (str): The base currency (e.g., 'EUR').
            to_symbol (str): The target currency (e.g., 'USD').
            datatype (str): The output format, default is 'csv'. Can also be 'json'.
        
        Returns:
            dict: The response data from the API in the requested format.
        """
        # Construct the base URL for the FX Daily API
        url = f'{self.base_url}FX_DAILY&from_symbol={from_symbol}&to_symbol={to_symbol}&apikey={self.api_key}'

        if datatype:
            url += f'{datatype}'

        # Send the request
        r = requests.get(url)
        r.raise_for_status()  

        if datatype == '&datatype=csv':
            return r.text  
        else:
            data = r.json()  
            return data


    def fx_weekly(self, from_symbol='EUR', to_symbol='USD', datatype='&datatype=csv'):
        """
        Get weekly forex data for a specific currency pair.
        
        Parameters:
            from_symbol (str): The base currency (e.g., 'EUR').
            to_symbol (str): The target currency (e.g., 'USD').
            datatype (str): The output format, default is 'csv'. Can also be 'json'.
        
        Returns:
            dict: The response data from the API in the requested format.
        """

        url = f'{self.base_url}FX_WEEKLY&from_symbol={from_symbol}&to_symbol={to_symbol}&apikey={self.api_key}'

        if datatype:
            url += f'{datatype}'

        r = requests.get(url)
        r.raise_for_status()  

        if datatype == '&datatype=csv':
            return r.text
        else:
            data = r.json() 
            return data


    def fx_monthly(self, from_symbol='EUR', to_symbol='USD', datatype='&datatype=csv'):
        """
        Get monthly forex data for a specific currency pair.
        
        Parameters:
            from_symbol (str): The base currency (e.g., 'EUR').
            to_symbol (str): The target currency (e.g., 'USD').
            datatype (str): The output format, default is 'csv'. Can also be 'json'.
        
        Returns:
            dict: The response data from the API in the requested format.
        """

        url = f'{self.base_url}FX_MONTHLY&from_symbol={from_symbol}&to_symbol={to_symbol}&apikey={self.api_key}'

        if datatype:
            url += f'{datatype}'

        r = requests.get(url)
        r.raise_for_status() 

 
        if datatype == '&datatype=csv':
            return r.text  
        else:
            data = r.json() 
            return data

    def currency_exchange_rate(self, from_currency='BTC', to_currency='EUR'):
        """
        Get the exchange rate between two currencies.

        Parameters:
            from_currency (str): The source currency (e.g., 'BTC', 'USD').
            to_currency (str): The destination currency (e.g., 'EUR', 'USD').

        Returns:
            dict: The response data from the API in JSON format.
        """
       
        url = f'{self.base_url}CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={self.api_key}'

        # Send the request
        r = requests.get(url)
        r.raise_for_status()  

   
        data = r.json()

        return data

    def crypto_intraday(self, symbol='ETH', market='USD', interval='5min', outputsize='full', datatype='&datatype=csv'):
        """
        Get the intraday time series data for a specific cryptocurrency.

        Parameters:
            symbol (str): The cryptocurrency symbol (e.g., 'ETH', 'BTC').
            market (str): The market for the cryptocurrency (e.g., 'USD', 'EUR').
            interval (str): The time interval between data points (e.g., '1min', '5min').
            outputsize (str): 'compact' or 'full'. Default is 'compact'.
            datatype (str): The format for the response, 'json' or 'csv'. Default is 'json'.

        Returns:
            dict: The response data from the API in the requested format (JSON or CSV).
        """
        url = f'{self.base_url}CRYPTO_INTRADAY&symbol={symbol}&market={market}&interval={interval}&apikey={self.api_key}&outputsize={outputsize}{datatype}'


        r = requests.get(url)
        r.raise_for_status()  
        if datatype == '&datatype=csv':
            return r.text  
        else:
            data = r.json() 
            return data


    def digital_currency_daily(self, symbol='BTC', market='EUR', output_size='full', datatype='csv'):
        """
        Fetches the daily digital currency data for the given symbol and market.

        Parameters:
            symbol (str): The digital currency symbol (default is 'BTC').
            market (str): The market in which the currency is traded (default is 'EUR').
            output_size (str): The size of the output data ('full' or 'compact', default is 'full').
            datatype (str): The format of the returned data ('csv' or 'json', default is 'csv').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}DIGITAL_CURRENCY_DAILY&symbol={symbol}&market={market}&apikey={self.api_key}'

        if output_size:
            url += f'&outputsize={output_size}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()


    def digital_currency_weekly(self, symbol='BTC', market='EUR', output_size='full', datatype='csv'):
        """
        Fetches the weekly digital currency data for the given symbol and market.

        Parameters:
            symbol (str): The digital currency symbol (default is 'BTC').
            market (str): The market in which the currency is traded (default is 'EUR').
            output_size (str): The size of the output data ('full' or 'compact', default is 'full').
            datatype (str): The format of the returned data ('csv' or 'json', default is 'csv').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}DIGITAL_CURRENCY_WEEKLY&symbol={symbol}&market={market}&apikey={self.api_key}'

        if output_size:
            url += f'&outputsize={output_size}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def digital_currency_monthly(self, symbol='BTC', market='EUR', output_size='full', datatype='csv'):
        """
        Fetches the monthly digital currency data for the given symbol and market.

        Parameters:
            symbol (str): The digital currency symbol (default is 'BTC').
            market (str): The market in which the currency is traded (default is 'EUR').
            output_size (str): The size of the output data ('full' or 'compact', default is 'full').
            datatype (str): The format of the returned data ('csv' or 'json', default is 'csv').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}DIGITAL_CURRENCY_MONTHLY&symbol={symbol}&market={market}&apikey={self.api_key}'

        if output_size:
            url += f'&outputsize={output_size}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def crude_oil_prices_wti(self, interval='monthly', datatype='csv'):
        """
        Fetches the WTI crude oil prices with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'daily', 'weekly', or 'monthly'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}WTI&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()


    def crude_oil_prices_brent(self, interval='monthly', datatype='csv'):
        """
        Fetches the Brent crude oil prices with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'daily', 'weekly', or 'monthly'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}BRENT&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def natural_gas(self, interval='monthly', datatype='csv'):
        """
        Fetches the natural gas prices.

        Parameters:
            interval (str): The frequency of the data (default is 'monthly'). 
                             Other options: 'daily', 'weekly', 'monthly'.
            datatype (str): The format of the data (default is 'json'). 
                             Options: 'json' returns data in JSON format, 
                                      'csv' returns data in CSV format.

        Returns:
            dict or str: JSON data (if datatype is json) or raw CSV data (if datatype is csv).
        """
        url = f'{self.base_url}NATURAL_GAS&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_copper(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of copper with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}COPPER&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_aluminum(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of aluminum with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}ALUMINUM&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_wheat(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of wheat with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}WHEAT&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_corn(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of corn with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}CORN&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_cotton(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of cotton with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}COTTON&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_sugar(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of sugar with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}SUGAR&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_of_coffee(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price of coffee with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}COFFEE&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def global_price_index_of_all_commodities(self, interval='monthly', datatype='csv'):
        """
        Fetches the global price index of all commodities with a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'monthly').
                            Options: 'monthly', 'quarterly', or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}ALL_COMMODITIES&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def real_gdp(self, interval='annual', datatype='csv'):
        """
        Fetches the Real GDP data for a specified interval.

        Parameters:
            interval (str): The time interval for the data (default is 'annual').
                            Options: 'quarterly' or 'annual'.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}REAL_GDP&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()
        
    def real_gdp_per_capita(self, datatype='csv'):
        """
        Fetches the Real GDP Per Capita data.

        Parameters:
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}REAL_GDP_PER_CAPITA&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def treasury_yield(self, interval='monthly', maturity='10year', datatype='csv'):
        """
        Fetches the Treasury Yield data.

        Parameters:
            interval (str): The time interval for the data ('daily', 'weekly', or 'monthly', default is 'monthly').
            maturity (str): The maturity of the bond ('3month', '2year', '5year', '7year', '10year', '30year', default is '10year').
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}TREASURY_YIELD&interval={interval}&maturity={maturity}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def federal_funds_rate(self, interval='monthly', datatype='csv'):
        """
        Fetches the Federal Funds Rate data.

        Parameters:
            interval (str): The time interval for the data ('daily', 'weekly', or 'monthly', default is 'monthly').
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}FEDERAL_FUNDS_RATE&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def cpi(self, interval='monthly', datatype='csv'):
        """
        Fetches the Consumer Price Index (CPI) data.

        Parameters:
            interval (str): The time interval for the data ('monthly' or 'semiannual', default is 'monthly').
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}CPI&interval={interval}&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def inflation(self, datatype='csv'):
        """
        Fetches the Inflation data.

        Parameters:
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}INFLATION&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def retail_sales(self, datatype='csv'):
        """
        Fetches the Retail Sales data.

        Parameters:
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}RETAIL_SALES&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def durables(self, datatype='csv'):
        """
        Fetches the Durable Goods data.

        Parameters:
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}DURABLES&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def unemployment(self, datatype='csv'):
        """
        Fetches the Unemployment data.

        Parameters:
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}UNEMPLOYMENT&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def nonfarm_payroll(self, datatype='csv'):
        """
        Fetches the Nonfarm Payroll data.

        Parameters:
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}NONFARM_PAYROLL&apikey={self.api_key}'

        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def sma(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Simple Moving Average (SMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Possible values: 
                            '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly' (default is 'weekly').
            time_period (int): The number of data points used to calculate each moving average value (e.g., 10, 50, 200).
            series_type (str): The price type to use for calculating SMA. Options are 'close', 'open', 'high', 'low' (default is 'open').
            month (str, optional): Only used for intraday intervals ('1min', '5min', '15min', '30min', '60min') to specify the month in 
                                    'YYYY-MM' format (e.g., '2009-01'). Not applicable for daily, weekly, or monthly intervals.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').
            apikey (str): Your API key for authenticating the request.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}SMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def ema(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Exponential Moving Average (EMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Possible values:
                            '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly' (default is 'weekly').
            time_period (int): The number of data points used to calculate each EMA value (e.g., 10, 50, 200).
            series_type (str): The price type to use for calculating EMA. Options are 'close', 'open', 'high', 'low' (default is 'open').
            month (str, optional): Only used for intraday intervals ('1min', '5min', '15min', '30min', '60min') to specify the month in 
                                    'YYYY-MM' format (e.g., '2009-01'). Not applicable for daily, weekly, or monthly intervals.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').
            apikey (str): Your API key for authenticating the request.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}EMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()
    def wma(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Weighted Moving Average (WMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Possible values:
                            '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly' (default is 'weekly').
            time_period (int): The number of data points used to calculate each WMA value (e.g., 10, 50, 200).
            series_type (str): The price type to use for calculating WMA. Options are 'close', 'open', 'high', 'low' (default is 'open').
            month (str, optional): Only used for intraday intervals ('1min', '5min', '15min', '30min', '60min') to specify the month in 
                                    'YYYY-MM' format (e.g., '2009-01'). Not applicable for daily, weekly, or monthly intervals.
            datatype (str): The format of the returned data ('json' or 'csv', default is 'json').
            apikey (str): Your API key for authenticating the request.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}WMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def dema(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Double Exponential Moving Average (DEMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. 
                            Options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'weekly'.
            time_period (int): The number of data points used to calculate each DEMA value (e.g., 10, 50, 200).
            series_type (str): The price type to use for calculating DEMA. Options: 'close', 'open', 'high', 'low'.
                               Default is 'open'.
            month (str, optional): For intraday intervals only ('1min', '5min', '15min', '30min', '60min').
                                    Specify the month in 'YYYY-MM' format (e.g., '2009-01').
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}DEMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()
        
    def tema(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Triple Exponential Moving Average (TEMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. 
                            Options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'weekly'.
            time_period (int): The number of data points used to calculate each TEMA value (e.g., 10, 50, 200).
            series_type (str): The price type to use for calculating TEMA. Options: 'close', 'open', 'high', 'low'.
                               Default is 'open'.
            month (str, optional): For intraday intervals only ('1min', '5min', '15min', '30min', '60min').
                                    Specify the month in 'YYYY-MM' format (e.g., '2009-01').
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}TEMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def trima(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Triple Exponential Moving Average (TRIMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'weekly'.
            time_period (int): The number of data points used to calculate each TRIMA value.
            series_type (str): The price type to use for calculating TRIMA. Options: 'close', 'open', 'high', 'low'.
                               Default is 'open'.
            month (str, optional): For intraday intervals only. Specify the month in 'YYYY-MM' format.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}TRIMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def kama(self, ticker, interval='weekly', time_period=10, series_type='open', month=None, datatype='csv'):
        """
        Fetches the Kaufman's Adaptive Moving Average (KAMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'weekly'.
            time_period (int): The number of data points used to calculate each KAMA value.
            series_type (str): The price type to use for calculating KAMA. Options: 'close', 'open', 'high', 'low'.
                               Default is 'open'.
            month (str, optional): For intraday intervals only. Specify the month in 'YYYY-MM' format.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}KAMA&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def mama(self, ticker, interval='daily', series_type='close', fastlimit=0.02, slowlimit=0.02, month=None, datatype='csv'):
        """
        Fetches the MESA Adaptive Moving Average (MAMA) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'daily'.
            series_type (str): The price type to use for calculating MAMA. Options: 'close', 'open', 'high', 'low'.
                               Default is 'close'.
            fastlimit (float, optional): Positive float for the fast limit. Default is 0.02.
            slowlimit (float, optional): Positive float for the slow limit. Default is 0.02.
            month (str, optional): For intraday intervals only. Specify the month in 'YYYY-MM' format.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        url = f'{self.base_url}MAMA&symbol={ticker}&interval={interval}&series_type={series_type}&fastlimit={fastlimit}&slowlimit={slowlimit}&apikey={self.api_key}'

        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def vwap(self, ticker, interval='15min', month=None, datatype='csv'):
        """
        Fetches the Volume Weighted Average Price (VWAP) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Supported options: '1min', '5min', '15min', '30min', '60min'.
                            Default is '15min'.
            month (str, optional): For intraday intervals only. Specify the month in 'YYYY-MM' format.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}VWAP&symbol={ticker}&interval={interval}&apikey={self.api_key}'

        # If month parameter is provided, add it to the URL
        if month:
            url += f'&month={month}'

        # If datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format
        if datatype == 'csv':
            return r.text
        else:
            return r.json()
        
    def t3(self, ticker, interval='weekly', time_period=10, series_type='close', month=None, datatype='csv'):
        """
        Fetches the T3 (Triple Exponential Moving Average) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Supported options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'weekly'.
            time_period (int): Number of data points used to calculate each moving average value.
                               (e.g., 60 or 200). Default is 10.
            series_type (str): The price type used for the calculation. Supported options: 'close', 'open', 'high', 'low'.
                               Default is 'close'.
            month (str, optional): For intraday intervals only. Specify the month in 'YYYY-MM' format.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}T3&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If month parameter is provided, add it to the URL
        if month:
            url += f'&month={month}'

        # If datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def macd(self, ticker, interval='daily', series_type='close', fastperiod=12, slowperiod=26, signalperiod=9, month=None, datatype='csv'):
        """
        Fetches the MACD (Moving Average Convergence Divergence) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Supported options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'daily'.
            series_type (str): The price type used for the calculation. Supported options: 'close', 'open', 'high', 'low'.
                               Default is 'close'.
            fastperiod (int): The number of periods used for the fast moving average. Default is 12.
            slowperiod (int): The number of periods used for the slow moving average. Default is 26.
            signalperiod (int): The number of periods used for the signal line. Default is 9.
            month (str, optional): For intraday intervals only. Specify the month in 'YYYY-MM' format.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: JSON data if datatype is 'json', or raw CSV data if datatype is 'csv'.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}MACD&symbol={ticker}&interval={interval}&series_type={series_type}&fastperiod={fastperiod}&slowperiod={slowperiod}&signalperiod={signalperiod}&apikey={self.api_key}'

        # If month parameter is provided, add it to the URL
        if month:
            url += f'&month={month}'

        # If datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def macdext(self, ticker, interval='daily', series_type='close', fastperiod=12, slowperiod=26, signalperiod=9,
                fastmatype=0, slowmatype=0, signalmatype=0, month=None, datatype='csv', apikey=None):
        """
        Fetches the MACD (Extended) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points.
                            Supported options: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
                            Default is 'daily'.
            series_type (str): The price type used for the calculation. Options: 'close', 'open', 'high', 'low'.
                               Default is 'close'.
            fastperiod (int): The number of periods for the fast moving average. Default is 12.
            slowperiod (int): The number of periods for the slow moving average. Default is 26.
            signalperiod (int): The number of periods for the signal line. Default is 9.
            fastmatype (int): The type of moving average for the fast moving average. Default is 0 (SMA).
                              Other options: 1 (EMA), 2 (WMA), etc.
            slowmatype (int): The type of moving average for the slow moving average. Default is 0 (SMA).
            signalmatype (int): The type of moving average for the signal line. Default is 0 (SMA).
            month (str, optional): Specify the month in 'YYYY-MM' format for historical data for intraday intervals.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: Returns the data in JSON format (default) or CSV format if requested.
        """
        url = f'{self.base_url}MACDEXT&symbol={ticker}&interval={interval}&series_type={series_type}&fastperiod={fastperiod}&slowperiod={slowperiod}&signalperiod={signalperiod}&fastmatype={fastmatype}&slowmatype={slowmatype}&signalmatype={signalmatype}&apikey={apikey}'

        # If the month parameter is provided, add it to the URL
        if month:
            url += f'&month={month}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def stoch(self, ticker, interval='daily', fastkperiod=5, slowkperiod=3, slowdperiod=3, 
              slowkmatype=0, slowdmatype=0, month=None, datatype='csv'):
        """
        Fetches the Stochastic Oscillator (STOCH) data.

        Parameters:
            ticker (str): The stock symbol (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            fastkperiod (int): Time period of the fastk moving average. Default is 5.
            slowkperiod (int): Time period of the slowk moving average. Default is 3.
            slowdperiod (int): Time period of the slowd moving average. Default is 3.
            slowkmatype (int): Moving average type for slowk. Default is 0 (SMA).
            slowdmatype (int): Moving average type for slowd. Default is 0 (SMA).
            month (str, optional): For historical data, specify a month in 'YYYY-MM' format.
            datatype (str): Format of returned data ('json' or 'csv'). Default is 'json'.

        Returns:
            dict or str: Returns data in JSON format or CSV format based on datatype.
        """
        url = f'{self.base_url}STOCH&symbol={ticker}&interval={interval}&fastkperiod={fastkperiod}&slowkperiod={slowkperiod}&slowdperiod={slowdperiod}&slowkmatype={slowkmatype}&slowdmatype={slowdmatype}&apikey={self.api_key}'

        # If the month parameter is provided, include it in the URL
        if month:
            url += f'&month={month}'

        # If datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (either JSON or CSV)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def stochf(self, ticker, interval='daily', fastkperiod=5, fastdperiod=3, fastdmatype=0, month=None, datatype='csv', apikey=None):
        """
        Fetches the STOCHF (Stochastic Fast) data.

        Parameters:
            ticker (str): The ticker symbol for the stock or asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
                            Supported values: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
            fastkperiod (int): The period for the fastk moving average. Default is 5.
            fastdperiod (int): The period for the fastd moving average. Default is 3.
            fastdmatype (int): The type of moving average for the fastd moving average. Default is 0 (SMA).
                               Other options: 1 (EMA), 2 (WMA), etc.
            month (str, optional): Specify the month in 'YYYY-MM' format for historical data (for intraday intervals).
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: Returns the data in JSON format (default) or CSV format if requested.
        """
        url = f'{self.base_url}STOCHF&symbol={ticker}&interval={interval}&fastkperiod={fastkperiod}&fastdperiod={fastdperiod}&fastdmatype={fastdmatype}&apikey={apikey}'

        # If the month parameter is provided, add it to the URL
        if month:
            url += f'&month={month}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def rsi(self, ticker, interval='daily', time_period=14, series_type='close', datatype='csv'):
        """
        Fetches the RSI (Relative Strength Index) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
                            Supported values: '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'.
            time_period (int): The number of data points used to calculate the RSI. Default is 14.
            series_type (str): The price type to use for calculation. Default is 'close'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The RSI data in JSON format (default) or CSV format.
        """
        # Constructing the URL
        url = f'{self.base_url}function=RSI&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Sending the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def stochrsi(self, ticker, interval='daily', time_period=14, series_type='close', fastkperiod=5, fastdperiod=3, fastdmatype=0, datatype='csv'):
        """
        Fetches the STOCHRSI (Stochastic Relative Strength Index) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): The number of data points used to calculate the STOCHRSI. Default is 14.
            series_type (str): The price type to use for calculation. Default is 'close'.
            fastkperiod (int): The period of the fast %K moving average. Default is 5.
            fastdperiod (int): The period of the fast %D moving average. Default is 3.
            fastdmatype (int): The type of moving average for the fast %D moving average. Default is 0 (SMA).
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The STOCHRSI data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=STOCHRSI&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&fastkperiod={fastkperiod}&fastdperiod={fastdperiod}&fastdmatype={fastdmatype}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()
            
    def willr(self, ticker, interval='daily', time_period=14, datatype='csv'):
        """
        Fetches the Williams %R (WILLR) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): The number of data points used to calculate the WILLR. Default is 14.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The WILLR data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=WILLR&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def adx(self, ticker, interval='daily', time_period=14, datatype='csv'):
        """
        Fetches the ADX (Average Directional Index) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): The number of data points used to calculate the ADX. Default is 14.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The ADX data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=ADX&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def adxr(self, ticker, interval='daily', time_period=14, datatype='csv'):
        """
        Fetches the ADXR (Average Directional Index Rating) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): The number of data points used to calculate the ADXR. Default is 14.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The ADXR data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=ADXR&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def apo(self, ticker, interval='daily', series_type='close', fastperiod=12, slowperiod=26, matype=0, datatype='csv'):
        """
        Fetches the APO (Absolute Price Oscillator) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            series_type (str): The price type in the time series. Options: 'close', 'open', 'high', 'low'. Default is 'close'.
            fastperiod (int): The time period for the fast moving average. Default is 12.
            slowperiod (int): The time period for the slow moving average. Default is 26.
            matype (int): The type of moving average to use. Default is 0 (Simple Moving Average).
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The APO data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=APO&symbol={ticker}&interval={interval}&series_type={series_type}&fastperiod={fastperiod}&slowperiod={slowperiod}&matype={matype}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()


    def ppo(self, ticker, interval='daily', series_type='close', fastperiod=12, slowperiod=26, matype=0, datatype='csv'):
        """
        Fetches the PPO (Percentage Price Oscillator) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            series_type (str): The price type in the time series. Options: 'close', 'open', 'high', 'low'. Default is 'close'.
            fastperiod (int): The time period for the fast moving average. Default is 12.
            slowperiod (int): The time period for the slow moving average. Default is 26.
            matype (int): The type of moving average to use. Default is 0 (Simple Moving Average).
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The PPO data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=PPO&symbol={ticker}&interval={interval}&series_type={series_type}&fastperiod={fastperiod}&slowperiod={slowperiod}&matype={matype}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def mom(self, ticker, interval='daily', time_period=10, series_type='close', datatype='csv'):
        """
        Fetches the MOM (Momentum) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): The number of data points used to calculate each MOM value. Default is 10.
            series_type (str): The price type in the time series. Options: 'close', 'open', 'high', 'low'. Default is 'close'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The MOM data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=MOM&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()
        
    def bop(self, ticker, interval='daily', datatype='csv'):
        """
        Fetches the BOP (Balance of Power) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The BOP data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=BOP&symbol={ticker}&interval={interval}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def cci(self, ticker, interval='daily', time_period=14, datatype='csv'):
        """
        Fetches the CCI (Commodity Channel Index) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each CCI value. Default is 14.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The CCI data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=CCI&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def cmo(self, ticker, interval='daily', time_period=14, series_type='close', datatype='csv'):
        """
        Fetches the Chande Momentum Oscillator (CMO) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each CMO value. Default is 14.
            series_type (str): The desired price type in the time series. Options: 'close', 'open', 'high', 'low'. Default is 'close'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The CMO data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=CMO&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def roc(self, ticker, interval='daily', time_period=10, series_type='close', datatype='csv'):
        """
        Fetches the Rate of Change (ROC) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each ROC value. Default is 10.
            series_type (str): The desired price type in the time series. Options: 'close', 'open', 'high', 'low'. Default is 'close'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The ROC data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=ROC&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def rocr(self, ticker, interval='daily', time_period=10, series_type='close', datatype='csv'):
        """
        Fetches the Rate of Change Ratio (ROCR) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each ROCR value. Default is 10.
            series_type (str): The desired price type in the time series. Options: 'close', 'open', 'high', 'low'. Default is 'close'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The ROCR data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=ROCR&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def aroon(self, ticker, interval='daily', time_period=14, datatype='csv'):
        """
        Fetches the Aroon indicator data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each Aroon value. Default is 14.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The Aroon data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=AROON&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def aroonosc(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Aroon Oscillator data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each Aroon Oscillator value. Default is 10.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The Aroon Oscillator data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=AROONOSC&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def mfi(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Money Flow Index (MFI) data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each MFI value. Default is 10.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The MFI data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=MFI&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()

    def trix(self, ticker, interval='daily', time_period=10, series_type='close', datatype='csv'):
        """
        Fetches the TRIX data for the given ticker symbol.

        Parameters:
            ticker (str): The ticker symbol for the asset (e.g., 'IBM').
            interval (str): Time interval between two consecutive data points. Default is 'daily'.
            time_period (int): Number of data points used to calculate each TRIX value. Default is 10.
            series_type (str): The price type to use (close, open, high, low). Default is 'close'.
            datatype (str): The format of the returned data. Options: 'json' (default), 'csv'.
            apikey (str): Your API key for authentication.

        Returns:
            dict or str: The TRIX data in JSON format (default) or CSV format.
        """
        # Construct the URL for the API request
        url = f'{self.base_url}function=TRIX&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}'

        # If the datatype is specified, add it to the URL
        if datatype:
            url += f'&datatype={datatype}'

        # Send the GET request to the API
        try:
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for bad HTTP status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

        # Return data in the specified format (json or csv)
        if datatype == 'csv':
            return r.text
        else:
            return r.json()
        
    def ultosc(self, ticker, interval='daily', timeperiod1=8, timeperiod2=14, timeperiod3=28, datatype='csv'):
        """
        Fetches the Ultimate Oscillator (ULTOSC) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'daily'.
        - timeperiod1 (int): The first time period used in the ULTOSC formula. Default is 8.
        - timeperiod2 (int): The second time period used in the ULTOSC formula. Default is 14.
        - timeperiod3 (int): The third time period used in the ULTOSC formula. Default is 28.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=ULTOSC{ticker_param}&interval={interval}&timeperiod1={timeperiod1}&timeperiod2={timeperiod2}&timeperiod3={timeperiod3}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def dx(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Directional Movement Index (DX) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'daily'.
        - time_period (int): The number of periods used in the DX calculation. Default is 10.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=DX{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def minus_di(self, ticker, interval='weekly', time_period=10, datatype='csv'):
        """
        Fetches the Minus Directional Indicator (-DI) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'weekly'.
        - time_period (int): The number of periods used in the calculation of -DI. Default is 10.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=MINUS_DI{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def plus_di(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Plus Directional Indicator (+DI) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'daily'.
        - time_period (int): The number of periods used in the calculation of +DI. Default is 10.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=PLUS_DI{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def minus_dm(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Minus Directional Movement (-DM) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'daily'.
        - time_period (int): The number of periods used in the calculation of -DM. Default is 10.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=MINUS_DM{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def plus_dm(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Plus Directional Movement (+DM) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'daily'.
        - time_period (int): The number of periods used in the calculation of +DM. Default is 10.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=PLUS_DM{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def bbands(self, ticker, interval='weekly', time_period=5, series_type='close', nbdevup=3, nbdevdn=3, matype=0, datatype='csv'):
        """
        Fetches the Bollinger Bands (BBANDS) for a given ticker symbol.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are 'daily', 'weekly', or 'monthly'. Default is 'weekly'.
        - time_period (int): The number of periods used in the BBANDS calculation. Default is 5.
        - series_type (str): The type of price to use for the calculation. Valid options are 'close', 'open', 'high', or 'low'. Default is 'close'.
        - nbdevup (int): The number of standard deviations for the upper band. Default is 3.
        - nbdevdn (int): The number of standard deviations for the lower band. Default is 3.
        - matype (int): The type of moving average used for the BBANDS. Default is 0 (simple moving average).
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=BBANDS{ticker_param}&interval={interval}&time_period={time_period}&series_type={series_type}&nbdevup={nbdevup}&nbdevdn={nbdevdn}&matype={matype}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def midpoint(self, ticker, interval='daily', time_period=10, series_type='close', datatype='csv'):
        """
        Fetches the Midpoint (MIDPOINT) values for a given ticker symbol.

        The MIDPOINT is calculated as the average of the highest high and the lowest low over a specified time period.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'. Default is 'daily'.
        - time_period (int): The number of data points used to calculate each MIDPOINT value. Default is 10.
        - series_type (str): The type of price to use for the calculation. Valid options are 'close', 'open', 'high', 'low'. Default is 'close'.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=MIDPOINT{ticker_param}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def midprice(self, ticker, interval='daily', time_period=10, datatype='csv'):
        """
        Fetches the Midprice (MIDPRICE) values for a given ticker symbol.

        The MIDPRICE is calculated as the average of the highest high and the lowest low over a specified time period.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'. Default is 'daily'.
        - time_period (int): The number of data points used to calculate each MIDPRICE value. Default is 10.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=MIDPRICE{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def sar(self, ticker, interval='daily', acceleration=0.02, maximum=0.2, datatype='csv'):
        """
        Fetches the Parabolic SAR (SAR) values for a given ticker symbol.

        The SAR (Stop and Reverse) is a trend-following indicator that provides potential entry and exit signals.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'. Default is 'daily'.
        - acceleration (float): The acceleration factor. Default is 0.02.
        - maximum (float): The maximum acceleration factor. Default is 0.2.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=SAR{ticker_param}&interval={interval}&acceleration={acceleration}&maximum={maximum}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def trange(self, ticker, interval='daily', datatype='csv'):
        """
        Fetches the True Range (TRANGE) values for a given ticker symbol.

        The True Range is a volatility indicator that captures the range of price movement.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'. Default is 'daily'.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=TRANGE{ticker_param}&interval={interval}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def atr(self, ticker, interval='daily', time_period=14, datatype='csv'):
        """
        Fetches the Average True Range (ATR) values for a given ticker symbol.

        The ATR is a measure of volatility based on the True Range, typically used to assess the volatility of an asset.

        Parameters:
        - ticker (str): The stock symbol (e.g., "AAPL").
        - interval (str): The time interval between data points. Valid values are '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'. Default is 'daily'.
        - time_period (int): The number of periods used to calculate the ATR. Default is 14.
        - datatype (str): The format of the returned data. Valid values are 'json' or 'csv'. Default is 'json'.
        """
        ticker_param = f'&symbol={ticker}'
        url = f'{self.base_url}function=ATR{ticker_param}&interval={interval}&time_period={time_period}&apikey={self.api_key}&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def natr(self, ticker, interval='weekly', time_period=14, month=None, datatype='csv'):
        """
        Fetches the Normalized Average True Range (NATR) data for a given ticker symbol.
        
        Args:
        ticker (str): The ticker symbol for the stock, e.g., 'AAPL'.
        interval (str): Time interval between data points. Options are: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        time_period (int): Number of data points used for the calculation of NATR. 
        month (str, optional): Only used for intraday data. Specify a specific month for calculation (YYYY-MM).
        datatype (str): Return data format. Default is 'json', can also be 'csv'.
        
        Example usage:
        api_handler.natr("AAPL")
        """
        url = f'{self.base_url}query?function=NATR&symbol={ticker}&interval={interval}&time_period={time_period}&apikey={self.api_key}'
        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ad(self, ticker, interval='daily', month=None, datatype='csv'):
        """
        Fetches the Chaikin A/D line (AD) data for a given ticker symbol.
        
        Args:
        ticker (str): The ticker symbol for the stock, e.g., 'AAPL'.
        interval (str): Time interval between data points. Options are: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        month (str, optional): Specify a specific month for calculation (YYYY-MM).
        datatype (str): Return data format. Default is 'json', can also be 'csv'.
        
        Example usage:
        api_handler.ad("AAPL")
        """
        url = f'{self.base_url}query?function=AD&symbol={ticker}&interval={interval}&apikey={self.api_key}'
        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def adosc(self, ticker, interval='daily', fastperiod=5, slowperiod=10, month=None, datatype='csv'):
        """
        Fetches the Chaikin A/D Oscillator (ADOSC) data for a given ticker symbol.
        
        Args:
        ticker (str): The ticker symbol for the stock, e.g., 'AAPL'.
        interval (str): Time interval between data points. Options are: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        fastperiod (int): Time period for the fast exponential moving average (EMA).
        slowperiod (int): Time period for the slow exponential moving average (EMA).
        month (str, optional): Specify a specific month for calculation (YYYY-MM).
        datatype (str): Return data format. Default is 'json', can also be 'csv'.
        
        Example usage:
        api_handler.adosc("AAPL")
        """
        url = f'{self.base_url}query?function=ADOSC&symbol={ticker}&interval={interval}&fastperiod={fastperiod}&slowperiod={slowperiod}&apikey={self.api_key}'
        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def obv(self, ticker, interval='daily', month=None, datatype='csv'):
        """
        Fetches the On Balance Volume (OBV) data for a given ticker symbol.
        
        Args:
        ticker (str): The ticker symbol for the stock, e.g., 'AAPL'.
        interval (str): Time interval between data points. Options are: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        month (str, optional): Specify a specific month for calculation (YYYY-MM).
        datatype (str): Return data format. Default is 'json', can also be 'csv'.
        
        Example usage:
        api_handler.obv("AAPL")
        """
        url = f'{self.base_url}query?function=OBV&symbol={ticker}&interval={interval}&apikey={self.api_key}'
        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ht_trendline(self, ticker, interval='daily', series_type='close', month=None, datatype='csv'):
        """
        Fetches the Hilbert Transform Trendline (HT_TRENDLINE) data for a given ticker symbol.
        
        Args:
        ticker (str): The ticker symbol for the stock, e.g., 'AAPL'.
        interval (str): Time interval between data points. Options are: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        series_type (str): The price type to use, options are: open, high, low, close.
        month (str, optional): Specify a specific month for calculation (YYYY-MM).
        datatype (str): Return data format. Default is 'json', can also be 'csv'.
        
        Example usage:
        api_handler.ht_trendline("AAPL")
        """
        url = f'{self.base_url}query?function=HT_TRENDLINE&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}'
        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ht_sine(self, ticker, interval='daily', series_type='close', month=None, datatype='csv'):
        """
        Fetches the Hilbert Transform Sine Wave (HT_SINE) data for a given ticker symbol.
        
        Args:
        ticker (str): The ticker symbol for the stock, e.g., 'AAPL'.
        interval (str): Time interval between data points. Options are: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly.
        series_type (str): The price type to use, options are: open, high, low, close.
        month (str, optional): Specify a specific month for calculation (YYYY-MM).
        datatype (str): Return data format. Default is 'json', can also be 'csv'.
        
        Example usage:
        api_handler.ht_sine("AAPL")
        """
        url = f'{self.base_url}query?function=HT_SINE&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}'
        if month:
            url += f'&month={month}'
        if datatype:
            url += f'&datatype={datatype}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ht_trendmode(self, ticker, interval='weekly', series_type='close'):
        """Get the HT_TRENDMODE for the specified ticker."""
        url = f'{self.base_url}function=HT_TRENDMODE&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ht_dcperiod(self, ticker, interval='daily', series_type='close'):
        """Get the HT_DCPERIOD for the specified ticker."""
        url = f'{self.base_url}function=HT_DCPERIOD&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ht_dcphase(self, ticker, interval='daily', series_type='close'):
        """Get the HT_DCPHASE for the specified ticker."""
        url = f'{self.base_url}function=HT_DCPHASE&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        print(data)

    def ht_phasor(self, ticker, interval='weekly', series_type='close'):
        """Get the HT_PHASOR for the specified ticker."""
        url = f'{self.base_url}function=HT_PHASOR&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        print(data)



