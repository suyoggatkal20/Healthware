import datetime
from django.utils import timezone
import pytz


def validate_appo(str_rep, appointment_start, duration):
    start = appointment_start
    appointment_start = appointment_start.replace(second=0, microsecond=0)
    tz = pytz.timezone('Asia/Kolkata')
    today = tz.localize(datetime.datetime.now()).replace(
        hour=0, minute=0, second=0, microsecond=0)
    slot_start = int((appointment_start-today).total_seconds()//60)
    slot_end = int((appointment_start-today+duration).total_seconds()//60)
    for i in range(slot_start, slot_end+1):
        if str_rep[i] != 0:
            return False
    return True


def get_str_rep(doctor):
    """
    0 time out of clinic
    B time in clinic but doctor on break
    A appointment set
    """
    from calendar import monthrange
    from accounts.models import Break
    from appointment.models import Appointment
    from accounts.serializers import BreakSerializer
    from appointment.serializers import AppointmentSerializer
    start = doctor.start_time
    end = doctor.end_time
    duration = doctor.appoinment_duration
    str_rep = "0"*24*60*7
    tz = pytz.timezone('Asia/Kolkata')
    today = tz.localize(datetime.datetime.now()).replace(
        hour=0, minute=0, second=0, microsecond=0)
    break_qs = Break.objects.filter(
        doctor=doctor, time_start__gte=today, time_end__lte=today+datetime.timedelta(days=7))
    appo_qs = Appointment.objects.filter(
        doctor=doctor, time_start__gte=today, time_start__lte=today+datetime.timedelta(days=7))
    # breaks = BreakSerializer(
    #     break_qs, fields=['time_start', 'time_end', 'repeat'], many=True).data
    # breaks = BreakSerializer(
    #     data=breaks, fields=['time_start', 'time_end', 'repeat'], many=True)
    # appos = AppointmentSerializer(
    #     appo_qs, fields=['time_start'], many=True).data
    # appos = AppointmentSerializer(
    #     data=appos, fields=['time_start'], many=True)
    duration_repete = datetime.timedelta(days=1).total_seconds()//60
    clinic_end = (today.replace(
        hour=end.hour, minute=end.minute)-today).total_seconds()//60-1
    clinic_start = (today.replace(hour=start.hour,
                    minute=start.minute)-today).total_seconds()//60-1
    str_rep = str_replace(str_rep, 0, int(clinic_start), '-')
    for i in range(6):
        str_rep = str_replace(str_rep, int(
            i*duration_repete+clinic_end), int((i+1)*duration_repete+clinic_start), '-')
    str_rep = str_replace(str_rep, int(
        6*duration_repete+clinic_end), len(str_rep)-1, '-')
    for i, break_ in enumerate(break_qs):
        print('processing break :', i)
        if break_.repeat == 'N':
            # is_valid = is_valid_break(start, end, break_)
            # if not is_valid:
            #     return False
            if break_.start_time.date() < today.date():
                print('break creation problem')
                print('skipped sice it is old break')
                print(break_.start_time.date())
                print(break_.end_time.date())
                continue
            slot_start = (break_.start_time-today).total_seconds()//60
            slot_end = (break_.end_time-today).total_seconds()//60
            str_rep = str_replace(str_rep, int(slot_start), int(slot_end), 'b')
            continue
        if break_.repeat == "D":
            # is_valid = is_valid_break(start, end, break_)
            # if not is_valid:
            #     return False
            duration_repete = datetime.timedelta(days=1).total_seconds()//60
            slot_start = (break_.time_start.replace(
                year=today.year, month=today.month, day=today.day)-today).total_seconds()//60

            slot_end = (break_.time_end.replace(
                day=today.day, month=today.month, year=today.year)-today).total_seconds()//60
            for i in range(7):
                str_rep = str_replace(str_rep, int(
                    i*duration_repete+slot_start), int(i*duration_repete+slot_end), 'b')
        if break_.repeat == "W":
            # is_valid = is_valid_break(start, end, break_)
            # if not is_valid:
            #     return False
            days_from_today = (
                (7+break_.time_start.weekday()-today.weekday()) % 7)
            print('days_from_today', days_from_today)
            duratio_from_today = datetime.timedelta(
                days=days_from_today).total_seconds()//60
            print('duratio_from_today', duratio_from_today)
            slot_start = (break_.time_start.replace(
                year=today.year, day=today.day, month=today.month)-today).total_seconds()//60
            print('slot_start', slot_start)
            slot_end = (break_.end_time.replace(
                day=today.day, month=today.month, year=today.year)-today).total_seconds()//60
            print('slot_end', slot_end)
            str_rep = str_replace(str_rep, int(
                duratio_from_today+slot_start),  int(duratio_from_today+slot_end), 'b')
            continue
        if break_.repeat == "M":
            # is_valid = is_valid_break(start, end, break_)
            # if not is_valid:
            #     return False
            try:
                break_start = break_.start_time.replace(
                    year=today.year, month=today.month)
                break_end = break_.end_time.replace(
                    year=today.year, month=today.month)
            except:
                print('break creation problem')
                print('current month does not have specified date')
                continue
            print(break_end.date())
            print((today+datetime.timedelta(days=7)).date())
            if today.date() > break_start.date() and break_start.date() < (today+datetime.timedelta(days=7)).date():
                print('skipped this break because it is not part of comming week')
                continue
            slot_start = (break_start-today).total_seconds()//60
            slot_end = (break_end-today).total_seconds()//60
            print(slot_start, slot_end)
            str_rep = str_replace(str_rep, int(slot_start), int(slot_end), 'b')
    for i, appo in enumerate(appo_qs):
        print('processing appo :', i)
        appo.time_start = appo.time_start.replace(
            second=0, microsecond=0)
        if appo.time_start.date() < today.date() or appo.time_start.date() > (today+datetime.timedelta(days=7)).date():
            print('appo creation problem')
            print('old oopo')
            print(appo.time_start.date())
            continue
        slot_start = (appo.time_start-today).total_seconds()//60
        slot_end = (appo.time_start-today+duration).total_seconds()//60
        str_rep = str_replace(str_rep, int(slot_start), int(slot_end), 'a')
        continue
    return str_rep


def is_valid_break(start, end, break_):
    # if break_['start_time'].date() != break_['end_time'].date():
    #     print('break creation problem')
    #     print('break date is not matching')
    #     print(break_['start_time'].date())
    #     print(break_['end_time'].date())
    #     return False
    # if break_['start_time'].date() > (timezone.now()+datetime.timedelta(days=7)).date():
    #     print('break creation problem')
    #     print('future break')
    #     print(break_['start_time'].date())
    #     print(break_['end_time'].date())
    #     return False
    # if break_['start_time'] > break_['end_time'] or break_['start_time'].time() < start or break_['end_time'].time() > end:
    #     print('break creation problem')
    #     print('invalid break start time must be bigger than end time')
    #     print('break must be set between clinic time')
    #     print(break_['start_time'])
    #     print(break_['end_time'])
    #     print(break_['start_time'].time())
    #     print(start)
    #     print(break_['end_time'].time())
    #     print(end)
    #     print('invalid break')
    #     return False
    return True


def check_break(str_rep, start, end, repete):
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    today = tz.localize(datetime.datetime.now()).replace(
        hour=0, minute=0, second=0, microsecond=0)
    mnc = (start.replace(day=today.day, month=today.month, year=today.year)-today)
    start_min = int((start.replace(day=today.day, month=today.month,
                    year=today.year)-today).total_seconds()//60)
    end_min = int((end.replace(day=today.day, month=today.month,
                  year=today.year)-today).total_seconds()//60)
    repete_duration = int(datetime.timedelta(days=1).total_seconds()//60)
    if repete == 'D':
        for i in range(7):
            for j in range(start_min, end_min+1):
                asx = str_rep[i*repete_duration+j]
                if str_rep[i*repete_duration+j] != '0' and str_rep[i*repete_duration+j].lower() != 'b':
                    print("i j", i, j, start_min, end_min, i*repete_duration+j)
                    return False
    else:
        for j in range(start_min, end_min+1):
            if str_rep[start_min+j] != '0' and str_rep[start_min+j].lower() != 'b':
                return False
    return True


def str_replace(str_rep, start, end, key):
    list_rep = list(str_rep)
    list_rep[start+1:end] = [key]*(end-start-1)
    list_rep[start] = key.upper()
    list_rep[end] = key.upper()
    return "".join(list_rep)


def str_to_slots(str_rep, appointment_duration):
    l = list()
    today = datetime.datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0)
    i = 0
    print(appointment_duration)
    duration_counter = int(appointment_duration.total_seconds()//60)
    print(duration_counter)
    add_in_break = False

    while i < len(str_rep):
        if i == 470:
            print('n')
        if str_rep[i] == '0':
            duration_counter = int(appointment_duration.total_seconds()//60)
            temp = i
            while i < len(str_rep) and duration_counter > 0 and str_rep[i] == '0':
                i += 1
                duration_counter -= 1
            print(temp, i, duration_counter)
#             print('dc',duration_counter)
            if duration_counter == 0:
                empty_slot = {}
                empty_slot['type'] = 'E'
                empty_slot['start_index'] = today + \
                    datetime.timedelta(minutes=temp)
                empty_slot['end_index'] = today+datetime.timedelta(minutes=i-1)
                l.append(empty_slot)
                duration_counter = int(
                    appointment_duration.total_seconds()//60)
            elif duration_counter >= 1:
                if (i == len(str_rep) or str_rep[i] == 'A' or str_rep[i] == '-'):
                    break_ = {}
                    break_['type'] = 'B'
                    break_['start_index'] = today + \
                        datetime.timedelta(minutes=temp)
                    break_['end_index'] = today+datetime.timedelta(minutes=i-1)
                    l.append(break_)
                    duration_counter = int(
                        appointment_duration.total_seconds()//60)
                elif str_rep[i] == 'B':
                    add_in_break = True
                    duration_counter = int(
                        appointment_duration.total_seconds()//60)
            continue
#         print('dsuj',i,len(str_rep))
        if (i == 0 or str_rep[i-1] != str_rep[i] or str_rep[i-1] == 'B') and str_rep[i] == 'B':
            break_ = {}
            break_['type'] = 'B'
            if add_in_break:
                break_['start_index'] = today+datetime.timedelta(minutes=temp)
                add_in_break = False
            else:
                break_['start_index'] = today+datetime.timedelta(minutes=i)
            while i < len(str_rep) and str_rep[i].lower() == 'b':
                i += 1
            i -= 1
            break_['end_index'] = today+datetime.timedelta(minutes=i)
            l.append(break_)
        if (i == 0 or str_rep[i-1] != str_rep[i]) and str_rep[i] == 'A':
            appo = {}
            appo['type'] = 'A'
            appo['start_index'] = today+datetime.timedelta(minutes=i)
            appo['end_index'] = today + \
                datetime.timedelta(minutes=str_rep.index('A', i+1))
            i = str_rep.index('A', i+1)
            l.append(appo)
        i += 1
    for item in l:
        if item['type'] == 'B':
            print('***********************Break**********************************')
            print(item['start_index'])
            print(item['end_index'])
            print()
            print()
        if item['type'] == 'A':
            print('***********************Appointment**********************************')
            print(item['start_index'])
            print(item['end_index'])
            print()
            print()
        if item['type'] == 'E':
            print('***********************Empty**********************************')
            print(item['start_index'])
            print(item['end_index'])
            print()
            print()
    return l


if __name__ == '__main__':
    appointment_data = {
        "start_time": datetime.datetime.strptime("2021-06-24 08:40:00", "%Y-%m-%d %H:%M:%S").time(),
        "end_time": datetime.datetime.strptime("2021-06-24 18:40:00", "%Y-%m-%d %H:%M:%S").time(),
        "appoinment_duration": datetime.timedelta(minutes=30),
        "breaks": [
            {
                "start_time": datetime.datetime.strptime("2000-06-30 13:40:00", "%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.datetime.strptime("2000-06-30 14:20:00", "%Y-%m-%d %H:%M:%S"),
                "repete": "M",
                "reason": "jdncdsm",
            },
            {
                "start_time": datetime.datetime.strptime("2021-06-28 16:30:00", "%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.datetime.strptime("2021-06-28 17:20:00", "%Y-%m-%d %H:%M:%S"),
                "repete": "N",
                "reason": "jdncdsm",
            },
            {
                "start_time": datetime.datetime.strptime("2020-07-02 09:30:00", "%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.datetime.strptime("2020-07-02 17:30:00", "%Y-%m-%d %H:%M:%S"),
                "repete": "N",
                "reason": "jdncdsm",
            },
            {
                "start_time": datetime.datetime.strptime("2020-07-01 12:30:00", "%Y-%m-%d %H:%M:%S"),
                "end_time": datetime.datetime.strptime("2020-07-01 17:15:00", "%Y-%m-%d %H:%M:%S"),
                "repete": "N",
                "reason": "jdncdsm",
            }
        ],
        "appointment": [
            {
                "time_start": datetime.datetime.strptime("2021-06-29 17:30:00", "%Y-%m-%d %H:%M:%S"),
            },
            {
                "time_start": datetime.datetime.strptime("2021-06-30 15:30:00", "%Y-%m-%d %H:%M:%S")
            },
            {
                "time_start": datetime.datetime.strptime("2021-07-02 12:30:00", "%Y-%m-%d %H:%M:%S")
            },
            {
                "time_start": datetime.datetime.strptime("2021-07-02 09:30:00", "%Y-%m-%d %H:%M:%S")
            }
        ]
    }
    asd = get_str_rep(appointment_data)
    str_to_slots(asd, datetime.timedelta(minutes=30))


# import time
# import datetime
# import pytz

# def get_str_rep(data):
#     """
#     0 time out of clinic
#     1 time in clinic but doctor on break
#     2 appointment set
#     """
#     from calendar import monthrange
#     start=data['clinic_start']
#     end=data['clinic_end']
#     du=data['duration']
#     str_rep="0"*24*60*7
#     breaks=data['breaks']
#     appos=data['appointment']
#     for i,break_ in enumerate(breaks):
#         print('processing break :',i)
#         break_['time_start']=break_['time_start'].replace(second=0,microsecond=0)
#         break_['time_start']=break_['time_start'].replace(second=0,microsecond=0)
#         if break_['repete']=='N':
#             is_valid=is_valid_break(start,end,du,break_)
#             if is_valid=='CON':
#                 continue
#             if not is_valid:
#                 return False
#             if break_['time_start'].date()<datetime.datetime.now().date():
#                 print('break creation problem')
#                 print('old break')
#                 print(break_['time_start'].date())
#                 print(break_['time_end'].date())
#                 continue
#             slot_start=(break_['time_start']-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             slot_end=(break_['time_end']-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             str_rep=str_rep_fun(str_rep,int(slot_start),int(slot_end),'1')
#             continue
#         if break_['repete']=="D":
#             is_valid=is_valid_break(start,end,du,break_)
#             if is_valid=='CON':
#                 continue
#             if not is_valid:
#                 return False
#             today=datetime.date.today()
#             duration_repete=datetime.timedelta(days=1).total_seconds()//60
#             slot_start=(break_['time_start'].replace(day=today.day,month=today.month,year=today.year)-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             slot_end=(break_['time_end'].replace(day=today.day,month=today.month,year=today.year)-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             for i in range(7):
#                 str_rep=str_rep_fun(str_rep, int(i*duration_repete+slot_start), int(i*duration_repete+slot_end), '1')
#         if break_['repete']=="W":
#             is_valid=is_valid_break(start,end,du,break_)
#             if is_valid=='CON':
#                 continue
#             if not is_valid:
#                 return False
#             today=datetime.date.today()
#             days_from_today=((7+break_['time_start'].weekday()-today.weekday())%7);
#             print('days_from_today',days_from_today)
#             duratio_from_today=datetime.timedelta(days=days_from_today).total_seconds()//60
#             print('duratio_from_today',duratio_from_today)
#             slot_start=(break_['time_start'].replace(year=today.year,day=today.day,month=today.month)-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             print('slot_start',slot_start)
#             slot_end=(break_['time_end'].replace(day=today.day,month=today.month,year=today.year)-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             print('slot_end',slot_end)
#             str_rep=str_rep_fun(str_rep, int(duratio_from_today+slot_start),  int(duratio_from_today+slot_end), '1')
#             continue
#         if break_['repete']=="M":
#             is_valid=is_valid_break(start,end,du,break_)
#             if is_valid=='CON':
#                 continue
#             if not is_valid:
#                 return False
#             today=datetime.datetime.now()
#             try:
#                 break_start = break_['time_start'].replace(year=today.year,month=today.month,second=0,microsecond=0)
#                 break_end = break_['time_end'].replace(year=today.year,month=today.month,second=0,microsecond=0)
#             except:
#                 print('break creation problem')
#                 print('current month does not have specified date')
#                 continue
#             slot_start = (break_start-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             slot_end = (break_end-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#             print(slot_start,slot_end)
#             str_rep = str_rep_fun(str_rep, int(slot_start), int(slot_end), '1')
#     for i,appo in enumerate(appos):
#         print('processing appo :', i)
#         appo['start_time'] = appo['start_time'].replace(second=0, microsecond=0)
#         if appo['start_time'].date() < datetime.datetime.now().date() or appo['start_time'].date() > (datetime.datetime.now()+datetime.timedelta(days=7)).date():
#             print('appo creation problem')
#             print('old oopo')
#             print(appo['start_time'].date())
#             continue
#         slot_start = (appo['start_time']-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()//60
#         slot_end = (appo['start_time']-datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+datetime.timedelta(minutes=du)).total_seconds()//60
#         str_rep = str_rep_fun(str_rep,int(slot_start),int(slot_end),'2')
#         continue
#     return str_rep

# appointment_data = {
#         "clinic_start": datetime.datetime.strptime("2021-06-24 08:40:00","%Y-%m-%d %H:%M:%S").time(),
#         "clinic_end": datetime.datetime.strptime("2021-06-24 18:40:00","%Y-%m-%d %H:%M:%S").time(),
#         "duration": 30,
#         "breaks": [
#             {
#                 "time_start": datetime.datetime.strptime("2000-06-25 13:40:00","%Y-%m-%d %H:%M:%S"),
#                 "time_end": datetime.datetime.strptime("2000-06-25 14:20:00","%Y-%m-%d %H:%M:%S"),
#                 "repete": "M",
#                 "reason": "jdncdsm",
#             },
#             {
#                 "time_start": datetime.datetime.strptime("2021-06-27 16:30:00","%Y-%m-%d %H:%M:%S"),
#                 "time_end": datetime.datetime.strptime("2021-06-27 17:20:00","%Y-%m-%d %H:%M:%S"),
#                 "repete": "N",
#                 "reason": "jdncdsm",
#             },
#             {
#                 "time_start": datetime.datetime.strptime("2020-06-15 09:30:00","%Y-%m-%d %H:%M:%S"),
#                 "time_end": datetime.datetime.strptime("2020-06-15 19:30:00","%Y-%m-%d %H:%M:%S"),
#                 "repete": "N",
#                 "reason": "jdncdsm",
#             },
#             {
#                 "time_start": datetime.datetime.strptime("2020-06-19 05:30:00","%Y-%m-%d %H:%M:%S"),
#                 "time_end": datetime.datetime.strptime("2020-06-19 19:15:00","%Y-%m-%d %H:%M:%S"),
#                 "repete": "N",
#                 "reason": "jdncdsm",
#             }
#         ],
#     "appointment": [
#             {
#                 "start_time": datetime.datetime.strptime("2021-06-25 17:30:00","%Y-%m-%d %H:%M:%S"),
#             },
#             {
#                 "start_time": datetime.datetime.strptime("2021-06-25 15:30:00","%Y-%m-%d %H:%M:%S")
#             },
#             {
#                 "start_time": datetime.datetime.strptime("2021-06-28 12:30:00","%Y-%m-%d %H:%M:%S")
#             },
#             {
#                 "start_time": datetime.datetime.strptime("2021-06-20 09:30:00","%Y-%m-%d %H:%M:%S")
#             }
#         ]
#  }

# def is_valid_break(start,end,du,break_):
#     if break_['time_start'].date()!=break_['time_end'].date():
#         print('break creation problem')
#         print('break date is not matching')
#         print(break_['time_start'].date())
#         print(break_['time_end'].date())
#         return 'RET';
#     if break_['time_start'].date()>(datetime.datetime.now()+datetime.timedelta(days=7)).date():
#         print('break creation problem')
#         print('future break')
#         print(break_['time_start'].date())
#         print(break_['time_end'].date())
#         return 'CON'
#     if break_['time_start']>break_['time_end'] or break_['time_start'].time()<start or break_['time_end'].time()>end:
#         print('break creation problem')
#         print('invalid break')
#         print(break_['time_start'])
#         print(break_['time_end'])
#         print(break_['time_start'].time())
#         print(start)
#         print(break_['time_end'].time())
#         print(end)
#         print('invalid break')
#         return 'RET';
#     return True


# def str_rep_fun(str_rep,start,end,key):
#     list_rep=list(str_rep)
#     list_rep[start:end+1]=[key]*(end-start+1)
#     return "".join(list_rep)


# def str_to_slots(str_rep):
#     l=list()
#     today=datetime.datetime.today().replace(hour=0,minute=0,second=0,microsecond=0)
#     for i in range(len(str_rep)):
#         if (i==0 or str_rep[i-1]!=str_rep[i]) and str_rep[i]=='1':
#             break_={}
#             break_['type']='B'
#             break_['start_index']=today+datetime.timedelta(minutes=i)
#         if (i!=0 and str_rep[i]!=str_rep[i-1] and str_rep[i-1]=='1'):
#             break_['end_index']=today+datetime.timedelta(minutes=i-1)
#             l.append(break_)
#         if i==len(str_rep)-1 and str_rep[i]=='1':
#             break_['end_index']=today+datetime.timedelta(minutes=i)
#             l.append(break_)
#         if (i==0 or str_rep[i-1]!=str_rep[i]) and str_rep[i]=='2':
#             appo={}
#             appo['type']='A'
#             appo['start_index']=today+datetime.timedelta(minutes=i)
#         if (i!=0 and str_rep[i]!=str_rep[i-1] and str_rep[i-1]=='2'):
#             appo['end_index']=today+datetime.timedelta(minutes=i-1)
#             l.append(appo)
#         if i==len(str_rep)-1 and str_rep[i]=='2':
#             appo['end_index']=today+datetime.timedelta(minutes=i)
#             l.append(appo)
#     for item in l:
#         if item['type']=='B':
#             print('***********************Break**********************************')
#             print(item['start_index'])
#             print(item['end_index'])
#             print()
#             print()
#         if item['type']=='A':
#             print('***********************Appointment**********************************')
#             print(item['start_index'])
#             print(item['end_index'])
#             print()
#             print()

# if __name__=='__main__':
#     asd=get_str_rep(appointment_data)
#     print(str_to_slots(asd))
