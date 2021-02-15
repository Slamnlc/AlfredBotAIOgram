from datetime import date, timedelta
from data.config import IMAGE_PATH
import locale
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from loader import db


def drawHistogramm(howMany, currency, userID):
    locale.setlocale(locale.LC_ALL, "ru_RU")
    osX = []
    osY = []
    today = date.today() - timedelta(days=howMany)
    data = db.getFromDB(
        tableName=currency,
        what="to_char(date,'TMMon.YY') as dt, "
             'cast(round(avg(rate),3) as float)',
        where=f"date >= '{today}'",
        groupBy='group by dt, extract(MONTH from date), extract(year from date)',
        orderBy='order by extract(year from date) asc,extract(MONTH from date) asc'
    )

    fig, ax = plt.subplots()
    for item in data:
        osX.append(item[0])
        osY.append(item[1])
        if item[1] > 10:
            offset = 0.1
        elif item[1] > 2:
            offset = 0.01
        elif item[1] > 1:
            offset = 0.005
        else:
            offset = 0.001
        ax.text(item[0], item[1] + offset, item[1], ha='center')

    minValue = min(osY) - min(osY) * 0.2
    maxValue = max(osY) + max(osY) * 0.015
    ax.bar(osX, osY)
    ax.set_ylim(minValue, maxValue)

    fig.set_figwidth(data.__len__() + 2)
    fig.set_figheight(7)
    xax = ax.xaxis
    xlabels = xax.get_ticklabels()

    for label in xlabels:
        label.set_rotation(75)
    if data.__len__() < 5:
        monthName = 'месяца'
    else:
        monthName = 'месяцев'

    plt.title(f'Средний курс {currency} за {data.__len__()} {monthName} ({howMany} дней)')
    plt.savefig(f'{IMAGE_PATH}{userID}.png')
    return f'{IMAGE_PATH}{userID}.png'


def drawDiagram(howMany, currency, userID):
    today = date.today() - timedelta(days=howMany)
    data = db.getFromDB(
        tableName=currency,
        what="to_char(date,'DD.MM') as dt,cast(rate as float)",
        where=f"date >= '{today}'",
        orderBy='order by date asc'
    )

    osX = []
    osY = []

    for item in data:
        osX.append(item[0])
        osY.append(item[1])

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
