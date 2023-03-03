from datetime import datetime
from apscheduler.schedulers.background import  BackgroundScheduler

from .jobs import test, surveiller_evenement

"""
interval: use when you want to run the job at fixed intervals of time

cron: use when you want to run the job periodically at certain time(s) of day

"""

"""
Avec intervalle, vous pouvez spécifier que le travail doit s'exécuter, par exemple, toutes les 15 minutes. Un laps de temps fixe entre chaque run et c'est tout.

Avec cron, vous pouvez lui dire de s'exécuter un mardi sur deux à 9h00, ou tous les jours à midi, ou le 1er janvier à 19h00. Dans cron, vous définissez la minute, l'heure, le jour du mois, le mois, le jour de la semaine (par exemple, lundi) et l'année où il doit s'exécuter, et vous pouvez attribuer une périodicité à n'importe lequel d'entre eux (c'est-à-dire tous les lundis ou toutes les cinq minutes ).

Je pense que tout ce que vous pouvez réaliser avec un intervalle peut également être réalisé avec cron, mais pas l'inverse
"""
def start():

    scheduler=BackgroundScheduler()
    #scheduler.add_job(test,'cron',second=5)
    scheduler.add_job(surveiller_evenement,'cron',hour=0)
    scheduler.start()

"""
with cron
year (int|str) – 4-digit year

month (int|str) – month (1-12)

day (int|str) – day of month (1-31)

week (int|str) – ISO week (1-53)

day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)

hour (int|str) – hour (0-23)

minute (int|str) – minute (0-59)

second (int|str) – second (0-59)

start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)

end_date (datetime|str) – latest possible date/time to trigger on (inclusive)

timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
#trigger=CronTrigger(hour='23', minute='05')
jitter (int|None) – delay the job execution by jitter seconds at mos


"""