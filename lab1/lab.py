# -*- coding: cp1251 -*-
import math, sys

def rk4(f1, f2, h, t0, u0, w0):

    t = t0
    u = u0
    w = w0

    x = 0
    y = 0

    #ymax = 0

    while y >= 0:
        k1 = h * f1(t, u, w)
        l1 = h * f2(t, u, w)

        k2 = h * f1(t + 0.5*h, u + 0.5*k1, w + 0.5 * l1)
        l2 = h * f2(t + 0.5*h, u + 0.5*k1, w + 0.5 * l1)

        k3 = h * f1(t + 0.5*h, u + 0.5*k2, w + 0.5 * l2)
        l3 = h * f2(t + 0.5*h, u + 0.5*k2, w + 0.5 * l2)

        k4 = h * f1(t + h, u + k3, w + l3)
        l4 = h * f2(t + h, u + k3, w + l3)

        u += (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0
        w += (l1 + 2.0*l2 + 2.0*l3 + l4) / 6.0
        t += h

        x += h * u
        y += h * w

        #ymax = max(ymax, y)

        #print u, w, x, y

    return x#, ymax

def galiley(v0, a0):

    g = 9.8

    x = (v0**2 / g) * math.sin(2*a0)
    #y = v0**2 * (math.sin(a0) ** 2) / (2 * g) 

    return x#, y

def newton(v0, a0, r, p_sh, h):

    g   = 9.8
    c_2 = 0.15
    p_v = 1.29

    #V   = 4 * math.pi * r**3 / 3
    #S   = 4 * math.pi * r**2
    #m   = p_sh * V
    #b   = c_2 * S * p_v

    b_m = - 3 * c_2 * p_v / (p_sh * r)

    def du(t, u, w):
        return b_m * u * math.sqrt(u**2 + w**2) 

    def dw(t, u, w):
        return -g + b_m * w * math.sqrt(u**2 + w**2)

    x1 = rk4(du, dw, h, 0, v0*math.cos(a0), v0*math.sin(a0))

    b_m = 0
    x2  = rk4(du, dw, h, 0, v0*math.cos(a0), v0*math.sin(a0))

    return x1, x2

def print_format(type, x):

    name = "Галилею" if not type else \
           "Ньютону с учётом сопротивления воздуха" if type == 1 else \
           "Ньютону без учёта сопротивления воздуха"
    print   "По %s:\n"\
            "    расстояние до места падения - {:.4f}м".format(x) % name

def main():

    v0 = 50
    a0 = math.pi/4
    r  = 0.1
    p  = 11300
    h = float(sys.argv[1])

    x_gal = galiley(v0, a0)

    x_new, x_0 = newton(v0, a0, r, p, h)

    print_format(0, x_gal)
    print_format(1, x_new)
    print_format(2, x_0)

main()