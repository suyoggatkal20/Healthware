from datetime import datetime, timedelta

appointment_data = {
    "clinic_start_time": "09:30:00",
    "clinic_end_time": "19:20:00",
    "appointment_duration": 30,

    "list_of_breaks": [
        {
            "break_start_time": "2021-06-13 13:40:00",
            "break_end_time": "2021-06-13 14:20:00",
            "repete on": "Y"
        },
        {
            "break_start_time": "2021-06-13 17:30:00",
            "break_end_time": "2021-06-13 18:20:00",
            "repete on": "Y"
        },
        {
            "break_start_time": "2021-06-15 09:30:00",
            "break_end_time": "2021-06-15 19:30:00",
            "repete on": "N"
        },
        {
            "break_start_time": "2021-06-19 05:30:00",
            "break_end_time": "2021-06-19 19:15:00",
            "repete on": "N"
        }
    ],

    "list_of_booked_appointment": [
        {
            "appointment_start_time": "2021-06-14 17:30:00"
        },
        {
            "appointment_start_time": "2021-06-15 15:30:00"
        },
        {
            "appointment_start_time": "2021-06-13 12:30:00"
        },
        {
            "appointment_start_time": "2021-06-19 09:30:00"
        }
    ]
}


def appoint(app):
    st = datetime.strptime(app["clinic_start_time"], '%Y/%d/%m %H:%M:%S')
    et = datetime.strptime(app["clinic_end_time"], '%Y/%d/%m %H:%M:%S')
    st.replace(second=0, microsecond=0)
    et.replace(second=0, microsecon=0)
    st = st.strftime("%H/%M/%S")
    et = et.strftime("%H/%M/%S")

    d = app["appointment_duration"]
    start_date = datetime.now().date()
    end_date = datetime.now().date() + timedelta(days=6)
    days = {}
    date = start_date

    while date <= end_date:
        hours = {}
        ms = date.strftime("%Y/%d/%m") + " " + st
        me = date.strftime("%Y/%d/%m") + " " + et
        time = datetime.strptime(ms, '%Y/%d/%m %H:%M:%S')
        end = datetime.strptime(me, '%Y/%d/%m %H:%M:%S')
        while time <= end:
            avail = "A"
            res = ""
            d = app["appointment_duration"]
            for i in app["list_of_breaks"]:
                sb = datetime.fromisoformat(i["break_start_time"])
                bd = datetime.fromisoformat(i["break_end_time"]) - sb
                if (time.strftime("%Y/%d/%m") == sb.strftime("%Y/%d/%m")) & (
                        time.strftime("%H/%M/%S") == sb.strftime("%H/%M/%S")):
                    avail = "O"
                    res = i["reason"]
                    d = bd.total_seconds() / 60

                elif (time.strftime("%Y/%d/%m") == sb.strftime("%Y/%d/%m")) & ((sb - time).total_seconds() > 0) & (
                        (sb - time).total_seconds() / 60 < d):
                    avail = "O"
                    res = i["reason"]
                    d = (sb - time).total_seconds() / \
                        60 + bd.total_seconds() / 60

            for i in app["list_of_booked_appointment"]:
                sa = datetime.fromisoformat(i["appointment_start_time"])
                if time.strftime("%Y/%d/%m" "%H/%M/%S") == sa.strftime("%Y/%d/%m" "%H/%M/%S"):
                    avail = "B"
                    res = i["reason"]
                else:
                    pass

                hours[time.strftime("%H:%M:%S")] = [avail, res]
            time += timedelta(minutes=d)
        days[date.strftime("%Y/%d/%m")] = hours
        date += timedelta(days=1)

        for i in app["list_of_breaks"]:
            if i["repete on"] == "Y":
                i["break_start_time"] = (datetime.fromisoformat(
                    i["break_start_time"])+timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
                i["break_end_time"] = (datetime.fromisoformat(
                    i["break_end_time"]) + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

    print(days)
    return days


if __name__ == '__main__':
    appoint(appointment_data)
