import numpy as np

class ProportionalController:
    def __init__(self, kp, setpoint):
        self.kp = kp
        self.setpoint = setpoint
    
    def update(self, measured_value):
        error = self.setpoint - measured_value
        output = self.kp * error
        return output, error

# Simulation parameters
dt = 1  # Time step
time = np.arange(0, 10, dt)  # Simulation time

# System parameters
setpoint = 10  # Desired position
initial_position = 0  # Initial position

# Proportional controller parameters
kp = 0.1


# Initialize Proportional controller
controller = ProportionalController(kp, setpoint)

# Initial condition
position = initial_position

# Simulation loop
print(f"{'Time':<10} {'Position':<15} {'Error':<15} {'Control Output':<15}")
for t in time:
    # Calculate control output
    control_output, error = controller.update(position)
    
    # Update position (simple model: position += control_output * dt)
    position += control_output * dt
    
    # Print data
    print(f"{t:<10.2f} {position:<15.2f} {error:<15.2f} {control_output:<15.2f}")

# import matplotlib.pyplot as plt
# import numpy as np

# class ProportionalController:
#     def __init__(self, kp, setpoint):
#         self.kp = kp
#         self.setpoint = setpoint
    
#     def update(self, measured_value):
#         error = self.setpoint - measured_value
#         output = self.kp * error
#         return output, error

# # Simulation parameters
# dt = 1  # Time step
# time = np.arange(0, 10, dt)  # Simulation time

# # System parameters
# setpoint = 10  # Desired position
# initial_position = 0  # Initial position

# # Proportional controller parameters
# kp = 2

# # Initialize Proportional controller
# controller = ProportionalController(kp, setpoint)

# # Initialize lists for storing simulation data
# positions = []
# errors = []

# # Initial condition
# position = initial_position

# # Simulation loop
# print(f"{'Time':<10} {'Position':<15} {'Error':<15} {'Control Output':<15}")
# for t in time:
#     # Calculate control output
#     control_output, error = controller.update(position)
    
#     # Update position (simple model: position += control_output * dt)
#     position += control_output * dt
    
#     # Store data
#     positions.append(position)
#     errors.append(error)
    
#     # Print data
#     print(f"{t:<10.2f} {position:<15.2f} {error:<15.2f} {control_output:<15.2f}")

# # Plot results
# plt.figure(figsize=(12, 6))

# plt.subplot(2, 1, 1)
# plt.plot(time, positions, label='Position')
# plt.axhline(y=setpoint, color='r', linestyle='--', label='Setpoint')
# plt.title('1D Position Control System')
# plt.xlabel('Time [s]')
# plt.ylabel('Position')
# plt.legend()

# plt.subplot(2, 1, 2)
# plt.plot(time, errors, label='Error', color='orange')
# plt.xlabel('Time [s]')
# plt.ylabel('Error')
# plt.legend()

# plt.tight_layout()
# plt.show()
