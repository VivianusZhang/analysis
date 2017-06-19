from crontab import CronTab

cron   = CronTab(user = True)

job = cron.new(command = 'python instrumentDailyData.py')
job.minute.on(0, 30)
job.hour.on(1,2,3,4,5,6,7,8,9,10)
job.day.on(1, 2, 3, 4, 5)

cron.write()
