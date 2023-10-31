# Synthetic ECG SCG Generator Hardware

The seismocardiogram (SCG) is a measure of chest wall vibrations resulting from the heartbeat. The SCG is typically
recorded using a low-noise accelerometer placed on the mid-sternum and contains features related to cardiovascular
activity such as aortic valve opening (AO) and aortic closing (AC). These features can support assessment of cardiovascular health and have been used in conjunction with other physiological signals to monitor key health parameters such as blood volume status and intracardiac filling pressures.

Electrocardiogram (ECG) signal reflects the electrical activity of the heart observed from the strategic points of the human body and represented by quasi-periodic voltage signal.
<!-- 
These signals fiducial points correspond to characteristic events in the cardiac cycle. For the SCG, the labels correspond to the physiological event they are believed to represent: MC, mitral valve closure; IVC, isovolumetric contraction; AO, aortic valve opening; RE, rapid ejection; AC, aortic valve closure; MO, mitral valve open- ing; and RF, rapid filling. -->

<!-- However, SCG signals are small signal, and they can get distorted easily by motion artifacts. Therefore exploring denoising methods is of great importance for SCG signals. Clearing out the noise enables extraction of physiologically relevant information from SCG. To study denoising methods, we need to collect SCG signals in noisy environments, but it is unsafe to use human subjects for such data collection in some high motion environments (medical transport helicopters). To address this, here we designed a phantom that can generate SCG and ECG signals synthetically. This enables us to collect data in those noisy environmnets without human subject involvement.
 -->
In this work, we introduce a portable USB-C powered Raspberry Pi-based system that can replicate any SCG and ECG signal inputs with minimal error in forms of acceleration and voltage. The SCG signals are generated using an off the shelf exciter speaker, and the ECG signals are generated using a voltage amplifier through 3 conductive pads. The generated signals can be recorded using the same wearable devices that are used to measure human SCG and ECG signals. Thus, this system can be used as a safer, more convenient alternative to human participants in high external vibration environments for testing and validating
classification/regression tasks and noise reduction algorithms.

## The Hardware 

he system proposed in this work consists of an actuator unit and a processing unit. The actuator unit, which generates SCG and ECG signals. 

<p align="center">
<img src="https://github.com/mohnikbakht/SyntheticSCG-Hardware/blob/main/figures/figure1.png" alt="Image of The ECG/SCG Patch" width="600"/>
</p>


<!-- <img src="https://github.com/mohnikbakht/Synthetic_ECG_SCG_Generator_Demo/blob/main/Images/Actuator2.png" alt="Image of The ECG/SCG Patch" width="300"/> -->


The system designed here offers two user-controlled modes of operation: (1) calibration, which re-estimates the transfer function of the exciter speaker with the added load on the platform (wearable sensors) , and (2) signal generation, which generates the ECG and SCG sequences.

A block diagram of the system operation:
<p align="center">
 <img src="https://github.com/mohnikbakht/SyntheticSCG-Hardware/blob/main/figures/figure2.png" alt="Image of The ECG/SCG Patch" width="800"/>
</p>

### Commands

1) Calibration mode: Calibrate the system (in a new environment):

calculate the transfer function of the actuator using a sine sweep and use it to calibrate the SCG beats to be ready for generation
 
```console
python3 SCG_Generator.py tf_estimate desktop
python3 SCG_Generator.py calibrate seq_synth desktop (or any file name [without .pkl])
```
<!-- 
<img src="https://github.com/mohnikbakht/Synthetic_ECG_SCG_Generator_Demo/blob/main/Images/calibrate_1.png" alt="Image of The ECG/SCG Patch" width="400"/> -->


2) Generation mode: Generate SCG waveforms:

generate SCG and ECG signals using the calibrated beats stored in the previous step

```console
python3 SCG_Generator.py generate seq_synth_calibrated desktop (or any file name you stored the calibrated signals [without .pkl])
```

<!-- <img src="https://github.com/mohnikbakht/Synthetic_ECG_SCG_Generator_Demo/blob/main/Images/generate_1.png" alt="Image of The ECG/SCG Patch" width="400"/> -->



## Use

Depending on the type of the connection to the RPi, there are 2 options:
1) If a display is connected to the RPi (or have X11 forwarding enabled), the plots will be shown in separate windows. Use this command (this mode is default):
```console
python3 SCG_generate.py generate signal_sample_calibrated desktop
```
2) If communication is through a terminal only, the plots will be plotted in the terminal (lower quality). Use this command:
```console
python3 SCG_generate.py generate signal_sample_calibrated terminal
```
## Output Recording Samples

A sample of the generator-output SCG and ECG compared to the ECG and SCG inputs:

<p align="center">
<img src="https://github.com/mohnikbakht/SyntheticSCG-Hardware/blob/main/figures/figure3_2.png" alt="Image of The ECG/SCG Patch" width="800"/>
</p>

Bland-Altman plots of error between the measured generator-output and the real human signal input based on the amplitude of the most prominent
feature of the beats after heartbeat segmentation for (a) SCG, and (b) ECG signals. 

<p align="center">
<img src="https://github.com/mohnikbakht/SyntheticSCG-Hardware/blob/main/figures/bland-altman.png" alt="Image of The ECG/SCG Patch" width="800"/>
</p>

<!-- Zoomed in:

<img src="https://github.com/mohnikbakht/Synthetic_ECG_SCG_Generator_Demo/blob/main/Images/sample_2.png" alt="Image of The ECG/SCG Patch" width="600"/>

 -->

## Reference

Please cite this paper:

M. Nikbakht, D. J. Lin, A. H. Gazi, and O. T. Inan, “A synthetic
seismocardiogram and electrocardiogram generator phantom,” in 2022
IEEE Sensors, in press.

BibTeX format: 

@inproceedings{nikbakht2022synthetic,
title={A Synthetic Seismocardiogram and Electrocardiogram Generator Phantom},
author={Nikbakht, Mohammad, and Lin, David J., and Gazi, Asim H., and Inan, Omer T.},
note={in press},
booktitle={2022 IEEE Sensors},
% pages={Accepted},
% year={2022},
% organization={IEEE}
}

