from time import perf_counter as pc

import matplotlib.pyplot as plt
import numpy as np

from tiffcomposer.core.coordinates import GeoCoordinate

# Define the starting coordinate
start_coord = GeoCoordinate(0, 0)

# Define a range of latitudes for the other coordinate
latitudes = np.linspace(0, 90, 100)

# Calculate distances for different step values
distances_step_0 = []
distances_step_5 = []
distances_step_10 = []
distances_step_25 = []
distances_step_50 = []
distances_step_100 = []

for lat in latitudes:
    end_coord = GeoCoordinate(lat, 0)
    distances_step_0.append(start_coord.distance_to(end_coord, step=0))
    distances_step_5.append(start_coord.distance_to(end_coord, step=5))
    distances_step_10.append(start_coord.distance_to(end_coord, step=10))
    distances_step_25.append(start_coord.distance_to(end_coord, step=25))
    distances_step_50.append(start_coord.distance_to(end_coord, step=50))
    distances_step_100.append(start_coord.distance_to(end_coord, step=100))

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(latitudes, distances_step_0, label='Step = 0')
plt.plot(latitudes, distances_step_5, label='Step = 5')
plt.plot(latitudes, distances_step_10, label='Step = 10')
plt.plot(latitudes, distances_step_25, label='Step = 25')
plt.plot(latitudes, distances_step_50, label='Step = 50')
plt.plot(latitudes, distances_step_100, label='Step = 100')
plt.xlabel('Latitude')
plt.ylabel('Distance (meters)')
plt.title('Distance between coordinates with varying steps')
plt.legend()
plt.grid(True)
plt.show()

# Measure execution times for different step values
times_step_0 = []
times_step_5 = []
times_step_10 = []
times_step_25 = []
times_step_50 = []
times_step_100 = []

for lat in latitudes:
    end_coord = GeoCoordinate(lat, 0)

    start_time = pc()
    start_coord.distance_to(end_coord, step=0)
    times_step_0.append(pc() - start_time)

    start_time = pc()
    start_coord.distance_to(end_coord, step=5)
    times_step_5.append(pc() - start_time)

    start_time = pc()
    start_coord.distance_to(end_coord, step=10)
    times_step_10.append(pc() - start_time)

    start_time = pc()
    start_coord.distance_to(end_coord, step=25)
    times_step_25.append(pc() - start_time)

    start_time = pc()
    start_coord.distance_to(end_coord, step=50)
    times_step_50.append(pc() - start_time)

    start_time = pc()
    start_coord.distance_to(end_coord, step=100)
    times_step_100.append(pc() - start_time)

# Plot the execution times
plt.figure(figsize=(10, 6))
plt.plot(latitudes, times_step_0, label='Step = 0')
plt.plot(latitudes, times_step_5, label='Step = 5')
plt.plot(latitudes, times_step_10, label='Step = 10')
plt.plot(latitudes, times_step_25, label='Step = 25')
plt.plot(latitudes, times_step_50, label='Step = 50')
plt.plot(latitudes, times_step_100, label='Step = 100')
plt.xlabel('Latitude')
plt.ylabel('Execution Time (seconds)')
plt.title('Execution Time for Distance Calculation with Varying Steps')
plt.legend()
plt.grid(True)
raise ValueError()

plt.show()
