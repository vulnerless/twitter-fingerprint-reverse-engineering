# Twitter/X `x-client-transaction-id` Generation in Python

This repository contains a Python implementation for generating the `x-client-transaction-id` HTTP header, which is used by X (formerly Twitter) in their internal API calls.

> **Important Notice**
>
> If Twitter is not happy about this repository, please contact me via email address in my profile instead of sending a DMCA takedown. This project is for educational and research purposes only.
>
> *(All work done in this repository was for my own learning purposes.)*

## Overview

The main purpose of this project is to replicate the logic that generates a transaction ID. This ID is a complex value derived from various inputs, including a seed value from the page, the API endpoint, the HTTP method, and the current time. The original logic is found in obfuscated JavaScript on the X website. This repository represents a complete port of that logic to Python.

The generation process is highly intricate and involves two main stages:
1.  **Animation Simulation (`animation.py`):** A sophisticated animation is simulated based on parameters derived from a seed value. This involves calculating a precise point on a cubic-Bézier curve, interpolating colors, and generating a 2D rotation matrix.
2.  **Transaction ID Assembly (`transaction.py`):** The result of the animation simulation is serialized, combined with request-specific data (method, endpoint, timestamp), and then hashed. This hash is packaged with other data into a byte array, which is then obfuscated and Base64 encoded to produce the final header value.

## The Porting Process: From JavaScript to Python

The original implementation is a piece of heavily obfuscated JavaScript. The process of creating this Python version involved several key steps:

1.  **De-obfuscation:** The first step was to analyze and de-obfuscate the obfuscated JavaScript code to understand its underlying algorithm. This meant tracing function calls, renaming cryptic variables, and documenting the flow of data.

2.  **Mathematical Replication:** The JavaScript code relies on browser-native or library-based functionalities for complex calculations. A significant part of this project was replicating them in Python using mathematical principles.
    *   **Cubic-Bézier Curves:** The most challenging part was replicating the Bézier curve calculation. While JavaScript can use CSS easing functions, Python has no such native equivalent. The `CubicBezierExactMatch` class in `animation.py` was built from scratch. It uses a **binary search algorithm** to find the parametric value `t` that corresponds to a given `x` (time) on the curve, achieving a high degree of precision (`1e-14`). This was crucial for matching the output of the original script.
    *   **Matrix Transformations:** The 2D rotation matrix is calculated using standard trigonometric functions (`sin`, `cos`) from Python's `math` library. This calculation directly implements the mathematical logic behind the CSS `matrix()` transform function.

3.  **Byte-Level Manipulation:** The script performs several low-level operations on byte arrays. These were ported using Python's `struct` for packing numbers into bytes and native list operations for array manipulation.

## File Breakdown

### `animation.py` - The Animation Engine

This module is a self-contained engine for calculating the state of a complex animation at a specific point in time. It does not perform any actual rendering; instead, it generates the *values* that would be used in a CSS animation.

-   `CubicBezierExactMatch`:
    -   Takes four control points `(x1, y1, x2, y2)` that define a cubic-Bézier curve.
    -   The `get_value(time)` method solves the Bézier equation for `y` given an `x` (`time`). Since this cannot be solved algebraically, it uses an iterative binary search to find the correct point on the curve with extreme precision.
    -   It also handles time values outside the `[0.0, 1.0]` range by linearly extrapolating from the curve's start and end gradients.

-   **Color and Rotation Functions:**
    -   `hex_to_rgb` / `rgb_to_hex`: Standard color format converters.
    -   `interpolate_color`: Performs a linear interpolation between two RGB colors. The interpolation factor is the `y` value returned by the `CubicBezierExactMatch` class.
    -   `exact_rotation_matrix`: Creates a 2D rotation matrix for a given angle in degrees.

-   **Main Function: `interpolate_with_bezier`**
    -   This function orchestrates the entire animation simulation. It takes the Bézier control points, a time value, start/end colors, and a rotation angle.
    -   It scales the input time (`time_value / 4096`), gets the animation progress from the Bézier curve, and uses this progress value to calculate the final interpolated color and the CSS-formatted rotation matrix.

### `transaction.py` - Header Generation Logic

This is the main script that uses the animation engine to construct the final `x-client-transaction-id` header.

The `create_x_client_transaction_id` function follows these steps:

1.  **Initialization:** It takes a Base64-encoded `value_from_page` (a seed), the `endpoint` URL, and the `method` (e.g., 'POST'). It decodes the seed into a byte array (`u`) and calculates a relative timestamp (`r`).

2.  **Parameter Derivation:** It uses specific bytes from the seed array `u` to derive all parameters for the animation simulation. This includes:
    -   Selecting one of the hardcoded SVG path strings from `animation_indexes`.
    -   Parsing this string to extract color values, a rotation angle, and the four control points for the cubic-Bézier curve.
    -   Calculating a `time_value` for the simulation.

3.  **Animation Simulation:** It calls `interpolate_with_bezier` from `animation.py` with the derived parameters. This returns an interpolated color and a rotation matrix string.

4.  **Fingerprint Creation:** The numeric parts of the animation result are extracted, converted to hexadecimal, and concatenated into a single string (`c`). This string acts as a dynamic "fingerprint" of the client environment simulation.

5.  **Hashing:** A unique string is constructed using the format: `f"{method}!{endpoint}!{r}obfiowerehiring{c}"`. This string is then hashed using **SHA-256**, and the first 16 bytes of the digest are kept. The `obfiowerehiring` part is a static salt from the original script.

6.  **Payload Assembly & Obfuscation:**
    -   A final byte array is assembled from a random byte, the seed array `u`, the timestamp bytes `o`, the 16-byte hash, and a static trailer byte.
    -   This entire array is passed through the `Mu` function, which performs a simple XOR obfuscation (each byte is XORed with the first byte of the array).

7.  **Final Encoding:** The resulting obfuscated byte array is **Base64 encoded** (with padding removed) to create the final `x-client-transaction-id` string.

## How to Use

To generate a transaction ID, you need three pieces of information:

1.  `value_from_page`: A Base64 string obtained from the X website. This value changes and acts as a seed.
2.  `endpoint`: The API endpoint you are targeting (e.g., `/1.1/jot/client_event.json`).
3.  `method`: The HTTP method for the request (e.g., `POST`).

```python
import transaction

# These values must be obtained from the target environment
value_from_page = 'd2D8zx/Nm0CbMRrr1Ujy+wCKkfyhM/UwYUTKu1GPyLM+49B2kzVxWoDjMasGkKN5'
endpoint = '/1.1/jot/client_event.json'
method = 'POST'

# Generate the header
transaction_id = transaction.create_x_client_transaction_id(
    value_from_page, 
    endpoint, 
    method
)

print(f"Generated x-client-transaction-id: {transaction_id}")
```

## Dependencies

-   `numpy`