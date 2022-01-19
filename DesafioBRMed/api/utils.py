from datetime import datetime, date, timedelta

from django.db.utils import IntegrityError
from workalendar.america.brazil import BrazilRioDeJaneiro as Rio

import requests

from .models import CurrencyRate


def updateDb(dates):
    dates = [date.strftime("%Y-%m-%d") for date in dates]
    for date in dates:
        url = f"https://api.vatcomply.com/rates?date={date}&base=USD"
        response = requests.get(url)
        # Se a data da resposta da API for diferente da data requisitada,
        # quer dizer que a cotaçao dessa data nao esta disponivel
        #if date != response.json()["date"]:
        #   continue
        
        rates = response.json()["rates"]
        try: # Se a data ja exitir no banco nao adiciona-la novamente
            CurrencyRate.objects.create(
                brl=rates["BRL"],
                eur=rates["EUR"],
                jpy=rates["JPY"], 
                date=datetime.strptime(date, "%Y-%m-%d")
            )
        except IntegrityError:
            pass


def getLast5WorkinDays():
    cal = Rio()
    today = datetime.now()- timedelta(days=1)
    i = 0
    working_days = []
    while i < 5:
        if cal.is_working_day(today):
            working_days.append(today.date())
            i += 1
            
        today = today - timedelta(days=1)

    return working_days


def getWorkinDays(start_date, end_date):
    cal = Rio()
    i = 0
    working_days = []
    while i < 5:
        if start_date > end_date:
            break
        
        if cal.is_working_day(end_date):
            working_days.append(end_date.date())
            i += 1
            
        end_date = end_date - timedelta(days=1)
        
    return working_days
