import datetime

class GetHolidaysUsecase:
    def execute(self):
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        weekends = []
        weekdays_jp = ['月', '火', '水', '木', '金', '土', '日']
        for i in range(7):
            current_day = monday + datetime.timedelta(days=i)
            if current_day.weekday() >= 5:  # 土曜(5) or 日曜(6)
                formatted = current_day.strftime("%m/%d") + f"({weekdays_jp[current_day.weekday()]})"
                weekends.append(formatted)
        return weekends