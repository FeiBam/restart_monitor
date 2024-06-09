# utils.py
import calendar
import datetime
from Types.restart_time_setting_t import restart_time_setting_t

def calculate_next_restart_time(settings: restart_time_setting_t, current_time=None):
    if current_time is None:
        current_time = datetime.datetime.now()

    #print(f"Current time: {current_time}")

    # 设置基本时间到今天的某个时间
    next_run = current_time.replace(second=settings.second, microsecond=0)

    # 如果给定了分钟数，设置分钟
    next_run = next_run.replace(minute=settings.minute)

    # 如果给定了小时数，设置小时
    next_run = next_run.replace(hour=settings.hour)

    #print(f"Initial next_run: {next_run}")

    # 处理天数，月数和星期
    if settings.month != 0 and settings.day != 0:
        next_run = next_run.replace(month=settings.month, day=settings.day)
        #print(f"Next run after setting month and day: {next_run}")
        if next_run <= current_time:
            try:
                next_run = next_run.replace(year=next_run.year + 1)
            except ValueError:
                next_run = next_run.replace(year=next_run.year + 1, month=1, day=1)
        #print(f"Next run adjusted for month and day: {next_run}")
    elif settings.day != 0:
        next_run = next_run.replace(day=settings.day)
        #print(f"Next run after setting day: {next_run}")
        if next_run <= current_time:
            # 调整到下个月
            year = next_run.year
            month = next_run.month + 1
            if month > 12:
                month = 1
                year += 1
            try:
                next_run = next_run.replace(year=year, month=month, day=settings.day)
            except ValueError:
                # 处理无效日期（例如 2 月 30 日）
                while True:
                    try:
                        next_run = datetime.datetime(year, month, settings.day, settings.hour, settings.minute, settings.second)
                        break
                    except ValueError:
                        month += 1
                        if month > 12:
                            month = 1
                            year += 1
        #print(f"Next run adjusted for day: {next_run}")
    elif settings.weekly != 0:
        weekly = (settings.weekly - 1) % 7  # 将1-7映射到0-6
        days_ahead = (weekly - next_run.weekday() + 7) % 7
        if days_ahead == 0 and next_run < current_time:
            days_ahead = 7
        next_run += datetime.timedelta(days=days_ahead)
        #print(f"Next run after setting weekly: {next_run}")
    elif settings.month != 0:
        month = settings.month
        if next_run.month > month or (next_run.month == month and next_run <= current_time):
            next_run = next_run.replace(year=next_run.year + 1, month=month, day=1)
        else:
            next_run = next_run.replace(month=month, day=1)
        #print(f"Next run after setting month: {next_run}")
        while next_run <= current_time:
            try:
                next_run = next_run.replace(month=next_run.month + 1)
            except ValueError:
                next_run = next_run.replace(year=next_run.year + 1, month=1)
            #print(f"Next run adjusted for month: {next_run}")
        next_run = next_run.replace(day=settings.day if settings.day != 0 else 1)
        #print(f"Next run final adjustment for month: {next_run}")
    else:
        if next_run <= current_time:
            next_run += datetime.timedelta(days=1)
        #print(f"Next run adjusted for daily: {next_run}")

    return next_run.timestamp()
