from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import yfinance as yf
from joblib import load
import io
import base64
from datetime import datetime

model = load('./stockModel/model.joblib')

def index(request):
    return render(request, 'Investment Suggestions/index.html')

def formInfo(request):
    start = '2010-01-01'
    end = datetime.now().strftime('%Y-%m-%d')
    stock = request.GET['stockname']

    data = yf.download(stock, start, end)

    data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
    data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0,1))

    pas_100_days = data_train.tail(100)
    data_test = pd.concat([pas_100_days, data_test], ignore_index=True)
    data_test_scale = scaler.fit_transform(data_test)

    ma_50_days = data.Close.rolling(50).mean()
    fig1 = Figure(figsize=(8,6))
    ax1 = fig1.add_subplot(111)
    ax1.plot(ma_50_days, 'r', label='MA 50 Days')
    ax1.plot(data.Close, 'g', label='Close Price')
    ax1.legend()

    ma_100_days = data.Close.rolling(100).mean()
    fig2 = Figure(figsize=(8,6))
    ax2 = fig2.add_subplot(111)
    ax2.plot(ma_50_days, 'r', label='MA 50 Days')
    ax2.plot(ma_100_days, 'b', label='MA 100 Days')
    ax2.plot(data.Close, 'g', label='Close Price')
    ax2.legend()

    ma_200_days = data.Close.rolling(200).mean()
    fig3 = Figure(figsize=(8,6))
    ax3 = fig3.add_subplot(111)
    ax3.plot(ma_100_days, 'r', label='MA 100 Days')
    ax3.plot(ma_200_days, 'b', label='MA 200 Days')
    ax3.plot(data.Close, 'g', label='Close Price')
    ax3.legend()

    x = []
    y = []

    for i in range(100, data_test_scale.shape[0]):
        x.append(data_test_scale[i-100:i])
        y.append(data_test_scale[i,0])

    x, y = np.array(x), np.array(y)

    predict = model.predict(x)

    scale = 1/scaler.scale_

    predict = predict * scale
    y = y * scale

    fig4 = Figure(figsize=(8,6))
    ax4 = fig4.add_subplot(111)
    ax4.plot(predict, 'r', label='Original Price')
    ax4.plot(y, 'g', label='Predicted Price')
    ax4.legend()

    figures = {
        'Price vs MA50': get_base64_encoded_image(fig1),
        'Price vs MA50 vs MA100': get_base64_encoded_image(fig2),
        'Price vs MA100 vs MA200': get_base64_encoded_image(fig3),
        'Original price vs Predicted price': get_base64_encoded_image(fig4),
    }

    latest_data = data.tail(10)

    return render(request, 'Investment Suggestions/result.html', {'result': latest_data, 'figures': figures})

def get_base64_encoded_image(fig):
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    data = buf.getvalue()
    return base64.b64encode(data).decode('utf-8')
