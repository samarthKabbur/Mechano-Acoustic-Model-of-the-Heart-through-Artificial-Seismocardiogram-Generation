# Mechano-Acoustic-Model-of-the-Heart-through-Artificial-Seismocardiogram-Generation

URF Project Development Proposal for a Mechano Acoustic Model of the Heart through Artificial Seismocardiogram Generation and Cardiac Tissue Modeling
PI: Dr. Nanshu Lu, Mentor: Sarnab Bhattacarya, Researcher: Samarth Kabbur, University of Texas at Austin
Background and Statement of Objectives
1 			2			3		

Figure 1: Assorted imagery. 1. Heart with muscle damage and blocked artery. 2. SCG data collection flowchart. 3. Proposed artificial seismocardiogram generation system.
“Intelligence will transform our ability to monitor and detect heart disease,” says Dr. Peter Libby, a renowned cardiologist at Harvard-affiliated Brigham and Women's Hospital.1 His words encapsulate the ever-increasing importance of leveraging cutting-edge technologies to address one of the most prevalent and impactful health concerns affecting the public today – cardiac complications (Fig 1.1). 
At the forefront of cardiac monitoring is seismocardiography, or SCG, which allows us to measure the mechanical motion of the heart. SCG has shown remarkable promise in its utility, holding the potential to revolutionize the early detection and prediction of atrial fibrillation6, CAD7, and heart failure6,7, potentially years before they manifest clinically (Fig 1.2). While the promise of SCG is undeniable, the development of sensors capable of accurately measuring SCG and deriving meaningful physical characteristics of the heart from its signals has been hindered by challenges. Progress has been slow, and the cost of development has been prohibitive.2 In response to these limitations I aim to create a device that advances upon the capabilities of existing artificial SCG waveform generators.This device will have the ability to artificially generate a wide range of waveforms, enabling researchers to rigorously test their SCG sensors by placing them on top of artificial tissue. By doing so, we will establish an anatomically accurate mechano-acoustic model of the heart, enabling the development and testing of non-invasive devices under various simulated heart conditions (Fig 1.3). The implications of such a device are profound, as it can be employed broadly in research clinics and commercial testing, provided it receives the necessary approvals.
While existing SCG Generator Phantoms have demonstrated the ability to replicate SCG waveforms with up to 90% accuracy, there remain several unexplored avenues.3 This research seeks to answer important questions regarding the use of alternative transduction methods, such as piezoelectric, for SCG generation. Additionally, by introducing configurable noise and artifact simulation into the system, this study aims to enhance the utility of artificial SCG signal generation for algorithm testing.
The significance of this study will be underscored if the developed device consistently and accurately reproduces SCG waveforms recorded by gold standard SCG sensors in real human subjects. Furthermore, the incorporation of artificial tissue layers into the waveform generation process holds the potential to contribute to the creation of more realistic SCG waveforms, advancing the state of the art in this field.This research is expected to be of particular interest to seismocardiogram researchers and those involved in SCG sensor development, as it promises to accelerate the testing phase of their projects. Many within our laboratory share these research interests.
In conclusion, the objectives of this study are twofold: the primary objective is to assess if the inclusion of artificial tissue composed of PDMS and other biopolymers enhances the accuracy of artificial SCG waveforms, while the secondary objective seeks to explore the procedural combination of noise artifacts with SCG waveforms.  It addresses critical questions, introduces innovative approaches, and holds the promise of improving the reliability and accuracy of SCG sensor technology.
Proposed Research Plan
    1			2	                  3			   4

Figure 2: Prototype results of a speaker based SCG transduction/generation platform. 1. The 10.7cm x 10.7cm base plate and ADXL355 accelerometer 2. The hexagonal cross-structure and sandwich. 3. Side profile reveals the Visaton EX60-S electrodynamic exciter, printed support base, bottom cushion, and the top placement of direct SCG measurement 4. rPi 3B computational structure for interface with the exciter and accelerometer. The rPi hat is developed by Nikbakht et.al.
2.1 Build and validate a speaker based SCG transduction platform that allows for the vibrational playback of Heartsound.wav waveforms.
Under the guidance of my mentor and previous work on a SCG Generator Phantom (hardware and software) by Nikbakht et.al3 I have developed a mechano-acoustic foundation for the artificial generation of SCG waveforms, a critical component of our research methodology (Fig 2). This system has been structured to facilitate validation through external sensor measurements. The core of this setup features a carefully designed base plate characterized by dimensions and curvature tailored to minimize internal echoes (Fig 2.1). Positioned atop this base plate is an accelerometer, responsible for recording the SCG waveform (Fig 2.1). To bolster mechanical coupling and optimize vibration transmission, a hexagonal cross structure is sandwiched within (Fig 2.2). The uppermost layer comprises a thin, rigid printed plastic roof plate, serving as the platform for the placement of the external SCG measurement device (Fig 2.3). Connecting these elements is a Raspberry Pi housing Python code that not only transmits the SCG waveform for playback but also collects internal vibration data from the accelerometer (Fig 2.4).
This endeavor benefits from the existence of more advanced software, as seen in the work by Nikbakht et.al. This software encompasses a comprehensive suite of features, including a feedback transfer function for waveform calibration against noise, error handling mechanisms, terminal-based inputs for precise control over playback, and it performs well on my mechanical model. In my research, I intend to draw inspiration from and further develop this existing codebase to refine and optimize my own system for SCG signal generation and validation.
	2.2 Build and study the effect of anatomically correct cardiac tissue layers composed of eco-polydimethylsiloxane and other bio-polymers on the generation of accurate artificial seismocardiogram waveforms.
SCG sensors do not sit directly on top of the heart, rather they read signals that need to travel through many layers of bone and tissue, including the myocardium, peritoneum, sternum, etc.2 Using our available eco-PDMS and other biopolymers as necessary, I will create layers of variable thickness, density, and composition to create a low-level structure mimicking the anatomical layers of the heart. The layers will rest on the top surface of the existing SCG Generator. Experimental testing will determine if the biostructure allows for a generation of a more accurate SCG signal, compared to a barebones platform. The testing will include varying the mechanical coupling between layers, changing the weight of the sensor itself, and varying tissue density all as independent variables.
	2.3 Create an algorithm that can incorporate noise artifacts (walking, running, stomach palpitations, small impulse) into a clean SCG signal.
Available SCG databases are limited, and sometimes a researcher may want to test their sensors on a unique signal that isn’t available to us. For example, the topic of research may deal with creating an e-tattoo that can detect SCG features while the patient is walking, running, etc. Citation no. 2 also describes this problem as a gap in existing literature. I will create a novel program that can combine noise artifacts generated by walking, running, hiking, swimming, etc. with a ‘clean’ SCG signal, in order to simulate a ‘dirty’ signal. Such a signal would then be played in the SCG Generator for testing purposes, allowing the researcher to test their device on a large variety of signals, all on a small in-house machine, allowing them to minimize expensive human trials.
Project Schedule and Milestones
Task
Subtask
Y1
Q1
Q2
Q3
Q4


1
Optimize and groove mechanical structure 








Mitigate external noise










2
Methodize variable density PDMS production








Manufacture tissue layers








Validate signal accuracy











3
Accumulate noisy and clean datasets








Procedural generation of noisy signal








Validate signal accuracy to ground truth










Review of Literature
A seminal external study that significantly informs the present research is the work titled "A Synthetic Seismocardiogram and Electrocardiogram Generator Phantom," authored by Mohammad Nikbakht et. al. This study introduced a portable and innovative system designed to synthetically generate SCG and electrocardiogram (ECG) signals. The researchers developed a Raspberry Pi-based system capable of replicating input SCG and ECG waveforms as physical acceleration and voltage outputs. For SCG generation, an off-the-shelf exciter speaker was employed as a mechanical transducer, and its transfer function was meticulously calibrated to ensure accurate replication of SCG waveforms. The system's performance was rigorously validated using human SCG and ECG data, achieving a remarkable >90% correlation between input and output signals in both time and frequency domains. Importantly, amplitude errors were maintained within clinically acceptable ranges, allowing the system to produce realistic waveforms with amplitudes corresponding to critical cardiac features. This innovation enables safe data collection in environments unsafe for human participants and provides a valuable source of ground truth signals.
While the aforementioned study represents a significant advancement in SCG signal generation, there remain opportunities for further development and improvement. First, expanding the validation process to encompass more diverse SCG morphologies, as well as various cardiac conditions, will enhance the applicability and reliability of the synthetic signal generator. The addition of noise artifacts associated with walking, running, and other forms of human mobility to the input waveform can help synthesize the effect of real world continuous processes on the heart. Finally, the proposed research seeks to build upon this foundation by creating a device that not only generates SCG signals but also incorporates artificial tissue layers to model the complex physiological nuances of the human body.
Budget
Raspberry Pi 4b+ KIT: Faster processor unlocks real time SCG processing and computationally intensive Python packages: $186
PDMS and Crosslinker: Biopolymer to simulate tissue layers: $175
Visaton 60s Electrodynamic Actuator x2: Generates the main SCG signal: $160
PAD Ex 60s x4: $120 x2: Adheres generator to surface, minimizes noise: $20
Piezoelectric Actuator: To study other methods of SCG generation: $12
Foam Padding: To pad external connections to minimize noise and internal vibration: $5
Polylactic Acid Filament: 3D printer material for foundation fabrication: $19
Ninjaflex Polyurethane Filament: 3D printer material for flexible plastics $28
Florida Biomedical Society 2024 Conference. (Coronado Springs, Florida, Feb 8-11, 8:30-10pm daily session time). The FBSS contains 48 hours of education sessions on topics relating to biomechanics. Researcher has identified these learning opportunities as valuable for the progress of his project, and has identified attending individuals, companies, and products highly relevant to this research and my career goals: $189 Registration Fee + $144 Hotel Fee. The researcher agrees to cover all extra conference related fees to guarantee attendance. (https://www.cmia.org/events/florida-biomedical-society-2024-symposium/)
Total: $938
The materials in the itemized budget are essential to the design and production of the proposal and validation study. While basic lab materials and electronic elements are available through courtesy of the PI, URF funding will expedite my research progress. It will also allow for stronger validation testing, robust manufacturing of the model, and quality materials.
References Cited
1.	Can a smart watch diagnose a heart attack? Harvard Health https://www.health.harvard.edu/heart-health/can-a-smart-watch-diagnose-a-heart-attack.
2.	Taebi, A., Solar, B. E., Bomar, A. J., Sandler, R. H. & Mansy, H. A. Recent Advances in Seismocardiography. Vibration 2, 64–86 (2019). doi: 10.3390/vibration2010005.
3.	A Synthetic Seismocardiogram and Electrocardiogram Generator Phantom. doi:10.1109/SENSORS52175.2022.9967101 
4.	Blocked Artery https://www.flickr.com/photos/nihgov/33328945325.
5.	Heart beat detection algorithm flowchart. https://www.researchgate.net/figure/Heart-beat-detection-algorithm-flowchart_fig3_33661771
6. M. Pankaala et al., “Detection of atrial fibrillation with seismocardiography,” doi: 10.1109/EMBC.2016.7591695.
7. I. Korzeniowska‐Kubacka, “Usefulness of Seismocardiography,” doi: 10.1111/j.1542-474X.2005.00547.x.
