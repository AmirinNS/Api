import urllib, json, csv, urllib2, base64
# Import local file
import spreadsheet

# Testing server
from bottle import Bottle, route, run, request, abort, template, error, response, static_file

# All Routes

# Stock Details Data
@route('/api/stock/data/<stockName>')
def getStockDetailsData(stockName = 'fbmklci'):
    stock = read_json(stockName)
    if stock != None:
        result = stockDetailsData(stock)
        return json.dumps(result)
    else:
        return json.dumps({})

# Fundamental Trends Data
@route('/api/stock/trend/<stockName>')
def getTrendData(stockName):
    result = read_csv(stockName)
    if result != None:
        return template('chart', value=json.dumps(result), chartTitle=stockName)
    else:
        return None

# Serve js
@route('/js/<jsFile>')
def serve_js_files(jsFile):
    filePath = './js/'
    return static_file(jsFile, filePath)
    

# Get stock data
def read_json(stockName):

    # url string
    url = "http://www.isaham.my/api/stock/"+stockName
    
    # load url data
    try:
        response = urllib.urlopen(url)
        return json.loads(response.read())
    except:
        return None

#  Get fundemental trend data from csv
def read_csv(stockName):

    # url string
    url = "http://www.isaham.my/csv/fundamental/%s.csv" % stockName.upper()

    # load url data
    try:
        response = urllib2.urlopen(url)
        cr = csv.reader(response)
        dataTrend = {}
        for row in cr:
            dataTrend[ row.pop(0) ] = row
        return dataTrend
    except:
        return None

# Formatting the fundemental ratio
def fundamental_ratio (stock):
    #Spreadsheet API
    variableFullName = spreadsheet.fetchSpreadSheet()
    
    f_ratioArray = []

    #PE ratio
    if stock['pe'] < stock['avg_pe']-1:
        f_ratioArray.append( {'name': variableFullName['pe'], 'color': '#009900', 'val': stock['pe']} )
        
    elif stock['pe'] > stock['avg_pe']+1:
        f_ratioArray.append( {'name': variableFullName['pe'], 'color': '#ff1a1a', 'val': stock['pe']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['pe'], 'color': '#000', 'val': stock['pe']} )
        

    # EV / EBITDA
    if stock['ev_ebitda'] < stock['avg_ev_ebitda']-1:
        f_ratioArray.append( {'name': variableFullName['ev_ebitda'], 'color': '#009900', 'val': stock['ev_ebitda']} )
        
    elif stock['ev_ebitda'] > stock['avg_ev_ebitda']+1:
        f_ratioArray.append( {'name': variableFullName['ev_ebitda'], 'color': '#ff1a1a', 'val': stock['ev_ebitda']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['ev_ebitda'], 'color': '#000', 'val': stock['ev_ebitda']} )
        

    # PEG
    if 0 < stock['peg'] < 1.0:
        f_ratioArray.append( {'name': variableFullName['peg'], 'color': '#009900', 'val': stock['peg']} )
        
    elif stock['peg'] > 1.5 or stock['peg'] <= 0:
        f_ratioArray.append( {'name': variableFullName['peg'], 'color': '#ff1a1a', 'val': stock['peg']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['peg'], 'color': '#000', 'val': stock['peg']} )
        

    # Sharpe Ratio (3 yrs)
    if stock['sharpe_ratio_600'] > 0.5:
        f_ratioArray.append( {'name': variableFullName['sharpe_ratio_600'], 'color': '#009900', 'val': stock['sharpe_ratio_600']} )
         
    elif stock['sharpe_ratio_600'] < 0.0:
        f_ratioArray.append( {'name': variableFullName['sharpe_ratio_600'], 'color': '#ff1a1a', 'val': stock['sharpe_ratio_600']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['sharpe_ratio_600'], 'color': '#000', 'val': stock['sharpe_ratio_600']} )
        

    # LTS Score
    if stock['lts_score'] > 7.5:
        f_ratioArray.append( {'name': variableFullName['lts_score'], 'color': '#009900', 'val': stock['lts_score']} )
        
    elif stock['lts_score'] < 4.0:
        f_ratioArray.append( {'name': variableFullName['lts_score'], 'color': '#ff1a1a', 'val': stock['lts_score']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['lts_score'], 'color': '#000', 'val': stock['lts_score']} )
        

    # Altman Z
    if stock['z'] > 3:
        f_ratioArray.append( {'name': variableFullName['z'], 'color': '#009900', 'val': stock['z']} )
        
    elif stock['z'] < 1.8:
        f_ratioArray.append( {'name': variableFullName['z'], 'color': '#ff1a1a', 'val': stock['z']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['z'], 'color': '#000', 'val': stock['z']} )
        
    
    # Beaver
    if stock['beaver'] > 0.06:
        f_ratioArray.append( {'name': variableFullName['beaver'], 'color': '#009900', 'val': stock['beaver']} )
        
    elif stock['beaver'] < 0.03:
        f_ratioArray.append( {'name': variableFullName['beaver'], 'color': '#ff1a1a', 'val': stock['beaver']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['beaver'], 'color': '#000', 'val': stock['beaver']} )
        

    # Current Ratio
    if stock['current_ratio'] > 2:
        f_ratioArray.append( {'name': variableFullName['current_ratio'], 'color': '#009900', 'val': stock['current_ratio']} )
        
    elif stock['current_ratio'] < 1.5:
        f_ratioArray.append( {'name': variableFullName['current_ratio'], 'color': '#ff1a1a', 'val': stock['current_ratio']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['current_ratio'], 'color': '#000', 'val': stock['current_ratio']} )
        

    # Debt / Equity (DE) Ratio
    if stock['de'] < 0.5:
        f_ratioArray.append( {'name': variableFullName['de'], 'color': '#009900', 'val': stock['de']} )
        
    elif stock['de'] > 1.0:
        f_ratioArray.append( {'name': variableFullName['de'], 'color': '#ff1a1a', 'val': stock['de']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['de'], 'color': '#000', 'val': stock['de']} )
        

    # Revenue QoQ
    if stock['revenue_qoq'] > 5:
        f_ratioArray.append( {'name': variableFullName['revenue_qoq'], 'color': '#009900', 'val': stock['revenue_qoq']} )
        
    elif stock['revenue_qoq'] < 0:
        f_ratioArray.append( {'name': variableFullName['revenue_qoq'], 'color': '#ff1a1a', 'val': stock['revenue_qoq']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['revenue_qoq'], 'color': '#000', 'val': stock['revenue_qoq']} )
        

    # Profit QoQ
    if stock['profit_qoq'] > 5 and (stock['opi_qoq']*2.0) > stock['profit_qoq']:
        f_ratioArray.append( {'name': variableFullName['profit_qoq'], 'color': '#009900', 'val': stock['profit_qoq']} )
        
    elif stock['profit_qoq'] < 0:
        f_ratioArray.append( {'name': variableFullName['profit_qoq'], 'color': '#ff1a1a', 'val': stock['profit_qoq']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['profit_qoq'], 'color': '#000', 'val': stock['profit_qoq']} )
        

    # Profit YoY
    if stock['profit_yoy'] > 5:
        f_ratioArray.append( {'name': variableFullName['profit_yoy'], 'color': '#009900', 'val': stock['profit_yoy']} )
        
    elif stock['profit_yoy'] < 0:
        f_ratioArray.append( {'name': variableFullName['profit_yoy'], 'color': '#ff1a1a', 'val': stock['profit_yoy']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['profit_yoy'], 'color': '#000', 'val': stock['profit_yoy']} )
        

    # NTA QoQ
    if stock['ntaps_qoq'] > 5:
        f_ratioArray.append( {'name': variableFullName['ntaps_qoq'], 'color': '#009900', 'val': stock['ntaps_qoq']} )
        
    elif stock['ntaps_qoq'] < 0:
        f_ratioArray.append( {'name': variableFullName['ntaps_qoq'], 'color': '#ff1a1a', 'val': stock['ntaps_qoq']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['ntaps_qoq'], 'color': '#000', 'val': stock['ntaps_qoq']} )
        

    # Profit Margin
    if stock['margin'] > 15:
        f_ratioArray.append( {'name': variableFullName['margin'], 'color': '#009900', 'val': stock['margin']} )
        
    elif stock['margin'] < 5:
        f_ratioArray.append( {'name': variableFullName['margin'], 'color': '#ff1a1a', 'val': stock['margin']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['margin'], 'color': '#000', 'val': stock['margin']} )
        

    # ROE
    if stock['roe'] > 15:
        f_ratioArray.append( {'name': variableFullName['roe'], 'color': '#009900', 'val': stock['roe']} )
        
    elif stock['roe'] < 0.0:
        f_ratioArray.append( {'name': variableFullName['roe'], 'color': '#ff1a1a', 'val': stock['roe']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['roe'], 'color': '#000', 'val': stock['roe']} )
        

    # ROIC
    if stock['roic'] > 15:
        f_ratioArray.append( {'name': variableFullName['roe'], 'color': '#009900', 'val': stock['roe']} )
        
    elif stock['roic'] < 0.0:
        f_ratioArray.append( {'name': variableFullName['roe'], 'color': '#ff1a1a', 'val': stock['roe']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['roe'], 'color': '#000', 'val': stock['roe']} )
        

    # Dividend Per Share (DPS)
    f_ratioArray.append( {'name': variableFullName['dps'], 'color': '#000', 'val': stock['dps']} )
    

    # Dividend Yield (DY)
    if stock['dy'] > 2:
        f_ratioArray.append( {'name': variableFullName['dy'], 'color': '#009900', 'val': stock['dy']} )
        
    elif stock['dy'] < 0:
        f_ratioArray.append( {'name': variableFullName['dy'], 'color': '#ff1a1a', 'val': stock['dy']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['dy'], 'color': '#000', 'val': stock['dy']} )
        

    # FCF Yield
    if stock['fcf_yield'] > 5:
        f_ratioArray.append( {'name': variableFullName['fcf_yield'], 'color': '#009900', 'val': stock['fcf_yield']} )
        
    elif stock['fcf_yield'] < 0:
        f_ratioArray.append( {'name': variableFullName['fcf_yield'], 'color': '#ff1a1a', 'val': stock['fcf_yield']} )
        
    else:
        f_ratioArray.append( {'name': variableFullName['fcf_yield'], 'color': '#000', 'val': stock['fcf_yield']} )
        
    
    return f_ratioArray

# Formatting Support and Resistance
def supportResistance(stock):
    snrArray = []
    for s in stock['resistance_vop'][::-1]:
        if s[0] in stock['strong_resistances']:
            snrArray.append( {'price': s[0], 'volume': s[1], 'color': '#FFB4B2'} )
        else:
            snrArray.append( {'price': s[0], 'volume': s[1], 'color': '#fff'} )

    snrArray.append( {'price': stock['lp1'], 'volume': '-', 'color': '#FFF9B2'} )

    for s in stock['support_vop']:
        if s[0] in stock['strong_supports']:
            snrArray.append( {'price': s[0], 'volume': s[1], 'color': '#DAF7A6'} )
        else:
            snrArray.append( {'price': s[0], 'volume': s[1], 'color': '#fff'} )
    
    return snrArray

# Formatting Trading Signals
def tradingSignals(stock):

    signalsArray = []

    # MA20
    if stock['lp1'] > stock['ma20']:
        signalsArray.append( {'name': 'Moving Average (Short Term)', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['lp1'] < stock['ma20']:
        signalsArray.append( {'name': 'Moving Average (Short Term)', 'signal': 'SELL', 'color': '#ff1a1a'} )  
    else:
        signalsArray.append( {'name': 'Moving Average (Short Term)', 'signal': 'HOLD', 'color': '#000'} )

    # MA50
    if stock['lp1'] > stock['ma50']:
        signalsArray.append( {'name': 'Moving Average (Mid Term)', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['lp1'] < stock['ma50']:
        signalsArray.append( {'name': 'Moving Average (Mid Term)', 'signal': 'SELL', 'color': '#ff1a1a'} )  
    else:
        signalsArray.append( {'name': 'Moving Average (Mid Term)', 'signal': 'HOLD', 'color': '#000'} )
    
    # MA200
    if stock['lp1'] > stock['ma200']:
        signalsArray.append( {'name': 'Moving Average (Long Term)', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['lp1'] < stock['ma200']:
        signalsArray.append( {'name': 'Moving Average (Long Term)', 'signal': 'SELL', 'color': '#ff1a1a'} )  
    else:
        signalsArray.append( {'name': 'Moving Average (Long Term)', 'signal': 'HOLD', 'color': '#000'} )

    # Ichimoku Kumo
    if 0 <= stock['kumo_cross'] <= 2:
        signalsArray.append( {'name': 'Ichimoku Kumo', 'signal': 'BUY (New)', 'color': '#009900'} )
    elif stock['ichimoku'] == 1:
        signalsArray.append( {'name': 'Ichimoku Kumo', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['ichimoku'] < -1:
        signalsArray.append( {'name': 'Ichimoku Kumo', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:
        signalsArray.append( {'name': 'Ichimoku Kumo', 'signal': 'HOLD', 'color': '#000'} )

    # Bollinger Band
    if stock['bb_cross'] > 0:
        signalsArray.append( {'name': 'Bollinger Band', 'signal': 'BUY (Oversold Cross)', 'color': '#009900'} )
    elif stock['bb_squeeze_buy'] > 0 and stock['vmar3'] > 0 and stock["no_action"] == 0:
        signalsArray.append( {'name': 'Bollinger Band', 'signal': 'BUY (Squeeze Breakout)', 'color': '#009900'} )
    elif 0 < stock['bb_breakout'] < 6:
        signalsArray.append( {'name': 'Bollinger Band', 'signal': 'BUY (Breakout)', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'Bollinger Band', 'signal': '-', 'color': '#000'} )

    # RSI
    if stock['rsi_14'] > 50:
        signalsArray.append( {'name': 'RSI', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['rsi_oversold'] > 0:
        signalsArray.append( {'name': 'RSI', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['rsi_14'] < 50:
        signalsArray.append( {'name': 'RSI', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:
        signalsArray.append( {'name': 'RSI', 'signal': 'HOLD', 'color': '#000'} )

    # Stochastic
    if stock['sto_14'] > 50:
        signalsArray.append( {'name': 'Stochastic', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['sto_bullish_cross'] > 0:
        signalsArray.append( {'name': 'Stochastic', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['sto_14'] < 50:
        signalsArray.append( {'name': 'Stochastic', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:
        signalsArray.append( {'name': 'Stochastic', 'signal': 'HOLD', 'color': '#000'} )

    # Heikin-Ashi
    if stock['heikin'] == 1:
        signalsArray.append( {'name': 'Heikin-Ashi', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['ha_bottom'] > 0:
        signalsArray.append( {'name': 'Heikin-Ashi', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['heikin'] == -1:
        signalsArray.append( {'name': 'Heikin-Ashi', 'signal': 'SELL', 'color': '#ff1a1a'} )
    elif stock['ha_top'] > 0:
        signalsArray.append( {'name': 'Heikin-Ashi', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:
        signalsArray.append( {'name': 'Heikin-Ashi', 'signal': 'HOLD', 'color': '#000'} )

    # MACD
    if stock['macd_4r1g'] == 1 and stock["near_ma20"] == 1 and stock['vma50'] > 500000:
        signalsArray.append( {'name': 'MACD', 'signal': 'BUY (4R1G+MA20)', 'color': '#009900'} )
    elif stock['macd_4r1g'] == 1 and stock["macd_line"] > 0  and stock['vma50'] > 500000:
        signalsArray.append( {'name': 'MACD', 'signal': 'BUY (4R1G+Above 0)', 'color': '#009900'} )
    elif stock['macd_line'] > 0 and stock['macd_cross'] > 0:
        signalsArray.append( {'name': 'MACD', 'signal': 'BUY (New Above 0)', 'color': '#009900'} )
    elif stock['macd_line'] > 0:
        signalsArray.append( {'name': 'MACD', 'signal': 'BUY (Above 0)', 'color': '#009900'} )    
    elif stock['macd_oversold'] > 0:
        signalsArray.append( {'name': 'MACD', 'signal': 'BUY (Oversold Cross)', 'color': '#009900'} )    
    elif stock['macd_line'] < 0:
        signalsArray.append( {'name': 'MACD', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:    
        signalsArray.append( {'name': 'MACD', 'signal': 'HOLD', 'color': '#000'} )

    # Solid MA Trend
    if stock['solid_ma'] > 0:
        signalsArray.append( {'name': 'Solid MA Trend', 'signal': 'BUY', 'color': '#009900'} )        
    else:
        signalsArray.append( {'name': 'Solid MA Trend', 'signal': '-', 'color': '#000'} )        
    
    # SAT
    if 0.20 <= stock["lp1"] <= 5 and stock["vma50"] > 500000 and stock["ema9_20"] == 1 and stock["rsi_14_upper"] == 1 and stock["macd_line"] > 0 and stock["macd_histogreen"] == 1:
        signalsArray.append( {'name': 'SAT', 'signal': 'BUY', 'color': '#009900'} )                
    elif stock['perf_1w'] < 0.1342329461:
        signalsArray.append( {'name': 'SAT', 'signal': 'SELL', 'color': '#ff1a1a'} )       
    else:
        signalsArray.append( {'name': 'SAT', 'signal': 'HOLD', 'color': '#000'} )

    # Sector Trend (Long Term)
    if stock["avg_trend_lt"] > 0.5:
        signalsArray.append( {'name': 'Sector Trend (Long Term)', 'signal': 'BUY', 'color': '#009900'} )        
    elif stock["avg_trend_lt"] < 0:
        signalsArray.append( {'name': 'Sector Trend (Long Term)', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:
        signalsArray.append( {'name': 'Sector Trend (Long Term)', 'signal': 'HOLD', 'color': '#000'} )

    # Sector Trend (Short Term)
    if stock["avg_trend_st"] > 0.5:
        signalsArray.append( {'name': 'Sector Trend (Short Term)', 'signal': 'BUY', 'color': '#009900'} )    
    elif stock["avg_trend_st"] < 0:
        signalsArray.append( {'name': 'Sector Trend (Short Term)', 'signal': 'SELL', 'color': '#ff1a1a'} )    
    else:
        signalsArray.append( {'name': 'Sector Trend (Short Term)', 'signal': 'HOLD', 'color': '#000'} )

    # Institutional Holdings
    if stock['insti'] == 1:
        signalsArray.append( {'name': 'Institutional Holdings', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'Institutional Holdings', 'signal': '-', 'color': '#000'} )    
    
    # Beat The Insti
    if stock['insti'] == 1 and stock['insti_diff_price'] > 0.1:
        signalsArray.append( {'name': 'Beat The Insti', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'Beat The Insti', 'signal': '-', 'color': '#000'} )

    # Magic Formula
    if stock['warrant'] == 0 and stock["market_cap"] > 50 and stock['magic_rank'] < 30 and stock['macd_line'] > 0:
        signalsArray.append( {'name': 'Magic Formula', 'signal': 'BUY (Momentum)', 'color': '#009900'} )
    elif stock['warrant'] == 0 and stock["market_cap"] > 50 and stock['magic_rank'] < 30:
        signalsArray.append( {'name': 'Magic Formula', 'signal': 'BUY', 'color': '#009900'} )
    elif stock['magic_rank'] > 700:
        signalsArray.append( {'name': 'Magic Formula', 'signal': 'SELL', 'color': '#ff1a1a'} )
    else:
        signalsArray.append( {'name': 'Magic Formula', 'signal': '-', 'color': '#000'} )

    # Better Than ASB
    if stock['better_than_asb'] > 0:
        signalsArray.append( {'name': 'Better Than ASB', 'signal': 'BUY', 'color': '#009900'} )    
    else:
        signalsArray.append( {'name': 'Better Than ASB', 'signal': '-', 'color': '#000'} )    
    
    # 52-Week High
    if stock['fbo'] > 0:
        signalsArray.append( {'name': '52-Week High', 'signal': 'BUY (Fresh Breakout)', 'color': '#009900'} )
    elif stock['b260'] > -1 and stock['vma5'] > 0:
        signalsArray.append( {'name': '52-Week High', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': '52-Week High', 'signal': '-', 'color': '#000'} )    

    # BTST
    if stock['marubozu'] == 1 and stock['higher_vol'] == 1 and stock['higher_spike'] == 1 and stock['no_action'] <= 2 and stock['tava_vol'] == 1:
        signalsArray.append( {'name': 'BTST', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'BTST', 'signal': '-', 'color': '#000'} )    

    # T+
    if 2 < stock['tplus'] < 8 and stock['tbreak'] == 0:
        signalsArray.append( {'name': 'T+', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'T+', 'signal': '-', 'color': '#000'} )    

    # Candlestick
    if stock['c_pattern2'] == 1 or stock["bullish_hammer_combo"] > 0:
        signalsArray.append( {'name': 'Candlestick', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'Candlestick', 'signal': '-', 'color': '#000'} )    

    # Chart Pattern
    if (stock["high_and_tight"] and stock["high_and_tight_upside"] > 1) or (stock["pipe_bottom"] and stock["pipe_upside"] > 1) or (stock["rounding_bot"] and stock["rounding_upside"]):
        signalsArray.append( {'name': 'Chart Pattern', 'signal': 'BUY', 'color': '#009900'} )
    else:
        signalsArray.append( {'name': 'Chart Pattern', 'signal': '-', 'color': '#000'} )    
        
    return signalsArray

# Pivot Point
def pivotPoint(stock):
    pivotArray = []

    # R2 Daily
    if abs(stock['lp1'] - stock['pp_r2']) == stock['closest_pivot']:
        pivotArray.append( {'name': 'R2', 'daily':  stock['pp_r2'], 'colorDaily': '#82CAFA'} )
    else:
        pivotArray.append( {'name': 'R2', 'daily':  stock['pp_r2'], 'colorDaily': '#fff'} )
    
    # R1 Daily
    if abs(stock['lp1'] - stock['pp_r1']) == stock['closest_pivot']:
        pivotArray.append( {'name': 'R1', 'daily':  stock['pp_r1'], 'colorDaily': '#82CAFA'} )    
    else:
        pivotArray.append( {'name': 'R1', 'daily':  stock['pp_r1'], 'colorDaily': '#fff'} )
    
    # P Daily
    if abs(stock['lp1'] - stock['pp_base']) == stock['closest_pivot']:
        pivotArray.append( {'name': 'P', 'daily':  stock['pp_base'], 'colorDaily': '#82CAFA'} )
    else:
        pivotArray.append( {'name': 'P', 'daily':  stock['pp_base'], 'colorDaily': '#fff'} )

    # S1 Daily
    if abs(stock['lp1'] - stock['pp_s1']) == stock['closest_pivot']:
        pivotArray.append( {'name': 'S1', 'daily':  stock['pp_s1'], 'colorDaily': '#82CAFA'} )
    else:
        pivotArray.append( {'name': 'S1', 'daily':  stock['pp_s1'], 'colorDaily': '#fff'} )
    
    # S2 Daily
    if abs(stock['lp1'] - stock['pp_s2']) == stock['closest_pivot']:
        pivotArray.append( {'name': 'S2', 'daily':  stock['pp_s2'], 'colorDaily': '#82CAFA'} )        
    else:
        pivotArray.append( {'name': 'S2', 'daily':  stock['pp_s2'], 'colorDaily': '#fff'} ) 
    
    # R2 Weekly
    if abs(stock['lp1'] - stock['pp5_r2']) == stock['closest_pivot5']:
        pivotArray[0]['weekly'] = stock['pp5_r2']
        pivotArray[0]['colorWeekly'] = '#82CAFA'
    else:
        pivotArray[0]['weekly'] = stock['pp5_r2']
        pivotArray[0]['colorWeekly'] = '#fff'

    # R1 Weekly
    if abs(stock['lp1'] - stock['pp5_r1']) == stock['closest_pivot5']:
        pivotArray[1]['weekly'] = stock['pp5_r1']
        pivotArray[1]['colorWeekly'] = '#82CAFA'
    else:
        pivotArray[1]['weekly'] = stock['pp5_r1']
        pivotArray[1]['colorWeekly'] = '#fff'
    
    # P Weekly
    if abs(stock['lp1'] - stock['pp5_base']) == stock['closest_pivot5']:
        pivotArray[2]['weekly'] = stock['pp5_base']
        pivotArray[2]['colorWeekly'] = '#82CAFA'
    else:
        pivotArray[2]['weekly'] = stock['pp5_base']
        pivotArray[2]['colorWeekly'] = '#fff'
    
    # S1 Weekly
    if abs(stock['lp1'] - stock['pp5_s1']) == stock['closest_pivot5']:
        pivotArray[3]['weekly'] = stock['pp5_s1']
        pivotArray[3]['colorWeekly'] = '#82CAFA'        
    else:
        pivotArray[3]['weekly'] = stock['pp5_s1']
        pivotArray[3]['colorWeekly'] = '#fff'    
    
    # S2 Weekly
    if abs(stock['lp1'] - stock['pp5_s2']) == stock['closest_pivot5']:
        pivotArray[4]['weekly'] = stock['pp5_s2']
        pivotArray[4]['colorWeekly'] = '#82CAFA'        
    else:
        pivotArray[4]['weekly'] = stock['pp5_s2']
        pivotArray[4]['colorWeekly'] = '#fff'    

    return pivotArray

def getChartImage():
    imgstring = 'iVBORw0KGgoAAAANSUhEUgAAAyEAAAMhCAYAAAD/7r7zAAAgAElEQVR4Xu3XMQ0AAAzDsJU/6bHI5RGoZO3JzhEgQIAAAQIECBAgQCAUWLhligABAgQIECBAgAABAidCPAEBAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQMZzzhwAABIrSURBVIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqmACEm5jREgQIAAAQIECBAgIEL8AAECBAgQIECAAAECqYAISbmNESBAgAABAgQIECAgQvwAAQIECBAgQIAAAQKpgAhJuY0RIECAAAECBAgQICBC/AABAgQIECBAgAABAqnAA+z0AyLxlodYAAAAAElFTkSuQmCC'
    imgdata = base64.b64decode(imgstring)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

def stockDetailsData(stockData):
    data = stockData
    data['fundamental_ratios'] = fundamental_ratio(stockData)
    data['support_resistance'] = supportResistance(stockData)
    data['trading_signals'] = tradingSignals(stockData)
    data['pivot_point'] = pivotPoint(stockData)
    data['profit_ma_chart'] = ''
    data['revenue_ma_chart'] = ''
    return data

run(host='localhost', port=8080)