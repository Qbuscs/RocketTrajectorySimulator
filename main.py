import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox
import datetime
import sys

from utils import *
from rocket import *
from vector3d import Vector3D


# ================ MISSION PLAN ================
mission_years = 2
mission_days = mission_years*365 + 0
mission_hours = mission_days*24 + 0
mission_minutes = mission_hours * 60 + 0

sim_time = mission_minutes

takeoff = datetime.timedelta(days=1) # 25.01

burns = {
    # minute: (direction, seconds)
    # possible directions: prograde, retrograde, radial_in, radial_out, normal, antinormal
    118500: ("retrograde", 250),
    208780: ("retrograde", 180),
}

# ================ DRAW SIZE ====================
draw_dim = 5    # 33 for total

# ================ PLANETS INFO =================
# in kg
masses = {
    "Mercury": 3301.e20,
    "Venus": 4867.e21,
    "Earth": 5972.e21,
    "Mars": 6414.e20,
    "Jupiter": 1898.e24,
    "Saturn": 5683.e23,
    "Uranus": 8681.e22,
    "Neptune": 1024.e23,
    "Pluto": 1303.e19,
    "Ceres": 9400.e17,
    "Eris": 1647.e19,
    "Sun": 1988.e27
}

# in AU
sizes = {
    "Mercury": m_to_AU(2440 * 1000),
    "Venus": m_to_AU(6052 * 1000),
    "Earth": m_to_AU(6380 * 1000),
    "Mars": m_to_AU(3390 * 1000),
    "Jupiter": m_to_AU(69911 * 1000),
    "Saturn": m_to_AU(58232 * 1000),
    "Uranus": m_to_AU(25362 * 1000),
    "Neptune": m_to_AU(24622 * 1000),
    "Pluto": m_to_AU(1188 * 1000),
    "Ceres": m_to_AU(469 * 1000),
    "Eris": m_to_AU(1163 * 1000),
    "Sun": m_to_AU(695700 * 1000)
}

# =============== PLANET LOAD =====================

print("Loading planets data...")
planets_total = get_planets(sim_time, takeoff)
print("Done.")

earth_v = earth_speed(planets_total[0]["Earth"])

# ================ ROCKET PARAMETERS ==============
start_pos = Vector3D(
        planets_total[0]["Earth"][0],
        planets_total[0]["Earth"][1] + m_to_AU(1000 * (6380 + 20000)), # Earth high orbit
        planets_total[0]["Earth"][2]
)
start_vel = Vector3D(10000 + earth_v[0], 8000 + earth_v[1], 0)
fuel = 8e4 # 4e3
mass = 4e3
engine_thrust = 6e5 # 6e4
engine_isp = 345
rocket = Rocket(start_pos, start_vel, fuel, mass, engine_thrust, engine_isp)
print(f"Fuel consumption: {round(rocket._fuel_consumption, 3)} kg/s")
print(f"Burn time available: {int(rocket.remaining_burn_time())} s")
rocket.set_planets_info(masses=masses, sizes=sizes)

# ================== FLIGHT ========================

print("Simulating flight...")
try:
    burns = split_burns(burns)
except ValidationError:
    print("ERROR: Planed burnes interlap with eachother")
    sys.exit(1)
rocket_x = [rocket.pos.x]
rocket_y = [rocket.pos.y]
tenth = int(sim_time/10)
for i in range(0, sim_time):
    if i % tenth == 0:
        print(f"{10 * i / tenth}%...")
    planets = {}
    planets["Sun"] = Vector3D(0, 0, 0)
    for key in planets_total[i]:
        planets[key] = Vector3D( planets_total[i][key][0], planets_total[i][key][1], planets_total[i][key][2] )
    rocket.set_planets_info(positions=planets)

    if not rocket.apply_forces():
        print(f"{i} minutes - BOOM!")
        sim_time = i + 1
        break

    if i in burns:
        print("\t---------------------------------------------------------------")
        print(f"\tMinute {i}: Initiating {burns[i][0]} burn for {burns[i][1]} s")
        feedback = rocket.burn(burns[i][0], burns[i][1])
        if feedback is not None:
            print(f"\tBurn reduced to {round(feedback, 1)} s due to lack of fuel")
        print(f"\tRemaining burn time available: {round(rocket.remaining_burn_time(), 1)}")

    rocket.move()
    rocket_x.append(rocket.pos.x)
    rocket_y.append(rocket.pos.y)

print("Done.")

# ====================== DRAW =========================

plt.figure(figsize=(9,9))
ax = plt.gca()

slider_ax = plt.axes([0.11, 0.05, 0.8, 0.02])
input_ax = plt.axes([0.81, 0.02, 0.1, 0.02])
slider_time = Slider(slider_ax, "Minute", 0, sim_time-1, valinit=0, valstep=1)
input_time = TextBox(input_ax, "", initial="0")

def draw(time):
    planets = planets_total[time]
    rocket_pos = (rocket_x[time], rocket_y[time])

    ax.cla() # clear things for fresh plot
    ax.set_xlim((-draw_dim, draw_dim))
    ax.set_ylim((-draw_dim, draw_dim))
    ax.plot(0,0,'.', label='Sun')
    ax.add_artist(plt.Circle((0, 0), sizes["Sun"], fill=True))
    for key in planets:
        x = planets[key][0]
        y = planets[key][1]
        size = sizes[key]
        ax.plot(x, y, '.', markersize=10, label=key)
        ax.add_artist(plt.Circle((x, y), size, fill=True))
        ax.add_artist(plt.Circle((0, 0), ((abs(x)**2+abs(y)**2)**0.5), color='r', fill=False))
    ax.legend(loc='upper center', bbox_to_anchor=(1.05, 1.0))
    ax.plot(rocket_x, rocket_y, "g")
    ax.plot(rocket_pos[0], rocket_pos[1], "^g")

def update_slider(val):
    input_time.set_val(val)
    draw(val)
slider_time.on_changed(update_slider)

def update_input(val):
    val_int = 0
    try:
        val_int = int(val)
    except ValueError:
        input_time.set(slider_time.val)
        return
    if val_int < 0:
        val_int = 0
    if val_int > sim_time-1:
        val_int = sim_time-1
    slider_time.set_val(val_int)
    draw(val_int)
input_time.on_submit(update_input)

draw(0)


plt.show()
