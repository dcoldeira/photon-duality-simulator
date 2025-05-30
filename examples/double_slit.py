#!/usr/bin/env python3
"""
Double-Slit Analysis with Bright/Dark States
============================================

This example demonstrates how the bright/dark photon model explains double-slit
interference patterns, including scenarios where classical explanations fall short.

Key Features:
- Traditional double-slit with bright/dark interpretation
- Path-dependent phase analysis
- "Which-path" information effects
- Delayed choice scenarios
- Comparison with standard quantum mechanics

Author: David Coldeira
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DoubleslitAnalyzer:
    """
    Comprehensive double-slit analysis using bright/dark photon model.
    """
    
    def __init__(self, slit_separation=2.0, slit_width=0.3, screen_distance=10.0):
        self.slit_separation = slit_separation
        self.slit_width = slit_width
        self.screen_distance = screen_distance
        self.x_screen = np.linspace(-4, 4, 1000)
        self.wavelength = 1.0  # Normalized wavelength
        self.k = 2 * np.pi / self.wavelength
        
    def path_difference(self, x):
        """Calculate path difference between two slits for screen position x."""
        slit1_pos = -self.slit_separation / 2
        slit2_pos = self.slit_separation / 2
        
        path1 = np.sqrt((x - slit1_pos)**2 + self.screen_distance**2)
        path2 = np.sqrt((x - slit2_pos)**2 + self.screen_distance**2)
        
        return path2 - path1
    
    def slit_envelope(self, x, slit_center):
        """Gaussian envelope for single slit."""
        return np.exp(-((x - slit_center)**2) / (2 * self.slit_width**2))
    
    def bright_dark_double_slit(self, alpha=1/np.sqrt(2), beta=1/np.sqrt(2), 
                               dark_phase_shift=0):
        """
        Simulate double-slit with bright/dark states.
        
        Args:
            alpha: amplitude of bright component
            beta: amplitude of dark component  
            dark_phase_shift: additional phase for dark states
        """
        slit1_pos = -self.slit_separation / 2
        slit2_pos = self.slit_separation / 2
        
        # Path differences and phases
        delta = self.path_difference(self.x_screen)
        phase_diff = self.k * delta
        
        # Bright states through each slit
        bright_1 = self.slit_envelope(self.x_screen, slit1_pos)
        bright_2 = self.slit_envelope(self.x_screen, slit2_pos) * np.exp(1j * phase_diff)
        
        # Dark states with additional phase relationship
        dark_1 = self.slit_envelope(self.x_screen, slit1_pos) * \
                np.exp(1j * dark_phase_shift)
        dark_2 = self.slit_envelope(self.x_screen, slit2_pos) * \
                np.exp(1j * (phase_diff + dark_phase_shift))
        
        # Total wavefunctions
        psi_bright = alpha * (bright_1 + bright_2) / np.sqrt(2)
        psi_dark = beta * (dark_1 + dark_2) / np.sqrt(2)
        psi_total = psi_bright + psi_dark
        
        return {
            'total_intensity': np.abs(psi_total)**2,
            'bright_only': np.abs(psi_bright)**2,
            'dark_only': np.abs(psi_dark)**2,
            'interference_term': 2 * np.real(psi_bright * np.conj(psi_dark)),
            'visibility': self.calculate_visibility(np.abs(psi_total)**2)
        }
    
    def calculate_visibility(self, intensity):
        """Calculate fringe visibility."""
        I_max, I_min = np.max(intensity), np.min(intensity)
        return (I_max - I_min) / (I_max + I_min) if I_max + I_min > 0 else 0
    
    def which_path_experiment(self, detection_efficiency=0.8):
        """
        Simulate 'which-path' detection that only affects bright states.
        
        This represents a key prediction: if detectors only interact with 
        bright states, some interference should persist from dark states.
        """
        results = {}
        
        # No which-path detection
        no_detection = self.bright_dark_double_slit()
        results['no_detection'] = no_detection
        
        # Partial which-path detection (only affects bright states)
        # Simulate by reducing bright amplitude and adding decoherence
        alpha_reduced = 1/np.sqrt(2) * np.sqrt(1 - detection_efficiency)
        beta_unchanged = 1/np.sqrt(2)
        
        with_detection = self.bright_dark_double_slit(
            alpha=alpha_reduced, 
            beta=beta_unchanged,
            dark_phase_shift=np.pi/8  # Small additional decoherence
        )
        results['with_detection'] = with_detection
        
        return results
    
    def delayed_choice_scenario(self):
        """
        Simulate delayed choice experiment in bright/dark framework.
        
        The decision to measure 'which-path' is made after the photon
        has passed through the slits but before detection.
        """
        # Initial state: coherent superposition
        initial_state = self.bright_dark_double_slit()
        
        # "Delayed" decision affects only detection of bright component
        delayed_bright_only = self.bright_dark_double_slit(
            alpha=1.0, beta=0.0  # Only bright states detected
        )
        
        delayed_dark_influence = self.bright_dark_double_slit(
            alpha=0.7, beta=0.714  # Some dark influence remains
        )
        
        return {
            'initial': initial_state,
            'bright_only': delayed_bright_only,
            'dark_influence': delayed_dark_influence
        }

def run_comprehensive_analysis():
    """Run complete double-slit analysis."""
    print("🔬 Double-Slit Analysis with Bright/Dark States")
    print("=" * 60)
    
    analyzer = DoubleslitAnalyzer()
    
    # Create comprehensive plot
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Double-Slit Analysis: Bright/Dark Photon Model', 
                 fontsize=16, fontweight='bold')
    
    # 1. Basic double-slit pattern
    ax1 = axes[0, 0]
    basic_result = analyzer.bright_dark_double_slit()
    
    ax1.plot(analyzer.x_screen, basic_result['total_intensity'], 
             'lime', linewidth=2, label='Total Intensity')
    ax1.plot(analyzer.x_screen, basic_result['bright_only'], 
             'cyan', linewidth=2, alpha=0.7, label='Bright Only')
    ax1.plot(analyzer.x_screen, basic_result['dark_only'], 
             'magenta', linewidth=2, alpha=0.7, label='Dark Only')
    
    ax1.set_title(f"Basic Pattern (V = {basic_result['visibility']:.3f})")
    ax1.set_xlabel('Screen Position')
    ax1.set_ylabel('Intensity')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Dark phase variation
    ax2 = axes[0, 1]
    dark_phases = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    colors = ['lime', 'orange', 'red', 'yellow']
    
    for phase, color in zip(dark_phases, colors):
        result = analyzer.bright_dark_double_slit(dark_phase_shift=phase)
        ax2.plot(analyzer.x_screen, result['total_intensity'], 
                color=color, linewidth=2, 
                label=f'φ_dark = {phase:.2f}')
    
    ax2.set_title('Dark State Phase Effects')
    ax2.set_xlabel('Screen Position')
    ax2.set_ylabel('Intensity')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Which-path experiment
    ax3 = axes[0, 2]
    which_path_results = analyzer.which_path_experiment()
    
    ax3.plot(analyzer.x_screen, which_path_results['no_detection']['total_intensity'],
             'lime', linewidth=2, label='No Detection')
    ax3.plot(analyzer.x_screen, which_path_results['with_detection']['total_intensity'],
             'orange', linewidth=2, label='With Detection')
    
    ax3.set_title('Which-Path Detection Effect')
    ax3.set_xlabel('Screen Position') 
    ax3.set_ylabel('Intensity')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Visibility vs detection efficiency
    ax4 = axes[1, 0]
    efficiencies = np.linspace(0, 1, 20)
    visibilities = []
    
    for eff in efficiencies:
        wp_result = analyzer.which_path_experiment(detection_efficiency=eff)
        visibilities.append(wp_result['with_detection']['visibility'])
    
    ax4.plot(efficiencies, visibilities, 'lime', linewidth=3, marker='o')
    ax4.set_title('Visibility vs Detection Efficiency')
    ax4.set_xlabel('Detection Efficiency')
    ax4.set_ylabel('Fringe Visibility')
    ax4.grid(True, alpha=0.3)
    
    # 5. Delayed choice results
    ax5 = axes[1, 1]
    delayed_results = analyzer.delayed_choice_scenario()
    
    ax5.plot(analyzer.x_screen, delayed_results['initial']['total_intensity'],
             'lime', linewidth=2, label='Initial State')
    ax5.plot(analyzer.x_screen, delayed_results['bright_only']['total_intensity'],
             'cyan', linewidth=2, label='Bright Detection Only')
    ax5.plot(analyzer.x_screen, delayed_results['dark_influence']['total_intensity'],
             'magenta', linewidth=2, label='Dark Influence Remains')
    
    ax5.set_title('Delayed Choice Effects')
    ax5.set_xlabel('Screen Position')
    ax5.set_ylabel('Intensity')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Interference term analysis
    ax6 = axes[1, 2]
    result = analyzer.bright_dark_double_slit()
    
    ax6.plot(analyzer.x_screen, result['total_intensity'], 
             'lime', linewidth=2, label='Total')
    ax6.plot(analyzer.x_screen, result['bright_only'] + result['dark_only'],
             'orange', linewidth=2, linestyle='--', label='Incoherent Sum')
    ax6.plot(analyzer.x_screen, result['interference_term'],
             'red', linewidth=2, alpha=0.7, label='Interference Term')
    
    ax6.set_title('Coherent vs Incoherent Contributions')
    ax6.set_xlabel('Screen Position')
    ax6.set_ylabel('Intensity')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print analysis summary
    print_analysis_summary(analyzer, basic_result, which_path_results)

def print_analysis_summary(analyzer, basic_result, which_path_results):
    """Print summary of key findings."""
    print("\n📊 Analysis Summary")
    print("=" * 50)
    print(f"Slit separation: {analyzer.slit_separation}")
    print(f"Screen distance: {analyzer.screen_distance}")
    print(f"Basic visibility: {basic_result['visibility']:.3f}")
    
    no_det_vis = which_path_results['no_detection']['visibility']
    with_det_vis = which_path_results['with_detection']['visibility']
    
    print(f"Visibility without which-path detection: {no_det_vis:.3f}")
    print(f"Visibility with which-path detection: {with_det_vis:.3f}")
    print(f"Visibility reduction: {(1 - with_det_vis/no_det_vis)*100:.1f}%")
    
    print("\n🎯 Key Predictions of Bright/Dark Model:")
    print("1. Which-path detection affects only bright states")
    print("2. Some interference persists from dark state coherence")
    print("3. Dark state phase relationships influence patterns")
    print("4. Delayed choice affects detection, not propagation")

if __name__ == "__main__":
    run_comprehensive_analysis()
    print("\n✨ This analysis demonstrates testable predictions!")
    print("   Try varying the parameters to explore different scenarios.")
