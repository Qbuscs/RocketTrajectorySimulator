from utils import *
from vector3d import Vector3D
from math import log


class Rocket:
    def __init__(self, position, velocity, fuel, mass, engine_thrust, Isp):
        self.pos = position
        self.vel = velocity
        self.fuel = fuel
        self.mass = mass
        self.engine_thrust = engine_thrust
        self.Isp = Isp
        self._fuel_consumption = self.engine_thrust / ( self.Isp * 9.81 )
        self.interval = "Minutes"
        self._g_force = None
    
    def total_mass(self):
        return self.mass + self.fuel
    
    def remaining_burn_time(self):
        return self.fuel / self._fuel_consumption
    
    def set_planets_info(self, masses=None, sizes=None, positions=None):
        if masses:
            self.p_masses = masses
        if sizes:
            self.p_sizes = sizes
        if positions:
            self.p_positions = positions
    
    def move(self):
        step = {
            "Hours": 3600,
            "Minutes": 60
        }
        
        a = self._g_force / self.total_mass()
        self.vel += a * step[self.interval]

        delta_pos = self.vel * step[self.interval]
        self.pos += delta_pos.apply(m_to_AU)
    
    def apply_forces(self):
        F = Vector3D(0.0, 0.0, 0.0)
        G = 66743.e-15
        step = {
            "Hours": 3600,
            "Minutes": 60
        }
        boom = False

        for planet in self.p_positions:
            planet_pos =self.p_positions[planet]
            planet_size = self.p_sizes[planet]
            planet_mass = self.p_masses[planet]

            d = self.pos.distance(planet_pos)
            if d < planet_size:
                boom = True
            F_val = (G * self.total_mass() * planet_mass) / ( AU_to_m(d) ** 2)
            F += F_val * (planet_pos - self.pos) / d

        self._g_force = F
        return not boom
    
    def _burn_prograde(self, delta_v):
        self.vel += self.vel.normal() * delta_v
    
    def _burn_retrograde(self, delta_v):
        self.vel -= self.vel.normal() * delta_v
    
    def _burn_normal(self, delta_v):
        self.vel += self.vel.crossproduct(self._g_force).normal() * delta_v

    def _burn_antinormal(self, delta_v):
        self.vel -= self.vel.crossproduct(self._g_force).normal() * delta_v
    
    def _burn_radial_in(self, delta_v):
        self.vel += self._g_force.normal() * delta_v
    
    def _burn_radial_out(self, delta_v):
        self.vel -= self._g_force.normal() * delta_v
        
    def burn(self, direction, burn_time):
        feedback = None
        time = min(burn_time, 60, self.remaining_burn_time())
        if time == self.remaining_burn_time():
            feedback = self.remaining_burn_time()
        if time <= 0:
            return 0
        delta_v = (self.engine_thrust / self._fuel_consumption) * (
            log(abs(-self.mass - self.fuel)) - log(abs(-self.mass - self.fuel + self._fuel_consumption * time))
        )
        self.fuel -= time * self._fuel_consumption

        burn_type = {
            "prograde": self._burn_prograde,
            "retrograde": self._burn_retrograde,
            "normal": self._burn_normal,
            "antinormal": self._burn_antinormal,
            "radial_in": self._burn_radial_in,
            "radial_out": self._burn_radial_out
        }
        burn_type[direction](delta_v)
        return feedback