import base64
import hashlib
import random
import re
import time
import struct
import numpy as np
from animation import interpolate_with_bezier
import random_strings

animation_indexes = [
    "M 10,30 C 6,183 122,77 109,2 h 110 s 222,93 148,1 C 69,39 84,87 104,151 h 83 s 183,66 34,171 C 83,176 56,9 85,93 h 205 s 33,234 127,160 C 183,132 239,111 149,158 h 155 s 12,206 44,113 C 48,137 198,185 161,118 h 165 s 15,203 156,87 C 121,223 109,63 167,100 h 59 s 209,183 249,25 C 110,121 87,29 139,192 h 64 s 215,141 206,63 C 91,186 247,241 121,159 h 61 s 116,52 212,53 C 156,21 206,140 138,121 h 210 s 0,134 111,184 C 157,138 57,185 248,28 h 74 s 56,14 112,129 C 228,106 190,210 156,101 h 243 s 28,127 0,55 C 59,168 120,239 193,233 h 114 s 128,105 213,4 C 96,26 223,25 192,36 h 89 s 221,76 212,13 C 149,243 102,38 143,240 h 20 s 54,24 174,118 C 186,65 84,168 141,123 h 177 s 16,59 19,175 C 94,63 89,25 20,153 h 109 s 159,192 70,42",
    "M 10,30 C 55,137 111,103 225,230 h 117 s 146,151 10,191 C 24,92 165,130 208,102 h 222 s 81,134 114,29 C 71,232 15,23 93,39 h 215 s 204,207 33,190 C 205,181 220,38 84,255 h 83 s 195,121 213,209 C 171,218 254,68 148,78 h 91 s 160,158 173,186 C 252,120 66,214 36,62 h 180 s 60,50 61,57 C 212,187 255,174 38,23 h 215 s 122,250 47,99 C 18,27 96,44 15,150 h 94 s 154,19 21,132 C 74,227 242,14 77,58 h 90 s 43,223 210,21 C 120,4 11,251 187,179 h 225 s 108,108 109,33 C 12,198 4,204 71,199 h 167 s 218,42 215,244 C 5,253 100,70 46,202 h 38 s 104,176 174,75 C 160,160 32,67 254,87 h 210 s 51,201 224,98 C 171,44 22,233 230,29 h 131 s 182,238 110,219 C 129,243 156,208 94,153 h 119 s 28,96 228,161 C 206,203 29,91 246,102 h 136 s 95,94 77,36",
    "M 10,30 C 117,233 35,159 77,147 h 233 s 183,11 126,141 C 192,84 121,200 145,203 h 114 s 236,19 10,27 C 230,9 214,10 97,9 h 246 s 206,144 162,249 C 42,166 220,204 4,90 h 85 s 47,118 58,162 C 80,186 88,52 159,91 h 104 s 114,8 99,170 C 80,18 90,215 51,53 h 84 s 218,11 3,61 C 96,48 200,79 73,185 h 229 s 143,6 230,214 C 167,199 150,93 30,231 h 167 s 56,206 108,135 C 63,83 161,91 18,116 h 109 s 166,236 80,234 C 72,149 55,10 225,177 h 139 s 38,10 174,28 C 132,72 70,32 29,108 h 192 s 53,142 217,84 C 179,243 76,8 36,193 h 189 s 236,27 205,166 C 38,31 96,92 181,5 h 70 s 232,54 8,64 C 244,156 107,121 218,43 h 44 s 216,194 43,142 C 241,20 163,129 170,11 h 76 s 30,86 206,192 C 40,106 82,239 89,186 h 216 s 146,130 46,146",
    "M 10,30 C 166,42 227,2 154,136 h 13 s 146,89 226,74 C 67,78 215,238 36,139 h 79 s 109,179 138,138 C 192,125 135,192 191,245 h 41 s 213,184 88,41 C 31,172 223,138 139,86 h 6 s 32,229 124,162 C 74,206 100,253 75,244 h 96 s 131,3 174,95 C 79,46 82,157 2,175 h 211 s 167,110 70,50 C 127,238 222,74 5,173 h 82 s 202,104 41,3 C 114,24 201,178 52,49 h 189 s 69,253 84,152 C 182,198 62,23 214,72 h 62 s 101,172 129,162 C 231,21 4,146 123,6 h 94 s 225,234 19,163 C 160,68 109,163 211,20 h 47 s 235,248 46,138 C 54,116 199,225 60,203 h 63 s 218,148 135,68 C 251,131 39,70 171,4 h 218 s 174,221 6,49 C 255,22 103,34 85,98 h 244 s 175,23 21,228 C 226,37 117,128 199,92 h 149 s 95,118 125,159 C 251,125 66,112 4,247 h 213 s 14,216 109,200"
]

def create_o(r):
    number = int(r)
    byte_array = struct.pack('I', number)
    byte_list = list(byte_array)
    return byte_list
def Mu(W):
    xored_total_list = []

    counter = 0
    for _ in W:


        if counter == 0:

            counter += 1
            xored_total_list.append(_)
        else:
            x = _ ^ W[0]
            xored_total_list.append(x)

    return xored_total_list
def FloatToHex(number, base = 16):

    if 0 == int(str(number).split('.')[1]):
        fixed_number = f"{number:.2f}"

        number_float = float(fixed_number)

        hexadecimal_string = format(int(number_float), 'x')
        return hexadecimal_string


    if number < 0:
        sign = "-"
        number = -number
    else:
        sign = ""

    s = [sign + str(int(number)) + '.']
    number -= int(number)

    for i in range(base):
        y = int(number * 16)
        s.append(hex(y)[2:])
        number = number * 16 - y

    return ''.join(s).rstrip('0')
def hexcalc(n):
    return "{:02x}".format(n)
def calculator(n, t, W):
    return round((n * (W - t) / 255 + t), 2)

def create_x_client_transaction_id(value_from_page, endpoint, method):

    #---------------------first parameters---------------------#
    current_time_ms = int(time.time() * 1000)
    r = int((current_time_ms - 1682924400000) / 1000) # return async (n, t)  const r
    o = create_o(r) # const o

    decoded_bytes = base64.b64decode(value_from_page)
    u = [byte for byte in decoded_bytes] # const u


    #---------------------first parameters---------------------#


    # ---------------------animation generation---------------------#
    animation_index = u[5] % 4

    stringo = animation_indexes[animation_index]

    stringo = stringo[9:]
    stringo = stringo.split("C")

    t = u[38] % 16 #  if (!Au) const [t,W]
    w = (u[43] % 16) * (u[0] % 16) * (u[9] % 16) #  if (!Au) const [t,W]

    list_all = []
    for i in stringo:
        i = re.sub(r'[^\d]+', ' ', i)
        i = i.strip()
        i = i.split(" ")

        z = []
        for _ in i:
            z.append(int(_))

        list_all.append(z)

    # ---------------------cubic bezier algo---------------------#
    z = list_all[t] #  if (!Au) { , z =

    get_rotate = z[6]

    rotate_angle = int(get_rotate * (360 - 60) / 255 + 60)

    color_hexcodes = ["#" + hexcalc(z[0]) + hexcalc(z[1]) + hexcalc(z[2]),  "#" + hexcalc(z[3]) + hexcalc(z[4]) + hexcalc(z[5])]

    calclist = z[7:]
    l = 0
    f = []
    for _ in calclist:
        if l % 2:
            val = -1
        else:
            val = 0

        l += 1

        f.append(calculator(_, val, 1))
    easing = f'cubic-bezier({f[0]},{f[1]},{f[2]},{f[3]})'

    bezier_points = (f[0], f[1], f[2], f[3])
    time_value = round((w / 10)) * 10
    degree = int(rotate_angle)
    start_hex = str(color_hexcodes[0])
    end_hex = str(color_hexcodes[1])


    print("rotate_angle:", f"rotate({rotate_angle}deg)")
    print("color", color_hexcodes)
    print("bezier_points", bezier_points)
    print("time_value", time_value)

    # ---------------------cubic bezier algo---------------------#

    result = interpolate_with_bezier(bezier_points, time_value, start_hex, end_hex, degree)
    interpolated_color_rgb = result["interpolated_color_rgb"]
    rotation_matrix = result["rotation_matrix"]
    print("Interpolated Color RGB:", interpolated_color_rgb)
    print("Rotation Matrix:", rotation_matrix)

    animation_result = f"{interpolated_color_rgb}{rotation_matrix}"

    # ---------------------animation generation---------------------#

    matches = re.findall(r'([\d.-]+)', animation_result)
    last_response = []
    for number in matches:
        number = float(number)
        number = round(number, 2)
        last_response.append(FloatToHex(number))

    c = "".join(last_response)
    c = re.sub(r"[.-]", "", c)

    to_decode = f"{method}!{endpoint}!{r}obfiowerehiring{c}"

    # to_decode = 'POST!/1.1/jot/client_event.json!46988559obfiowerehiring97a2a8091eb851eb851e80d1eb851eb851e80d1eb851eb851e8091eb851eb851e800'

    print("to_decode:", to_decode)
    sha256_hash = hashlib.sha256(to_decode.encode()).digest()
    uint_array = np.frombuffer(sha256_hash, dtype=np.uint8).tolist()
    uint_array = uint_array[:16]
    print("uint_array:", uint_array)



    random_num = [int((str(random.random() * 256)).split('.')[0])]

    total = random_num + u + o + uint_array + [3]

    # total = [145,4,149,57,191,214,188,177,137,105,183,15,149,212,70,249,153,73,121,142,53,185,8,198,24,106,223,160,223,241,207,167,22,32,14,17,6,145,86,22,143,9,87,72,197,205,47,41,153,178,7,205,2,139,39,196,195,215,210,109,252,152,191,164,141,113,245,145,236,3]
    print("total:", total)
    xored_total_list = Mu(total)
    print("xored_total_list:", xored_total_list)

    byte_string = bytes(xored_total_list)

    encoded_string = base64.b64encode(byte_string).decode('utf-8').replace('=', '')

    return encoded_string


"""test code
value_from_page = 'd2D8zx/Nm0CbMRrr1Ujy+wCKkfyhM/UwYUTKu1GPyLM+49B2kzVxWoDjMasGkKN5'#example
endpoint = 'POST'#example
method = '/1.1/jot/client_event.json'#example
print(value_from_page)
print(endpoint)
print(method)
print(create_x_client_transaction_id(value_from_page, endpoint, method))"""


