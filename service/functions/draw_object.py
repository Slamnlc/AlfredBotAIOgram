import json
import datetime
from data.config import IMAGE_PATH
import locale
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


def drawHistogramm(howMany, currency, userID):
    locale.setlocale(locale.LC_ALL, "ru_RU")
    osX = []
    osY = []
    with open(f'/Users/maksim/CurrencyBot/rate/{currency}.json', 'r') as outFile:
        data = json.load(outFile)
    daysNumber = 0
    minValue = 0
    maxValue = 0
    lastMonth = 0
    ii = 0
    monthArray = []
    dataList = list(data.keys())
    dataList.reverse()
    fig, ax = plt.subplots()
    for i in range(dataList.__len__() - 1 - howMany, dataList.__len__()):
        currDate = datetime.datetime.strptime(dataList[i], '%Y%m%d')
        monthNumber = currDate.strftime('%b.%y')
        if (lastMonth != monthNumber and lastMonth != 0) or i == dataList.__len__() - 1:
            if len(monthArray) != 0:
                osX.append(lastMonth)
                middleValue = round(sum(monthArray) / len(monthArray), 2)
                if min(monthArray) > minValue:
                    minValue = min(monthArray)
                if max(monthArray) > maxValue:
                    maxValue = max(monthArray)
                osY.append(middleValue)
                ax.text(lastMonth, middleValue + 0.1, middleValue, ha="center")
                monthArray = []
                ii += 1
            lastMonth = monthNumber
        else:
            monthArray.append(data[dataList[i]]['rate'])
            lastMonth = monthNumber
        daysNumber += 1
    minValue -= minValue * 0.2
    maxValue += maxValue * 0.008
    ax.bar(osX, osY)
    ax.set_ylim(minValue, maxValue)
    fig.set_figwidth(ii + 2)
    fig.set_figheight(7)
    xax = ax.xaxis
    xlabels = xax.get_ticklabels()

    for label in xlabels:
        label.set_rotation(75)
    if ii < 5:
        monthName = 'месяца'
    else:
        monthName = 'месяцев'
    plt.title(f'Средний курс {currency} за {ii} {monthName} ({daysNumber - 1} дней)')
    plt.savefig(f'{IMAGE_PATH}{userID}.png')
    return f'{IMAGE_PATH}{userID}.png'


def drawDiagram(howMany, currency, userID):
    with open(f'/Users/maksim/CurrencyBot/rate/{currency}.json', 'r') as outFile:
        data = json.load(outFile)
    dataList = list(data.keys())
    dataList.reverse()
    osX = []
    osY = []
    for i in range(dataList.__len__() - 1 - howMany, dataList.__len__()):
        currDate = datetime.datetime.strptime(dataList[i], '%Y%m%d')
        osX.append(currDate.strftime("%d.%m"))
        osY.append(data[dataList[i]]['rate'])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(osX, osY)
    xax = ax.xaxis
    xlabels = xax.get_ticklabels()

    for label in xlabels:
        label.set_rotation(75)
    fig.set_figwidth(15)
    fig.set_figheight(6)
    plt.title(f'Курс {currency} за {howMany} (дней)')
    plt.grid(True)
    plt.savefig(f'{IMAGE_PATH}{userID}.png')
    return f'{IMAGE_PATH}{userID}.png'
