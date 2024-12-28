import numpy as np
import base64, os
import math
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor

FORMULA = None

#parse 
def parse_formula(formula_str):
    """
    Create a lambda function for the user-defined recursive formula.
    The formula must use `z` and `c` as variables.
    Example input: "z**2 + c" mandelbrot
    """
    try:
        global FORMULA
        
        allowed_globals = {
        '__builtins__': {},  # Disable dangerous built-ins
        'z': None,
        'c': None,
        'sin': math.sin,        
        'cos': math.cos,
        'pi': math.pi
        }

        FORMULA = eval(f"lambda z, c: {formula_str}", allowed_globals) #lambda function! in python syntax is : lambda variables : expression
    except Exception as e:
        raise ValueError(f"Invalid formula: {e}")

#error in computation in think? sometype of overflow
def calculate_fractal_chunk(start_row, end_row, real, imag, div_bound, max_itr):
    '''
    int, int, arr, arr, lambda func, int, int -> arr (calculated chunk)
    '''
    esc_times = np.zeros((end_row - start_row, len(real)), dtype=int)
    #print(len(esc_times), len(esc_times[0]))

    #for each pixel given in bounds, iterate through formula and check if diverges
    for i in range(start_row, end_row):
        for r in range(len(esc_times[0])):
            z = 0
            c = real[r] + imag[i] * 1j #j is imag dtype 
            itr = 0
            while itr < max_itr and abs(z) < div_bound:
                z = FORMULA(z, c)
                if np.isnan(z.real) or np.isnan(z.imag) or np.isinf(z.real) or np.isinf(z.imag):
                    print(f"Overflow at z = {z}, c = {c}")
                    break
                itr += 1
            esc_times[i - start_row, r] = itr 

    return start_row, end_row, esc_times

    
#generate the fractal:
def generate_fractal(formula_str, width, height, div_bound, real_bound, imag_bound, max_itr):
    parse_formula(formula_str) #function

    real = np.linspace(real_bound[0], real_bound[1], width) # evenly spaced list from lower to upper bound w/width# values
    imag = np.linspace(imag_bound[0], imag_bound[1], height) # imaginary part on vertical axis
    esc_times = np.zeros((height, width), dtype=int) #record escape times in num itrs for colors, rc major

    num_workers = os.cpu_count()
    #print(num_workers)
    row_chunks = np.array_split(np.arange(height), num_workers) #designates chunks of rows for each cpu
    #print(row_chunks)

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        #divide by rows, len(esc_times) = #rows 
        #each worker gets #rows/#cpus rows
        futures = [
            executor.submit(calculate_fractal_chunk, chunk[0], chunk[-1] + 1, real, imag, div_bound, max_itr)
            for chunk in row_chunks
        ]
        for future in futures:
            start, end, esc = future.result()
            esc_times[start:end, :] = esc
                
    
    #plotting
    plt.figure(figsize=(12, 12))
    plt.imshow(esc_times, cmap="inferno", extent=(real_bound[0], real_bound[1], imag_bound[0], imag_bound[1]))
    plt.colorbar(label="Escape Time", shrink=.5)
    plt.title(f"Fractal: {formula_str}")

    # Save the image to a BytesIO object and convert to base64
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return img_str
            
