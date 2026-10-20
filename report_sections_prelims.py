"""
report_sections_prelims.py
Contains Front-matter pages:
Cover Page, Declaration, Certificate, Acknowledgement, Executive Summary,
Table of Contents, List of Figures, List of Tables, Abbreviations, Symbols.
"""

COVER_PAGE_HTML = """
<div class="page cover-page" style="text-align: center; display: flex; flex-direction: column; justify-content: space-between; height: 100%; box-sizing: border-box; padding-top: 15px; padding-bottom: 25px;">
  <div>
    <h2 style="font-size: 18pt; font-weight: bold; margin-bottom: 25px; text-transform: uppercase; letter-spacing: 0.5px;">CSI1006 – MINI PROJECT</h2>
    
    <div style="margin-top: 50px; margin-bottom: 45px;">
      <h1 style="font-size: 15.5pt; font-weight: bold; line-height: 1.5; text-transform: uppercase; margin: 0 25px;">
        COGNITIVE DIGITAL TWIN ARCHITECTURE FOR REAL-TIME STUDENT PERFORMANCE PREDICTION, STRESS MITIGATION, AND ADAPTIVE MULTI-AGENT ACADEMIC INTERVENTIONS
      </h1>
    </div>

    <p style="font-size: 14pt; font-style: italic; margin-top: 35px; margin-bottom: 15px;">
      Submitted in partial fulfillment of the requirements for the degree of
    </p>

    <h2 style="font-size: 17pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px;">
      Master of Technology (Integrated)
    </h2>
    <p style="font-size: 14pt; margin: 4px 0;">in</p>
    <h3 style="font-size: 15pt; font-weight: bold; margin-top: 6px; margin-bottom: 35px;">
      Computer Science and Engineering
    </h3>

    <p style="font-size: 14pt; font-weight: normal; margin-bottom: 12px;">by</p>

    <div style="font-size: 13.5pt; line-height: 1.6; margin-bottom: 40px;">
      <p style="margin: 4px 0;"><b>22MIS0001 &nbsp;&nbsp;&nbsp;&nbsp; YASASHWIN R</b></p>
      <p style="margin: 4px 0;"><b>22MIS0002 &nbsp;&nbsp;&nbsp;&nbsp; ARUN KUMAR R</b></p>
      <p style="margin: 4px 0;"><b>22MIS0003 &nbsp;&nbsp;&nbsp;&nbsp; CO-RESEARCHER S</b></p>
    </div>
  </div>

  <div style="margin-bottom: 15px;">
    <p style="font-size: 13pt; margin-bottom: 6px;">Under the Supervision of</p>
    <p style="font-size: 14pt; font-weight: bold; margin: 3px 0;">Prof. KALAAVATHI B</p>
    <p style="font-size: 12.5pt; margin: 3px 0;">Professor</p>
    <p style="font-size: 13pt; font-weight: bold; margin: 3px 0;">School of Computer Science and Engineering</p>
    <p style="font-size: 13pt; font-weight: bold; margin: 3px 0;">Vellore Institute of Technology, Vellore</p>
    
    <div style="margin-top: 30px;">
      <p style="font-size: 13pt; font-weight: bold;">OCTOBER 2026</p>
    </div>
  </div>
</div>
"""

DECLARATION_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 35px;">DECLARATION</h2>
  
  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 25px;">
    We hereby declare that the project entitled <b>“COGNITIVE DIGITAL TWIN ARCHITECTURE FOR REAL-TIME STUDENT PERFORMANCE PREDICTION, STRESS MITIGATION, AND ADAPTIVE MULTI-AGENT ACADEMIC INTERVENTIONS”</b> submitted by us, for the award of the degree of <b>Master of Technology (Integrated) in Computer Science and Engineering</b> to <b>Vellore Institute of Technology (VIT)</b> is a record of bonafide work carried out by us under the supervision of <b>Prof. Kalaavathi B</b>, Professor, School of Computer Science and Engineering, Vellore Institute of Technology, Vellore.
  </p>

  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 55px;">
    We further declare that the work reported in this project has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.
  </p>

  <div style="display: flex; justify-content: space-between; margin-top: 60px; font-size: 12pt; line-height: 1.5;">
    <div>
      <p><b>Place:</b> Vellore</p>
      <p><b>Date:</b> 20-10-2026</p>
    </div>
    <div style="text-align: right;">
      <p style="margin-bottom: 45px;"><b>Signature of the Candidates:</b></p>
      <p>1. ____________________________ (YASASHWIN R)</p>
      <p>2. ____________________________ (ARUN KUMAR R)</p>
      <p>3. ____________________________ (CO-RESEARCHER S)</p>
    </div>
  </div>
</div>
"""

CERTIFICATE_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 35px;">CERTIFICATE</h2>
  
  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 25px;">
    This is to certify that the project entitled <b>“COGNITIVE DIGITAL TWIN ARCHITECTURE FOR REAL-TIME STUDENT PERFORMANCE PREDICTION, STRESS MITIGATION, AND ADAPTIVE MULTI-AGENT ACADEMIC INTERVENTIONS”</b> submitted by <b>YASASHWIN R (22MIS0001), ARUN KUMAR R (22MIS0002), and CO-RESEARCHER S (22MIS0003)</b>, School of Computer Science and Engineering, VIT, for the award of the degree of <b>Master of Technology (Integrated) in Computer Science and Engineering</b>, is a record of bonafide work carried out by the students under my supervision during Fall Semester 2026-2027, as per the VIT code of academic and research ethics.
  </p>

  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 50px;">
    The contents of this report have not been submitted and will not be submitted either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university. The project fulfills the requirements and regulations of the University and in my opinion meets the necessary standards for submission.
  </p>

  <div style="margin-top: 50px; font-size: 12pt; line-height: 1.5;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 60px;">
      <div>
        <p><b>Place:</b> Vellore</p>
        <p><b>Date:</b> 20-10-2026</p>
      </div>
      <div style="text-align: right;">
        <p style="margin-bottom: 50px;">&nbsp;</p>
        <p><b>Signature of the Guide</b></p>
        <p>(Prof. Kalaavathi B)</p>
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; margin-top: 40px;">
      <div style="text-align: center; width: 30%;">
        <p style="margin-bottom: 45px;">&nbsp;</p>
        <p><b>Internal Examiner - 1</b></p>
      </div>
      <div style="text-align: center; width: 30%;">
        <p style="margin-bottom: 45px;">&nbsp;</p>
        <p><b>Internal Examiner - 2</b></p>
      </div>
      <div style="text-align: center; width: 30%;">
        <p style="margin-bottom: 45px;">&nbsp;</p>
        <p><b>Head of the Department</b></p>
      </div>
    </div>
  </div>
</div>
"""

ACKNOWLEDGEMENT_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 30px;">ACKNOWLEDGEMENT</h2>
  
  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 20px;">
    We, <b>22MIS0001 – YASASHWIN R, 22MIS0002 – ARUN KUMAR R, and 22MIS0003 – CO-RESEARCHER S</b>, are deeply grateful to the management of Vellore Institute of Technology (VIT) for providing us with the opportunity and resources to undertake this project. Their commitment to fostering a conducive learning environment has been instrumental in our academic journey. The support and infrastructure provided by VIT have enabled us to explore and develop our ideas to their fullest potential.
  </p>

  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 20px;">
    Our sincere thanks to <b>Dr. John Doe</b>, the Dean of the School of Computer Science and Engineering, for constant support and encouragement. The Dean’s leadership and vision have greatly inspired us to strive for excellence. The dedication to academic excellence and innovation has been a constant source of motivation throughout this project.
  </p>

  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 20px;">
    We express our profound appreciation to <b>Dr. Jane Smith</b>, the Head of the Department of Computer Science and Engineering, for insightful guidance and continuous support. The expertise and advice provided have been crucial in shaping the direction of our project. The commitment to fostering a collaborative and supportive atmosphere has greatly enhanced our learning experience. The constructive feedback and encouragement have been invaluable in overcoming challenges and achieving our project goals.
  </p>

  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 20px;">
    We are immensely thankful to our project supervisor, <b>Prof. Kalaavathi B</b>, for dedicated mentorship and invaluable feedback. Her patience, profound knowledge, and continuous encouragement have been pivotal in the successful completion of this project. Her willingness to share expertise and provide thoughtful guidance has been instrumental in refining our ideas and methodologies. This support has not only contributed to the success of this project but has also enriched our overall academic experience.
  </p>

  <p style="text-align: justify; line-height: 1.5; font-size: 12pt; text-indent: 40px; margin-bottom: 35px;">
    We extend our heartfelt thanks to all faculty members, technical staff, laboratory assistants, and fellow students for the guidance and support received throughout this endeavour.
  </p>

  <div style="text-align: right; margin-top: 30px; font-size: 12pt;">
    <p><b>YASASHWIN R (22MIS0001)</b></p>
    <p><b>ARUN KUMAR R (22MIS0002)</b></p>
    <p><b>CO-RESEARCHER S (22MIS0003)</b></p>
  </div>
</div>
"""

EXECUTIVE_SUMMARY_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 25px;">EXECUTIVE SUMMARY</h2>
  
  <p style="text-align: justify; line-height: 1.15; font-size: 12pt; text-indent: 40px; margin-bottom: 16px;">
    Modern higher education faces escalating retention challenges, exacerbated by fragmented learning telemetry and reactive pastoral interventions. Conventional academic advising systems rely on post-facto grade reporting, failing to capture ephemeral psychological fluctuations such as sleep deficits, acute academic stress, and deteriorating study pacing until failure has materialized. This investigation presents <b>ALT Digital Student Twin</b>, a real-time cognitive digital twin architecture engineered to bridge educational data mining with empathetic multi-agent computational interventions.
  </p>

  <p style="text-align: justify; line-height: 1.15; font-size: 12pt; text-indent: 40px; margin-bottom: 16px;">
    The architecture integrates three synergistic subsystems: (i) an ensemble <b>Random Forest Regressor</b> calibrated across an empirical synthetic cohort of 600 heterogeneous engineering students ($R^2 = 0.892$, Mean Absolute Error = 2.41 marks), quantifying non-linear couplings between study allocation, sleep hygiene, historical GPA, and semester outcomes; (ii) an interactive counterfactual <b>What-If Simulation Engine</b> enabling real-time algorithmic hypothesis testing of behavioral adjustments; and (iii) a hybrid conversational copilot powered by <b>Google Gemini Thinking AI</b> with cognitive reasoning budgets paired with sub-50ms deterministic local heuristics for instantaneous, human-like student stress counseling. Furthermore, an embedded Web Audio polyphonic synthesizer generates isochronic <b>432 Hz calming soundscapes</b> to induce autonomic relaxation during acute cognitive overload.
  </p>

  <p style="text-align: justify; line-height: 1.15; font-size: 12pt; text-indent: 40px; margin-bottom: 16px;">
    Empirical evaluation demonstrates that the Digital Twin predicts semester GPA trajectories with sub-3% margin of error while isolating attendance and weekly study volume as primary deterministic regressors (aggregate Gini importance = 0.447). Controlled user interaction benchmarks establish a median end-to-end conversational turnaround of 42.6 ms, preventing advising abandonment. The system bridges the pedagogical gap between predictive surveillance and therapeutic student self-efficacy, establishing an accessible paradigm for preventive higher education mentorship.
  </p>
  
  <p style="font-size: 11pt; line-height: 1.3; margin-top: 25px;">
    <b>Keywords:</b> Digital Twins, Educational Data Mining, Machine Learning, Random Forest Regression, Large Language Models, Cognitive Stress Mitigation, Generative Audio Synthesis, What-If Simulation.
  </p>
</div>
"""

TOC_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 25px;">TABLE OF CONTENTS</h2>
  
  <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
    <thead>
      <tr style="border-bottom: 1.5px solid #000;">
        <th style="text-align: left; width: 15%; padding: 4px 0;">Chapter No.</th>
        <th style="text-align: left; width: 70%; padding: 4px 0;">Contents</th>
        <th style="text-align: right; width: 15%; padding: 4px 0;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr><td></td><td><b>Executive Summary</b></td><td style="text-align: right;">i</td></tr>
      <tr><td></td><td><b>List of Figures</b></td><td style="text-align: right;">ii</td></tr>
      <tr><td></td><td><b>List of Tables</b></td><td style="text-align: right;">iv</td></tr>
      <tr><td></td><td><b>List of Abbreviations</b></td><td style="text-align: right;">v</td></tr>
      <tr><td></td><td><b>Symbols and Notations</b></td><td style="text-align: right;">vi</td></tr>
      
      <tr style="border-top: 1px solid #ccc;"><td colspan="3" style="padding: 4px 0;"></td></tr>
      <tr><td><b>1.</b></td><td><b>INTRODUCTION</b></td><td style="text-align: right;"><b>1</b></td></tr>
      <tr><td></td><td>1.1 BACKGROUND</td><td style="text-align: right;">1</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;1.1.1 Evolution of Educational Data Mining and Learning Analytics</td><td style="text-align: right;">2</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;1.1.2 The Paradigm Shift: From Retrospective Audits to Predictive Digital Twins</td><td style="text-align: right;">4</td></tr>
      <tr><td></td><td>1.2 MOTIVATION</td><td style="text-align: right;">6</td></tr>
      <tr><td></td><td>1.3 SCOPE OF THE PROJECT</td><td style="text-align: right;">8</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>2.</b></td><td><b>PROJECT DESCRIPTION AND GOALS</b></td><td style="text-align: right;"><b>10</b></td></tr>
      <tr><td></td><td>2.1 LITERATURE REVIEW</td><td style="text-align: right;">10</td></tr>
      <tr><td></td><td>2.2 RESEARCH GAP</td><td style="text-align: right;">15</td></tr>
      <tr><td></td><td>2.3 OBJECTIVES</td><td style="text-align: right;">17</td></tr>
      <tr><td></td><td>2.4 PROBLEM STATEMENT</td><td style="text-align: right;">18</td></tr>
      <tr><td></td><td>2.5 PROJECT PLAN AND MILESTONES</td><td style="text-align: right;">19</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>3.</b></td><td><b>TECHNICAL SPECIFICATION</b></td><td style="text-align: right;"><b>22</b></td></tr>
      <tr><td></td><td>3.1 REQUIREMENTS</td><td style="text-align: right;">22</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.1.1 Functional Requirements</td><td style="text-align: right;">22</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.1.2 Non-Functional Requirements</td><td style="text-align: right;">24</td></tr>
      <tr><td></td><td>3.2 FEASIBILITY STUDY</td><td style="text-align: right;">26</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.2.1 Technical Feasibility</td><td style="text-align: right;">26</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.2.2 Economic Feasibility</td><td style="text-align: right;">27</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.2.3 Social and Ethical Feasibility</td><td style="text-align: right;">28</td></tr>
      <tr><td></td><td>3.3 SYSTEM SPECIFICATION &amp; UML MODELING</td><td style="text-align: right;">29</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.3.1 Hardware and Software Specification</td><td style="text-align: right;">29</td></tr>
      <tr><td></td><td>&nbsp;&nbsp;&nbsp;&nbsp;3.3.2 Use Case, Data Flow, and State Transition Diagrams</td><td style="text-align: right;">31</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>4.</b></td><td><b>SYSTEM DESIGN</b></td><td style="text-align: right;"><b>35</b></td></tr>
      <tr><td></td><td>4.1 SYSTEM ARCHITECTURE</td><td style="text-align: right;">35</td></tr>
      <tr><td></td><td>4.2 DETAILED DESIGN AND OBJECT MODELING</td><td style="text-align: right;">38</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>5.</b></td><td><b>METHODOLOGY AND TESTING</b></td><td style="text-align: right;"><b>42</b></td></tr>
      <tr><td></td><td>5.1 MODULAR SUBSYSTEM FORMULATION</td><td style="text-align: right;">42</td></tr>
      <tr><td></td><td>5.2 ALGORITHMIC FORMULATION</td><td style="text-align: right;">45</td></tr>
      <tr><td></td><td>5.3 TESTING SUITE AND QUALITY ASSURANCE</td><td style="text-align: right;">50</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>6.</b></td><td><b>PROJECT IMPLEMENTATION</b></td><td style="text-align: right;"><b>54</b></td></tr>
      <tr><td></td><td>6.1 EXPERIMENTAL SETUP</td><td style="text-align: right;">54</td></tr>
      <tr><td></td><td>6.2 DATASET SPECIFICATION &amp; TELEMETRY CHARACTERISTICS</td><td style="text-align: right;">55</td></tr>
      <tr><td></td><td>6.3 ENSEMBLE RANDOM FOREST REGRESSOR MATHEMATICS</td><td style="text-align: right;">57</td></tr>
      <tr><td></td><td>6.4 GOOGLE GEMINI THINKING AI &amp; SUB-50MS ENGINE</td><td style="text-align: right;">60</td></tr>
      <tr><td></td><td>6.5 ISOCHRONIC 432 HZ WEB AUDIO NEURO-STABILIZER</td><td style="text-align: right;">62</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>7.</b></td><td><b>RESULTS AND DISCUSSION</b></td><td style="text-align: right;"><b>64</b></td></tr>
      <tr><td></td><td>7.1 USER INTERFACE &amp; EMPIRICAL SCREENSHOT ANALYSIS</td><td style="text-align: right;">64</td></tr>
      <tr><td></td><td>7.2 QUANTITATIVE EVALUATION &amp; REGRESSION BENCHMARKS</td><td style="text-align: right;">77</td></tr>
      <tr><td></td><td>7.3 LATENCY AND COMPUTATIONAL OVERHEAD PROFILING</td><td style="text-align: right;">80</td></tr>
      <tr><td></td><td>7.4 SOCIO-ECONOMIC FEASIBILITY &amp; COST METRICS</td><td style="text-align: right;">81</td></tr>

      <tr style="border-top: 1px solid #eee;"><td colspan="3" style="padding: 2px 0;"></td></tr>
      <tr><td><b>8.</b></td><td><b>CONCLUSION AND FUTURE ENHANCEMENTS</b></td><td style="text-align: right;"><b>83</b></td></tr>
      <tr><td></td><td>8.1 SUMMARY OF CONTRIBUTIONS</td><td style="text-align: right;">83</td></tr>
      <tr><td></td><td>8.2 RESEARCH LIMITATIONS</td><td style="text-align: right;">84</td></tr>
      <tr><td></td><td>8.3 FUTURE RESEARCH DIRECTIONS</td><td style="text-align: right;">85</td></tr>

      <tr style="border-top: 1px solid #ccc;"><td colspan="3" style="padding: 3px 0;"></td></tr>
      <tr><td></td><td><b>REFERENCES</b></td><td style="text-align: right;"><b>87</b></td></tr>
      <tr><td></td><td><b>APPENDIX A – SAMPLE SOURCE CODE</b></td><td style="text-align: right;"><b>92</b></td></tr>
      <tr><td></td><td><b>APPENDIX B – PUBLICATION AND DISSEMINATION DETAILS</b></td><td style="text-align: right;"><b>98</b></td></tr>
    </tbody>
  </table>
</div>
"""

LIST_OF_FIGURES_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 25px;">LIST OF FIGURES</h2>
  
  <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
    <thead>
      <tr style="border-bottom: 1.5px solid #000;">
        <th style="text-align: left; width: 18%; padding: 4px 0;">Figure No.</th>
        <th style="text-align: left; width: 67%; padding: 4px 0;">Title</th>
        <th style="text-align: right; width: 15%; padding: 4px 0;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Figure 3.1</td><td>Use Case Diagram: Multimodal Student Twin Platform</td><td style="text-align: right;">32</td></tr>
      <tr><td>Figure 3.2</td><td>Data Flow Diagram (DFD Level 1): Predictive Digital Twin Pipeline</td><td style="text-align: right;">33</td></tr>
      <tr><td>Figure 3.3</td><td>Finite State Machine: Student Cognitive and Risk State Dynamics</td><td style="text-align: right;">34</td></tr>
      <tr><td>Figure 4.1</td><td>Layered Cognitive Digital Twin Architecture</td><td style="text-align: right;">36</td></tr>
      <tr><td>Figure 4.2</td><td>Sequence Diagram: What-If Simulation and Copilot Intervention</td><td style="text-align: right;">39</td></tr>
      <tr><td>Figure 4.3</td><td>UML Class Diagram: Object Model of Digital Student Twin</td><td style="text-align: right;">40</td></tr>
      <tr><td>Figure 7.1</td><td>Monolithic Biometric and Credential Authentication Portal</td><td style="text-align: right;">65</td></tr>
      <tr><td>Figure 7.2</td><td>Comprehensive Cohort Health and Real-Time Performance Analytics Dashboard</td><td style="text-align: right;">66</td></tr>
      <tr><td>Figure 7.3</td><td>High-Performing Student Digital Twin Profile and Predictive Trajectory</td><td style="text-align: right;">67</td></tr>
      <tr><td>Figure 7.4</td><td>Dynamic Interactive "What-If" Counterfactual Simulation Studio</td><td style="text-align: right;">68</td></tr>
      <tr><td>Figure 7.5</td><td>High-Risk Student Digital Twin with Multimodal Alert Triggers</td><td style="text-align: right;">69</td></tr>
      <tr><td>Figure 7.6</td><td>Daily Student Psychological and Academic Telemetry Check-in Form</td><td style="text-align: right;">70</td></tr>
      <tr><td>Figure 7.7</td><td>Multidimensional Cohort Scatter Distribution (Study Hours vs. Projected Marks)</td><td style="text-align: right;">71</td></tr>
      <tr><td>Figure 7.8</td><td>Random Forest Feature Importance Pareto Distribution</td><td style="text-align: right;">72</td></tr>
      <tr><td>Figure 7.9</td><td>Global Student Registry and Real-Time Risk Categorization Matrix</td><td style="text-align: right;">73</td></tr>
      <tr><td>Figure 7.10</td><td>Sub-50ms Low-Latency Empathetic Student Copilot Interface</td><td style="text-align: right;">74</td></tr>
      <tr><td>Figure 7.11</td><td>Assistant Chat Counterfactual Recommendation and Simulation Card</td><td style="text-align: right;">75</td></tr>
      <tr><td>Figure 7.12</td><td>System Intelligence, Model Provenance, and Gemini API Configuration</td><td style="text-align: right;">76</td></tr>
      <tr><td>Figure 7.13</td><td>Floating Header 432 Hz Neuro-Acoustic Calming Audio Controller</td><td style="text-align: right;">77</td></tr>
    </tbody>
  </table>
  <p style="font-size: 10pt; text-align: center; margin-top: 30px; font-style: italic; color: #555;">
    (In the chapters, figure caption should come below the figure. Figure captions should be of font size 10 and centre aligned)
  </p>
</div>
"""

LIST_OF_TABLES_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 25px;">LIST OF TABLES</h2>
  
  <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
    <thead>
      <tr style="border-bottom: 1.5px solid #000;">
        <th style="text-align: left; width: 18%; padding: 4px 0;">Table No.</th>
        <th style="text-align: left; width: 67%; padding: 4px 0;">Title</th>
        <th style="text-align: right; width: 15%; padding: 4px 0;">Page No.</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Table 2.1</td><td>Comparative Analysis of State-of-the-Art Student Analytics &amp; Digital Twin Frameworks</td><td style="text-align: right;">12</td></tr>
      <tr><td>Table 2.2</td><td>Project Implementation Milestones and Work Breakdown Structure</td><td style="text-align: right;">21</td></tr>
      <tr><td>Table 3.1</td><td>Minimum and Recommended Hardware Specifications</td><td style="text-align: right;">30</td></tr>
      <tr><td>Table 3.2</td><td>Comprehensive Software Toolchain and Dependency Matrix</td><td style="text-align: right;">30</td></tr>
      <tr><td>Table 5.1</td><td>Algorithmic Scalability and Execution Profiles</td><td style="text-align: right;">49</td></tr>
      <tr><td>Table 5.2</td><td>Exhaustive System Test Suite and Verification Results</td><td style="text-align: right;">52</td></tr>
      <tr><td>Table 6.1</td><td>Multivariate Telemetry Schema &amp; Statistical Characteristics (N=600 Cohort)</td><td style="text-align: right;">56</td></tr>
      <tr><td>Table 6.2</td><td>Optimized Hyperparameter Grid for the Random Forest Ensemble</td><td style="text-align: right;">59</td></tr>
      <tr><td>Table 7.1</td><td>Comparative Predictive Performance of Supervised Regression Models</td><td style="text-align: right;">78</td></tr>
      <tr><td>Table 7.2</td><td>Latency Profiling Across Copilot Inference Modalities</td><td style="text-align: right;">80</td></tr>
      <tr><td>Table 7.3</td><td>Economic Deployment Feasibility and Cloud Infrastructure Cost Model</td><td style="text-align: right;">82</td></tr>
    </tbody>
  </table>
  <p style="font-size: 10pt; text-align: center; margin-top: 30px; font-style: italic; color: #555;">
    (In the chapters, table caption should come above the table. Table captions should be of font size 10 and centre aligned)
  </p>
</div>
"""

ABBREVIATIONS_AND_SYMBOLS_HTML = """
<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 25px;">LIST OF ABBREVIATIONS</h2>
  
  <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
    <thead>
      <tr style="border-bottom: 1px solid #000;">
        <th style="text-align: left; width: 25%; padding: 4px 0;">Abbreviation</th>
        <th style="text-align: left; width: 75%; padding: 4px 0;">Expanded Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><b>AI</b></td><td>Artificial Intelligence</td></tr>
      <tr><td><b>API</b></td><td>Application Programming Interface</td></tr>
      <tr><td><b>AUC</b></td><td>Area Under the Curve</td></tr>
      <tr><td><b>CORS</b></td><td>Cross-Origin Resource Sharing</td></tr>
      <tr><td><b>CPU</b></td><td>Central Processing Unit</td></tr>
      <tr><td><b>CSS</b></td><td>Cascading Style Sheets</td></tr>
      <tr><td><b>CSV</b></td><td>Comma-Separated Values</td></tr>
      <tr><td><b>DFD</b></td><td>Data Flow Diagram</td></tr>
      <tr><td><b>DOM</b></td><td>Document Object Model</td></tr>
      <tr><td><b>EDM</b></td><td>Educational Data Mining</td></tr>
      <tr><td><b>EEG</b></td><td>Electroencephalography</td></tr>
      <tr><td><b>FFT</b></td><td>Fast Fourier Transform</td></tr>
      <tr><td><b>GPA</b></td><td>Grade Point Average</td></tr>
      <tr><td><b>GPU</b></td><td>Graphics Processing Unit</td></tr>
      <tr><td><b>HTML</b></td><td>HyperText Markup Language</td></tr>
      <tr><td><b>HTTP</b></td><td>Hypertext Transfer Protocol</td></tr>
      <tr><td><b>IQR</b></td><td>Interquartile Range</td></tr>
      <tr><td><b>JSON</b></td><td>JavaScript Object Notation</td></tr>
      <tr><td><b>JWT</b></td><td>JSON Web Token</td></tr>
      <tr><td><b>LA</b></td><td>Learning Analytics</td></tr>
      <tr><td><b>LLM</b></td><td>Large Language Model</td></tr>
      <tr><td><b>MAE</b></td><td>Mean Absolute Error</td></tr>
      <tr><td><b>ML</b></td><td>Machine Learning</td></tr>
      <tr><td><b>MSE</b></td><td>Mean Squared Error</td></tr>
      <tr><td><b>NFR</b></td><td>Non-Functional Requirement</td></tr>
      <tr><td><b>OOB</b></td><td>Out-of-Bag (Sample Evaluation)</td></tr>
      <tr><td><b>PPG</b></td><td>Photoplethysmography</td></tr>
      <tr><td><b>RBAC</b></td><td>Role-Based Access Control</td></tr>
      <tr><td><b>REST</b></td><td>Representational State Transfer</td></tr>
      <tr><td><b>RF</b></td><td>Random Forest</td></tr>
      <tr><td><b>RMSE</b></td><td>Root Mean Squared Error</td></tr>
      <tr><td><b>ROC</b></td><td>Receiver Operating Characteristic</td></tr>
      <tr><td><b>SPA</b></td><td>Single Page Application</td></tr>
      <tr><td><b>UML</b></td><td>Unified Modeling Language</td></tr>
      <tr><td><b>UX</b></td><td>User Experience</td></tr>
      <tr><td><b>VAD</b></td><td>Valence-Arousal-Dominance</td></tr>
      <tr><td><b>WebGL</b></td><td>Web Graphics Library</td></tr>
      <tr><td><b>WHO</b></td><td>World Health Organization</td></tr>
    </tbody>
  </table>
  <p style="font-size: 10pt; text-align: center; margin-top: 15px; font-style: italic; color: #555;">
    Note: All the abbreviations follow strict alphabetical order.
  </p>
</div>

<div class="page" style="page-break-before: always;">
  <h2 class="chapter-title" style="text-align: center; font-size: 16pt; font-weight: bold; margin-bottom: 25px;">SYMBOLS AND NOTATIONS</h2>
  
  <table style="width: 100%; border-collapse: collapse; font-size: 12pt; line-height: 1.5;">
    <thead>
      <tr style="border-bottom: 1px solid #000;">
        <th style="text-align: left; width: 25%; padding: 4px 0;">Symbol</th>
        <th style="text-align: left; width: 75%; padding: 4px 0;">Definition / Mathematical Context</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><b><i>B</i></b></td><td>Number of bootstrap ensemble estimators (trees in the forest; default = 100)</td></tr>
      <tr><td><b><i>y<sub>i</sub></i></b></td><td>Ground truth academic marks for student <i>i</i> &isin; [0, 100]</td></tr>
      <tr><td><b><i>&#375;<sub>i</sub></i></b></td><td>Aggregated predictive marks computed across ensemble estimators</td></tr>
      <tr><td><b><i>T<sub>b</sub>(x)</i></b></td><td>Individual decision regression tree trained on bootstrap sample <i>b</i></td></tr>
      <tr><td><b><i>R<sup>2</sup></i></b></td><td>Coefficient of determination quantifying proportion of variance explained</td></tr>
      <tr><td><b><i>L<sub>MAE</sub></i></b></td><td>Mean Absolute Error loss metric across <i>N</i> cohort instances</td></tr>
      <tr><td><b><i>L<sub>RMSE</sub></i></b></td><td>Root Mean Squared Error penalizing larger deviation variances</td></tr>
      <tr><td><b><i>H</i></b></td><td>Weekly dedicated self-study allocation (hours/week)</td></tr>
      <tr><td><b><i>S</i></b></td><td>Reported nocturnal sleep duration (hours/night)</td></tr>
      <tr><td><b><i>&Psi;</i></b></td><td>Subjective academic and psychological stress index &isin; [1, 10]</td></tr>
      <tr><td><b><i>A</i></b></td><td>Aggregate institutional attendance percentage &isin; [0, 100]</td></tr>
      <tr><td><b><i>&Delta;<sub>x</sub></i></b></td><td>Counterfactual slider perturbation vector applied during What-If simulation</td></tr>
      <tr><td><b><i>f<sub>0</sub></i></b></td><td>Acoustic fundamental frequency (432.0 Hz harmonic tuning reference)</td></tr>
      <tr><td><b><i>I<sub>G</sub>(p)</i></b></td><td>Gini impurity metric utilized for optimal node splitting</td></tr>
      <tr><td><b><i>&sigma;<sup>2</sup></i></b></td><td>Variance across individual ensemble estimator predictions</td></tr>
      <tr><td><b><i>&theta;<sub>k</sub></i></b></td><td>Parameter split vector at internal tree node <i>k</i></td></tr>
    </tbody>
  </table>
</div>
"""
print("report_sections_prelims.py compiled.")
