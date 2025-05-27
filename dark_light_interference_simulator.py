import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.special import fresnel
import seaborn as sns

class PhotonDualitySimulator:
    """
    A comprehensive simulator for the bright/dark photon interference model.
    
    This class implements the theoretical framework where photons exist as
    superpositions of 'bright' (detectable) and 'dark' (undetectable) states,
    with interference arising from their interaction.
    """
    
    def __init__(self, x_range=(-10, 10), num_points=2000):
        self.x = np.linspace(x_range[0], x_range[1], num_points)
        self.setup_plotting_style()
    
    def setup_plotting_style(self):
        """Configure matplotlib style for publication-quality plots."""
        plt.style.use('dark_background')
        sns.set_palette("husl")
    
    def psi_bright(self, x, center=1.0, sigma=0.5, k=5.0):
        """
        Bright state wavefunction with optional momentum component.
        
        Args:
            x: spatial coordinate array
            center: peak position
            sigma: width parameter
            k: momentum (wave number)
        """
        envelope = np.exp(-((x - center)**2) / (2 * sigma**2))
        phase = np.exp(1j * k * x)
        return envelope * phase
    
    def psi_dark(self, x, center=-1.0, sigma=0.5, k=5.0):
        """
        Dark state wavefunction with optional momentum component.
        
        Args:
            x: spatial coordinate array
            center: peak position  
            sigma: width parameter
            k: momentum (wave number)
        """
        envelope = np.exp(-((x - center)**2) / (2 * sigma**2))
        phase = np.exp(1j * k * x)
        return envelope * phase
    
    def total_wavefunction(self, x, alpha=1/np.sqrt(2), beta_mag=1/np.sqrt(2), 
                          beta_phase=0.0, bright_params=None, dark_params=None):
        """
        Complete wavefunction as superposition of bright and dark states.
        
        Args:
            alpha: amplitude of bright component
            beta_mag: magnitude of dark component amplitude
            beta_phase: phase of dark component
            bright_params: dict of parameters for bright state
            dark_params: dict of parameters for dark state
        """
        bright_params = bright_params or {}
        dark_params = dark_params or {}
        
        beta = beta_mag * np.exp(1j * beta_phase)
        
        psi_b = self.psi_bright(x, **bright_params)
        psi_d = self.psi_dark(x, **dark_params)
        
        return alpha * psi_b + beta * psi_d
    
    def observable_intensity(self, x, alpha, beta_mag, beta_phase, 
                           detection_efficiency=1.0, **kwargs):
        """
        Calculate the observable intensity including detector efficiency.
        
        Args:
            detection_efficiency: fraction of bright photons detected
        """
        psi = self.total_wavefunction(x, alpha, beta_mag, beta_phase, **kwargs)
        base_intensity = np.abs(psi)**2
        
        # Only bright component contributes to detection
        bright_contribution = np.abs(alpha)**2
        observable_fraction = bright_contribution * detection_efficiency
        
        return base_intensity * observable_fraction
    
    def interference_visibility(self, intensity_profile):
        """Calculate fringe visibility: V = (I_max - I_min)/(I_max + I_min)"""
        I_max = np.max(intensity_profile)
        I_min = np.min(intensity_profile)
        return (I_max - I_min) / (I_max + I_min) if (I_max + I_min) > 0 else 0
    
    def decoherence_model(self, psi, decoherence_rate=0.1, time=1.0):
        """
        Apply decoherence to the wavefunction.
        
        Args:
            psi: input wavefunction
            decoherence_rate: rate of phase randomization
            time: evolution time
        """
        # Simple model: add random phase noise
        phase_noise = np.random.normal(0, decoherence_rate * time, len(psi))
        return psi * np.exp(1j * phase_noise)
    
    def double_slit_experiment(self, slit_separation=2.0, slit_width=0.3, 
                              screen_distance=10.0):
        """
        Simulate double-slit experiment with bright/dark formalism.
        
        Returns:
            dict with slit positions, interference pattern, and analysis
        """
        # Slit positions
        slit1_pos = -slit_separation / 2
        slit2_pos = slit_separation / 2
        
        # Path difference for each point on screen
        path_diff = np.sqrt((self.x - slit2_pos)**2 + screen_distance**2) - \
                   np.sqrt((self.x - slit1_pos)**2 + screen_distance**2)
        
        # Phase difference
        k = 2 * np.pi  # wavelength = 1
        phase_diff = k * path_diff
        
        # Bright and dark contributions through each slit
        bright_1 = np.exp(-((self.x - slit1_pos)**2) / (2 * slit_width**2))
        bright_2 = np.exp(-((self.x - slit2_pos)**2) / (2 * slit_width**2)) * \
                  np.exp(1j * phase_diff)
        
        dark_1 = np.exp(-((self.x - slit1_pos)**2) / (2 * slit_width**2)) * 0.7
        dark_2 = np.exp(-((self.x - slit2_pos)**2) / (2 * slit_width**2)) * \
                np.exp(1j * (phase_diff + np.pi/4)) * 0.7
        
        # Total wavefunctions
        psi_bright_total = (bright_1 + bright_2) / np.sqrt(2)
        psi_dark_total = (dark_1 + dark_2) / np.sqrt(2)
        
        # Combined wavefunction
        alpha, beta = 1/np.sqrt(2), 1/np.sqrt(2)
        psi_total = alpha * psi_bright_total + beta * psi_dark_total
        
        intensity = np.abs(psi_total)**2
        
        return {
            'positions': self.x,
            'intensity': intensity,
            'visibility': self.interference_visibility(intensity),
            'bright_only': np.abs(psi_bright_total)**2,
            'phase_difference': phase_diff
        }
    
    def weak_measurement_simulation(self, coupling_strength=0.1):
        """
        Simulate weak measurement that only partially collapses bright states.
        """
        # Initial superposed state
        psi_initial = self.total_wavefunction(self.x)
        
        # Weak measurement operator (only affects bright component)
        measurement_operator = np.exp(-coupling_strength * np.abs(self.x)**2)
        
        # Apply measurement
        psi_post = psi_initial * measurement_operator
        
        # Renormalize
        norm = np.sqrt(np.trapz(np.abs(psi_post)**2, self.x))
        psi_post /= norm
        
        return {
            'pre_measurement': np.abs(psi_initial)**2,
            'post_measurement': np.abs(psi_post)**2,
            'measurement_disturbance': measurement_operator
        }
    
    def phase_sweep_analysis(self, phase_range=(0, 4*np.pi), num_phases=100):
        """
        Analyze how interference patterns change with dark state phase.
        """
        phases = np.linspace(phase_range[0], phase_range[1], num_phases)
        visibilities = []
        peak_positions = []
        
        for phase in phases:
            intensity = self.observable_intensity(
                self.x, 1/np.sqrt(2), 1/np.sqrt(2), phase
            )
            visibilities.append(self.interference_visibility(intensity))
            peak_positions.append(self.x[np.argmax(intensity)])
        
        return {
            'phases': phases,
            'visibilities': np.array(visibilities),
            'peak_positions': np.array(peak_positions)
        }
    
    def create_comprehensive_plot(self):
        """Create a comprehensive visualization of the model."""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Bright/Dark Photon Interference Model Analysis', 
                    fontsize=16, fontweight='bold')
        
        # 1. Basic interference pattern
        ax1 = axes[0, 0]
        phases = [0, np.pi/2, np.pi, 3*np.pi/2]
        colors = ['cyan', 'orange', 'magenta', 'lime']
        
        for phase, color in zip(phases, colors):
            intensity = self.observable_intensity(
                self.x, 1/np.sqrt(2), 1/np.sqrt(2), phase
            )
            ax1.plot(self.x, intensity, color=color, 
                    label=f'φ_dark = {phase:.2f}', linewidth=2)
        
        ax1.set_title('Interference vs Dark Phase')
        ax1.set_xlabel('Position')
        ax1.set_ylabel('Intensity')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Double-slit simulation
        ax2 = axes[0, 1]
        double_slit_data = self.double_slit_experiment()
        
        ax2.plot(double_slit_data['positions'], double_slit_data['intensity'], 
                'cyan', linewidth=2, label='Combined (Bright+Dark)')
        ax2.plot(double_slit_data['positions'], double_slit_data['bright_only'], 
                'orange', linewidth=2, alpha=0.7, label='Bright Only')
        
        ax2.set_title(f'Double-Slit (V = {double_slit_data["visibility"]:.3f})')
        ax2.set_xlabel('Screen Position')
        ax2.set_ylabel('Intensity')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Phase sweep analysis
        ax3 = axes[0, 2]
        phase_data = self.phase_sweep_analysis()
        
        ax3.plot(phase_data['phases'], phase_data['visibilities'], 
                'lime', linewidth=2)
        ax3.set_title('Visibility vs Dark Phase')
        ax3.set_xlabel('Dark State Phase (rad)')
        ax3.set_ylabel('Fringe Visibility')
        ax3.grid(True, alpha=0.3)
        
        # 4. Weak measurement
        ax4 = axes[1, 0]
        weak_data = self.weak_measurement_simulation()
        
        ax4.plot(self.x, weak_data['pre_measurement'], 'cyan', 
                linewidth=2, label='Before Measurement')
        ax4.plot(self.x, weak_data['post_measurement'], 'orange', 
                linewidth=2, label='After Measurement')
        
        ax4.set_title('Weak Measurement Effect')
        ax4.set_xlabel('Position')
        ax4.set_ylabel('Probability Density')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Component analysis
        ax5 = axes[1, 1]
        psi_b = self.psi_bright(self.x)
        psi_d = self.psi_dark(self.x)
        
        ax5.plot(self.x, np.abs(psi_b)**2, 'cyan', 
                linewidth=2, label='|ψ_bright|²')
        ax5.plot(self.x, np.abs(psi_d)**2, 'magenta', 
                linewidth=2, label='|ψ_dark|²')
        ax5.plot(self.x, np.abs(psi_b + psi_d)**2/2, 'lime', 
                linewidth=2, label='|ψ_total|²')
        
        ax5.set_title('Wavefunction Components')
        ax5.set_xlabel('Position')
        ax5.set_ylabel('Probability Density')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Decoherence effect
        ax6 = axes[1, 2]
        psi_coherent = self.total_wavefunction(self.x)
        psi_decoherent = self.decoherence_model(psi_coherent, decoherence_rate=0.5)
        
        ax6.plot(self.x, np.abs(psi_coherent)**2, 'cyan', 
                linewidth=2, label='Coherent')
        ax6.plot(self.x, np.abs(psi_decoherent)**2, 'orange', 
                linewidth=2, label='Decoherent')
        
        ax6.set_title('Decoherence Effects')
        ax6.set_xlabel('Position')
        ax6.set_ylabel('Intensity')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def create_animation(self, parameter='phase', frames=100, interval=50):
        """Create animated visualization of parameter variation."""
        fig, ax = plt.subplots(figsize=(12, 8))
        line, = ax.plot([], [], 'cyan', linewidth=2)
        
        ax.set_xlim(self.x.min(), self.x.max())
        ax.set_ylim(0, 2)
        ax.set_xlabel('Position')
        ax.set_ylabel('Intensity')
        ax.grid(True, alpha=0.3)
        
        def animate(frame):
            if parameter == 'phase':
                phase = 4 * np.pi * frame / frames
                intensity = self.observable_intensity(
                    self.x, 1/np.sqrt(2), 1/np.sqrt(2), phase
                )
                ax.set_title(f'Dark State Phase = {phase:.2f} rad')
            
            elif parameter == 'amplitude':
                beta_mag = frame / frames
                alpha = np.sqrt(1 - beta_mag**2) if beta_mag < 1 else 0
                intensity = self.observable_intensity(
                    self.x, alpha, beta_mag, 0
                )
                ax.set_title(f'Dark Amplitude = {beta_mag:.2f}')
            
            line.set_data(self.x, intensity)
            return line,
        
        anim = FuncAnimation(fig, animate, frames=frames, 
                           interval=interval, blit=True)
        return anim, fig

# Demonstration usage
if __name__ == "__main__":
    # Initialize simulator
    sim = PhotonDualitySimulator()
    
    # Create comprehensive analysis
    fig = sim.create_comprehensive_plot()
    plt.show()
    
    # Create animation (uncomment to run)
    # anim, fig = sim.create_animation('phase')
    # plt.show()
    
    # Save animation as GIF (uncomment to save)
    # anim.save("bright_dark_interference.gif", writer=PillowWriter(fps=10))
    
    print("Photon Duality Simulator initialized successfully!")
    print("Use sim.create_comprehensive_plot() for analysis")
    print("Use sim.create_animation() for animated visualizations")
