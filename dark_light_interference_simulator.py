import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Define spatial range
x = np.linspace(-5, 5, 1000)

# Bright and dark state wavefunctions
def psi_bright(x, d=1.0, sigma=0.5):
    return np.exp(-((x - d)**2) / (2 * sigma**2))

def psi_dark(x, d=1.0, sigma=0.5):
    return np.exp(-((x + d)**2) / (2 * sigma**2))

# Superposition of bright and dark components
def total_wavefunction(x, alpha=1/np.sqrt(2), beta_mag=1/np.sqrt(2), beta_phase=0.0):
    beta = beta_mag * np.exp(1j * beta_phase)
    return alpha * psi_bright(x) + beta * psi_dark(x)

# Calculate observable intensity
def intensity(x, alpha, beta_mag, beta_phase):
    psi = total_wavefunction(x, alpha, beta_mag, beta_phase)
    return np.abs(psi)**2

# Plot setup
fig, ax = plt.subplots()
line, = ax.plot(x, intensity(x, 1/np.sqrt(2), 1/np.sqrt(2), 0.0))
ax.set_ylim(0, 2)
ax.set_xlim(-5, 5)
ax.set_title("Interference Pattern with Varying Phase of Dark State")
ax.set_xlabel("Position (x)")
ax.set_ylabel("Intensity")

# Animation update function
def update(frame):
    phase = 2 * np.pi * frame / 100
    y = intensity(x, 1/np.sqrt(2), 1/np.sqrt(2), phase)
    line.set_ydata(y)
    ax.set_title(f"Dark Phase = {phase:.2f} rad")
    return line,

# Animate
ani = FuncAnimation(fig, update, frames=100, interval=100)

# Save as GIF (uncomment below to export)
# ani.save("interference_dark_phase.gif", writer=PillowWriter(fps=10))

plt.show()
