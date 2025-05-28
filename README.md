# Photon Duality Simulator: Bright/Dark State Interference Model

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

This project presents a novel theoretical framework and computational simulator for quantum interference patterns based on **bright/dark photon states**. The model proposes that photons exist as superpositions of:

- **Bright states** (|B⟩): Directly detectable by measurement apparatus
- **Dark states** (|D⟩): Undetectable but influence interference through coherent evolution

This framework bridges multiple quantum mechanical interpretations while providing testable predictions for experimental validation.

## Theoretical Foundation

### Core Hypothesis

**Interference patterns arise from the interaction between "bright" (detectable) and "dark" (undetectable) photon states, where only bright states contribute directly to measurement outcomes.**

### Mathematical Formulation

The total photon state is expressed as:
```
|ψ⟩ = α|B⟩ + β|D⟩
```

Where:
- `α, β ∈ ℂ` with `|α|² + |β|² = 1` (normalization)
- Detection probability: `P_detect = |α|²`
- Interference intensity: `I(x) ∝ |α⟨x|B⟩ + β⟨x|D⟩|²`

The cross-term `α*β⟨x|B⟩*⟨x|D⟩` generates interference patterns even when only the bright component is directly measurable.

### Theoretical Connections

1. **Quantum Superposition**: Dark states represent unmeasured components of the wavefunction
2. **Pilot-Wave Theory**: Dark states act as guiding fields for bright particle detection
3. **Decoherence Theory**: Environmental interactions selectively affect bright vs. dark components
4. **Weak Measurement**: Partial collapse scenarios naturally emerge from this formalism

## Features

### Core Simulation Capabilities

- **Spatial Wavefunction Modeling**: Gaussian envelope functions with momentum components
- **Interference Pattern Generation**: Real-time computation of bright/dark state interactions  
- **Phase Relationship Analysis**: Dynamic visualization of how dark state phases affect observable patterns
- **Double-Slit Experiments**: Full simulation including path differences and fringe visibility
- **Weak Measurement Effects**: Modeling partial wavefunction collapse scenarios
- **Decoherence Modeling**: Environmental interaction effects on coherence

### Advanced Analysis Tools

- **Fringe Visibility Calculations**: Quantitative measure of interference quality
- **Phase Sweep Analysis**: Systematic study of parameter space
- **Component Decomposition**: Separate analysis of bright/dark contributions
- **Animated Visualizations**: Real-time parameter variation studies

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/[username]/photon-duality-simulator.git
cd photon-duality-simulator
```

2. **Create a virtual environment** (recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Simulator

#### Simple Version (Recommended for beginners)
```bash
python dark_light_interference_simulator.py
```

This will:
- Display a comprehensive theoretical overview
- Generate static analysis plots
- Show an animated phase variation
- Optionally save animations as GIFs

#### Advanced Class-Based Version
```python
from photon_simulator import PhotonDualitySimulator

# Initialize simulator
sim = PhotonDualitySimulator()

# Generate comprehensive analysis
fig = sim.create_comprehensive_plot()

# Run double-slit experiment
results = sim.double_slit_experiment(slit_separation=2.0)
print(f"Fringe visibility: {results['visibility']:.3f}")

# Create phase animation
anim, fig = sim.create_animation('phase')
```

### Virtual Environment Management

**Activate environment** (before running simulations):
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Deactivate environment** (when finished):
```bash
deactivate
```

**Requirements file** (`requirements.txt`):
```
numpy>=1.21.0
matplotlib>=3.5.0
scipy>=1.7.0
seaborn>=0.11.0
```

## Experimental Predictions & Testable Hypotheses

### 1. Modified Interferometer Experiments

**Prediction**: Introduce selective decoherence that only affects bright states while preserving dark state coherence. Residual interference should persist even when bright paths are decohered.

**Test Setup**: Mach-Zehnder interferometer with polarization-selective weak measurement in one arm.

### 2. Dark-Channel Phase Control

**Prediction**: Controllable phase delays applied only to dark components should shift interference fringes in detectable patterns.

**Test Setup**: Encode dark states in orthogonal polarization or frequency modes outside detector bandwidth, then apply controlled phase shifts.

### 3. Post-Selection Experiments

**Prediction**: Weak measurement followed by post-selection should reveal dark state influence on detected photon statistics.

**Test Setup**: Use quantum eraser techniques to reconstruct dark path contributions through correlation analysis.

### 4. Visibility Scaling Laws

**Prediction**: Interference visibility should scale with the coherent product |α·β| rather than individual bright/dark amplitudes.

**Test Setup**: Systematically vary bright/dark amplitude ratios while maintaining total normalization.

## Current Simulation Results

The simulator demonstrates several key phenomena:

1. **Phase-Dependent Interference**: Dark state phase variations produce observable fringe shifts
2. **Visibility Enhancement**: Optimal bright/dark ratios maximize interference contrast
3. **Decoherence Resistance**: Dark states show differential robustness to environmental noise
4. **Weak Measurement Signatures**: Partial collapse scenarios produce characteristic distortions

## Project Structure

```
photon-duality-simulator/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── dark_light_interference_simulator.py   # Simple standalone simulator
├── photon_simulator.py                    # Advanced class-based simulator
├── venv/                                  # Virtual environment (created by you)
├── examples/                              # Example scripts and notebooks
│   ├── basic_interference.py
│   ├── double_slit_analysis.py
│   └── weak_measurement_demo.py
└── docs/                                  # Additional documentation
    ├── theory.md                          # Detailed theoretical framework
    ├── experiments.md                     # Proposed experimental setups
    └── api_reference.md                   # Code documentation
```

## Troubleshooting

### Common Issues

**Import errors after installation:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Verify packages are installed
pip list
```

**Plots not displaying:**
```bash
# On some systems, you may need tkinter
sudo apt-get install python3-tk  # Ubuntu/Debian
# or
brew install python-tk           # macOS with Homebrew
```

**Animation not working:**
```bash
# Install additional multimedia support
pip install pillow
```

### Platform-Specific Notes

**Windows Users:**
- Use `python` instead of `python3` in commands
- Use backslashes in paths: `venv\Scripts\activate`

**macOS Users:**
- May need to install Xcode command line tools: `xcode-select --install`
- If using M1/M2 Mac, ensure compatibility with `arch -x86_64` prefix if needed

**Linux Users:**
- May need additional packages: `sudo apt-get install python3-dev python3-tk`

### Near-term Development
- [ ] **Entanglement Support**: Multi-photon bright/dark state correlations
- [ ] **Realistic Detector Models**: Quantum efficiency and noise characteristics  
- [ ] **3D Spatial Dynamics**: Full vectorial electromagnetic field treatment
- [ ] **Temporal Evolution**: Time-dependent Schrödinger equation integration

### Long-term Research Directions
- [ ] **Field Theory Extension**: Second-quantized bright/dark field operators
- [ ] **Bell Test Scenarios**: Bright/dark state non-locality experiments
- [ ] **Cavity QED**: Bright/dark state interactions with optical resonators
- [ ] **Machine Learning**: Pattern recognition for dark state signatures

## Contributing

We welcome contributions from the quantum optics, foundations of quantum mechanics, and computational physics communities. Areas of particular interest:

- **Experimental Design**: Proposals for bright/dark state detection schemes
- **Theoretical Extensions**: Mathematical refinements and new predictions  
- **Code Optimization**: Performance improvements for large-scale simulations
- **Visualization**: Enhanced plotting and animation capabilities

## Literature & Related Work

This model connects to several established areas:

- **Bohmian Mechanics**: Pilot-wave guidance mechanisms
- **Consistent Histories**: Alternative quantum interpretation frameworks  
- **Quantum Darwinism**: Environment-induced superselection rules
- **Weak Measurement Theory**: Partial information extraction protocols

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this simulator in your research, please cite:

```bibtex
@software{photon_duality_simulator,
  title={Photon Duality Simulator: Bright/Dark State Interference Model},
  author={[Your Name]},
  year={2025},
  url={https://github.com/[username]/photon-duality-simulator}
}
```

## Contact

For questions, collaborations, or experimental proposals, please open an issue or contact [your email].

---

*"The dark states guide the bright, creating patterns in the observable world through their invisible dance."*