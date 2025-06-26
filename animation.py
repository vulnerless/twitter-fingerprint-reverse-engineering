import math

class CubicBezierExactMatch:
    def __init__(self, curves):
        self.curves = curves

    def get_value(self, time):
        if time <= 0.0:
            return self.calculate_start_gradient() * time

        if time >= 1.0:
            return 1.0 + self.calculate_end_gradient() * (time - 1.0)

        start, end = 0.0, 1.0
        precision = 1e-14
        max_iterations = 10000
        iterations = 0

        while end - start > precision and iterations < max_iterations:
            mid = (start + end) / 2
            x_est = self.f(self.curves[0], self.curves[2], mid)
            if abs(time - x_est) < precision:
                return self.f(self.curves[1], self.curves[3], mid)
            if x_est < time:
                start = mid
            else:
                end = mid
            iterations += 1

        return self.f(self.curves[1], self.curves[3], (start + end) / 2)

    def calculate_start_gradient(self):
        if self.curves[0] > 0.0:
            return self.curves[1] / self.curves[0]
        elif self.curves[1] == 0.0 and self.curves[2] > 0.0:
            return self.curves[3] / self.curves[2]
        return 0.0

    def calculate_end_gradient(self):
        if self.curves[2] < 1.0:
            return (self.curves[3] - 1.0) / (self.curves[2] - 1.0)
        elif self.curves[2] == 1.0 and self.curves[0] < 1.0:
            return (self.curves[1] - 1.0) / (self.curves[0] - 1.0)
        return 0.0

    @staticmethod
    def f(a, b, m):
        return 3.0 * a * (1 - m) ** 2 * m + 3.0 * b * (1 - m) * m ** 2 + m ** 3

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate_color(start_color, end_color, cubic_value):
    return tuple(
        max(0, min(255, round(start + (end - start) * cubic_value)))
        for start, end in zip(start_color, end_color)
    )

def exact_rotation_matrix(degrees):
    radians = degrees * math.pi / 180.0
    c = math.cos(radians)
    s = math.sin(radians)
    return [round(c, 10), round(s, 10), round(-s, 10), round(c, 10), 0, 0]

def format_rotation_matrix(matrix):
    return f"matrix({matrix[0]:.6f}, {matrix[1]:.6f}, {matrix[2]:.6f}, {matrix[3]:.6f}, {matrix[4]}, {matrix[5]})"

def interpolate_with_bezier(bezier_points, time_value, start_hex, end_hex, degree):
    time_value = time_value / 4096  
    cubic_curve = CubicBezierExactMatch(bezier_points)
    cubic_value = cubic_curve.get_value(time_value)
    
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    interpolated_rgb = interpolate_color(start_rgb, end_rgb, cubic_value)
    interpolated_hex = rgb_to_hex(interpolated_rgb)
    
    start_deg, end_deg = 0, degree
    degrees = start_deg + (end_deg - start_deg) * cubic_value
    rotation_matrix = exact_rotation_matrix(degrees)
    formatted_matrix = format_rotation_matrix(rotation_matrix)
    
    return {
        "interpolated_color_rgb": interpolated_rgb,
        "interpolated_color_hex": interpolated_hex,
        "rotation_matrix": formatted_matrix
    }

""" test code
bezier_points = (0.57,-0.30,0.89,-0.42)
time_value = 210
start_hex = "#a62ae3"
end_hex = "#029a88"
degree = 75

result = interpolate_with_bezier(bezier_points, time_value, start_hex, end_hex, degree)
print("Interpolated Color RGB:", result["interpolated_color_rgb"])
print("Rotation Matrix:", result["rotation_matrix"])

print("Interpolated Color HEX:", result["interpolated_color_hex"])"""