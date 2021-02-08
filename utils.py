import datetime
import pickle
import solarsystem
from math import sqrt
from recordtype import recordtype


Planet = recordtype("Planet", "pos name")

class PickleTooShortException(Exception):
    pass

class ValidationError(Exception):
    pass

def AU_to_m(AU):
    return AU * 1495979.e5
    

def m_to_AU(m):
    return m / 1495979.e5

def earth_speed(earth_pos):
    # 110,000 km/h =~ 30,555 m/s
    v = 30555
    x = earth_pos[0]
    y = earth_pos[1]
    vx = v * abs(y)
    vy = v * abs(x)
    if x >= 0 and y >= 0:
        return (-vx, vy)
    if x >= 0 and y < 0:
        return (vx, vy)
    if x < 0 and y >= 0:
        return (-vx, -vy)
    return (vx, -vy)

def now_parts(now):
    year   = now.year
    month  = now.month
    day    = now.day
    hour   = now.hour
    minute = now.minute
    return year, month, day, hour, minute

def get_planets(val, takeoff):
    try:
        pickle_in = open("planets.pickle", "rb")
        planets = pickle.load(pickle_in)
        if len(planets) < val:
            raise PickleTooShortException
        return planets
    except (PickleTooShortException, FileNotFoundError) as e:
        planets = generate_planets(val, takeoff)
        pickle_out = open("planets.pickle", "wb")
        pickle.dump(planets, pickle_out)
        return planets

def generate_planets(val, takeoff):
    now    = datetime.datetime.now(datetime.timezone.utc) + takeoff
    UT     = 0
    dst = 0
    planets = []
    tenth = int(val/10)
    for i in range(0, val):
        if i % tenth == 0:
            print(f"{int(10 * i / tenth)}%...")
        year, month, day, hour, minute = now_parts(now)
        H = solarsystem.Heliocentric(
            year=year, month=month, day=day, hour=hour, minute=minute, 
            UT=UT, dst=dst, view='rectangular'
        )
        _planets = H.planets()
        _planets.pop("Chiron")
        planets.append(_planets)
        now += datetime.timedelta(minutes=1)
    return planets

def validate_burns(burns):
    for time in burns:
        if burns[time][1] < 60:
            continue
        for i in range(1, int(burns[time][1] / 60) + 1):
            if (time + i) in burns:
                raise ValidationError

def split_burns(burns):
    validate_burns(burns)
    split_burns = {}
    for time in burns:
        if burns[time][1] < 60:
            split_burns[time] = burns[time]
            continue
        remaining_burn = burns[time][1]
        this_burn_time = time
        while(remaining_burn):
            split_burns[this_burn_time] = (burns[time][0], min(remaining_burn, 60))
            remaining_burn -= min(remaining_burn, 60)
            this_burn_time += 1
    return split_burns


