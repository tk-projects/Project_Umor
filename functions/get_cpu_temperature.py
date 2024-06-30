import subprocess

def get_cpu_temperature():
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temperature_str = result.stdout.strip()
    temperature = float(temperature_str.split('=')[1].split("'")[0])
    return temperature

# Example usage
temperature = get_cpu_temperature()
print(f"CPU Temperature: {temperature} °C")