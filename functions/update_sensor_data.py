def update_sensor_data(sensors):
    try:
        # Fetch sensor readings
        sensor_readings = {}
        for sensor in sensors:
            try:
                sensor_readings[sensor.name] = sensor.read()
            except Exception as e:
                print(f"Error reading sensor {sensor.name}: {e}")
                sensor_readings[sensor.name] = 0.0

    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return sensor_readings