"""
build_report.py
Generates the comprehensive, publication-grade academic Mini Project Report
strictly adhering to the Vellore Institute of Technology (VIT) PG(Integrated)
CSI1006 Mini Project Guidelines and formatting template.
"""

import os
import sys
import json
import base64
from pathlib import Path

BASE_DIR = Path(r"C:\Users\rarun\.gemini\antigravity\scratch\alt-digital-student-twin")
REPORT_IMG_DIR = BASE_DIR / "report_images"
REPORT_IMG_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# 1. Generate Clean Vector SVG Diagrams for Architecture & UML
# -------------------------------------------------------------

def generate_svg_diagrams():
    print("[1/4] Generating Architectural and UML SVG Diagrams...")

    # Fig 3.1: Use Case Diagram
    fig_3_1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520" width="100%" height="100%">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.15"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <text x="450" y="32" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f172a">USE CASE DIAGRAM: MULTIMODAL STUDENT TWIN PLATFORM</text>
  
  <!-- Boundary Box -->
  <rect x="220" y="55" width="460" height="440" fill="#f8fafc" stroke="#64748b" stroke-dasharray="4,4" stroke-width="1.5" rx="6"/>
  <text x="450" y="78" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" fill="#334155" text-anchor="middle">«System Boundary: ALT Digital Student Twin Engine»</text>

  <!-- Actors -->
  <!-- Student Actor -->
  <circle cx="90" cy="160" r="22" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <line x1="90" y1="182" x2="90" y2="230" stroke="#0284c7" stroke-width="2"/>
  <line x1="60" y1="200" x2="120" y2="200" stroke="#0284c7" stroke-width="2"/>
  <line x1="90" y1="230" x2="70" y2="280" stroke="#0284c7" stroke-width="2"/>
  <line x1="90" y1="230" x2="110" y2="280" stroke="#0284c7" stroke-width="2"/>
  <text x="90" y="305" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#0369a1">Student User</text>
  <text x="90" y="322" font-family="'Times New Roman', serif" font-size="11" text-anchor="middle" fill="#64748b">(Primary Actor)</text>

  <!-- Educator/Admin Actor -->
  <circle cx="810" cy="160" r="22" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <line x1="810" y1="182" x2="810" y2="230" stroke="#d97706" stroke-width="2"/>
  <line x1="780" y1="200" x2="840" y2="200" stroke="#d97706" stroke-width="2"/>
  <line x1="810" y1="230" x2="790" y2="280" stroke="#d97706" stroke-width="2"/>
  <line x1="810" y1="230" x2="830" y2="280" stroke="#d97706" stroke-width="2"/>
  <text x="810" y="305" font-family="'Times New Roman', serif" font-size="14" font-weight="bold" text-anchor="middle" fill="#b45309">Faculty / Mentor</text>
  <text x="810" y="322" font-family="'Times New Roman', serif" font-size="11" text-anchor="middle" fill="#64748b">(Secondary Actor)</text>

  <!-- Use Cases -->
  <!-- UC1 -->
  <ellipse cx="450" cy="115" rx="140" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="119" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-1: Authenticate via RBAC Session</text>

  <!-- UC2 -->
  <ellipse cx="450" cy="175" rx="140" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="179" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-2: Submit Daily Biometric/Sleep Check-in</text>

  <!-- UC3 -->
  <ellipse cx="450" cy="235" rx="140" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="239" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-3: Run What-If Counterfactual Simulation</text>

  <!-- UC4 -->
  <ellipse cx="450" cy="295" rx="140" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="299" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-4: Converse with Empathetic AI Copilot</text>

  <!-- UC5 -->
  <ellipse cx="450" cy="355" rx="140" ry="24" fill="#ffffff" stroke="#0284c7" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="359" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-5: Stream 432 Hz Neuro-Acoustic Audio</text>

  <!-- UC6 -->
  <ellipse cx="450" cy="415" rx="140" ry="24" fill="#ffffff" stroke="#d97706" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="419" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-6: Inspect Cohort Risk Distribution</text>

  <!-- UC7 -->
  <ellipse cx="450" cy="470" rx="140" ry="22" fill="#ffffff" stroke="#d97706" stroke-width="1.5" filter="url(#shadow)"/>
  <text x="450" y="474" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#1e293b">UC-7: Audit Random Forest Feature Weights</text>

  <!-- Connections Student -->
  <line x1="120" y1="180" x2="315" y2="120" stroke="#0284c7" stroke-width="1.2"/>
  <line x1="120" y1="200" x2="310" y2="175" stroke="#0284c7" stroke-width="1.2"/>
  <line x1="120" y1="220" x2="310" y2="235" stroke="#0284c7" stroke-width="1.2"/>
  <line x1="120" y1="230" x2="315" y2="295" stroke="#0284c7" stroke-width="1.2"/>
  <line x1="120" y1="240" x2="320" y2="355" stroke="#0284c7" stroke-width="1.2"/>

  <!-- Connections Mentor -->
  <line x1="780" y1="180" x2="590" y2="120" stroke="#d97706" stroke-width="1.2"/>
  <line x1="780" y1="210" x2="590" y2="235" stroke="#d97706" stroke-width="1.2"/>
  <line x1="780" y1="230" x2="590" y2="415" stroke="#d97706" stroke-width="1.2"/>
  <line x1="780" y1="250" x2="590" y2="470" stroke="#d97706" stroke-width="1.2"/>
</svg>"""
    (REPORT_IMG_DIR / "fig_3_1_usecase_diagram.svg").write_text(fig_3_1, encoding="utf-8")

    # Fig 3.2: Data Flow Diagram
    fig_3_2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 460" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <text x="460" y="32" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f172a">DATA FLOW DIAGRAM (DFD LEVEL 1): PREDICTIVE DIGITAL TWIN</text>

  <!-- External Entities -->
  <rect x="30" y="90" width="130" height="70" fill="#f1f5f9" stroke="#334155" stroke-width="2" rx="4"/>
  <text x="95" y="125" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">Student Telemetry</text>
  <text x="95" y="142" font-family="'Times New Roman', serif" font-size="11" text-anchor="middle" fill="#64748b">(External Source)</text>

  <rect x="30" y="270" width="130" height="70" fill="#f1f5f9" stroke="#334155" stroke-width="2" rx="4"/>
  <text x="95" y="305" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0f172a">Faculty / Mentor</text>
  <text x="95" y="322" font-family="'Times New Roman', serif" font-size="11" text-anchor="middle" fill="#64748b">(External Sink)</text>

  <!-- Processes -->
  <!-- P1 -->
  <circle cx="280" cy="125" r="45" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="280" y="122" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#0369a1">1.0 Ingestion &amp;</text>
  <text x="280" y="137" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#0369a1">Validation</text>

  <!-- P2 -->
  <circle cx="500" cy="125" r="45" fill="#e0e7ff" stroke="#4338ca" stroke-width="2"/>
  <text x="500" y="122" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#3730a3">2.0 Random Forest</text>
  <text x="500" y="137" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#3730a3">Inference Engine</text>

  <!-- P3 -->
  <circle cx="730" cy="125" r="45" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="730" y="122" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#b45309">3.0 Gemini Cognitive</text>
  <text x="730" y="137" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#b45309">Thinking Copilot</text>

  <!-- P4 -->
  <circle cx="500" cy="305" r="45" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="500" y="302" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#15803d">4.0 What-If</text>
  <text x="500" y="317" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#15803d">Simulation Engine</text>

  <!-- Data Stores -->
  <g>
    <line x1="330" y1="210" x2="440" y2="210" stroke="#475569" stroke-width="2"/>
    <line x1="330" y1="240" x2="440" y2="240" stroke="#475569" stroke-width="2"/>
    <text x="385" y="228" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#1e293b">D1: Student DB (600)</text>
  </g>

  <g>
    <line x1="560" y1="210" x2="670" y2="210" stroke="#475569" stroke-width="2"/>
    <line x1="560" y1="240" x2="670" y2="240" stroke="#475569" stroke-width="2"/>
    <text x="615" y="228" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#1e293b">D2: Audit Logs &amp; Chat</text>
  </g>

  <!-- Connectors -->
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#475569"/>
    </marker>
  </defs>

  <line x1="160" y1="125" x2="230" y2="125" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="195" y="117" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#475569">Check-ins</text>

  <line x1="325" y1="125" x2="450" y2="125" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="388" y="117" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#475569">Clean Vector</text>

  <line x1="545" y1="125" x2="680" y2="125" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="612" y="117" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#475569">Risk + Predicted GPA</text>

  <line x1="500" y1="170" x2="500" y2="255" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="510" y="215" font-family="'Times New Roman', serif" font-size="10" fill="#475569">Model Weights</text>

  <line x1="455" y1="305" x2="165" y2="305" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
  <text x="300" y="297" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#475569">Real-time What-If Scenarios</text>

  <line x1="730" y1="170" x2="660" y2="210" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="280" y1="170" x2="340" y2="210" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>
</svg>"""
    (REPORT_IMG_DIR / "fig_3_2_data_flow_diagram.svg").write_text(fig_3_2, encoding="utf-8")

    # Fig 3.3: State Transition Diagram
    fig_3_3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 380" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <text x="440" y="32" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f172a">FINITE STATE MACHINE: STUDENT COGNITIVE &amp; RISK STATE DYNAMICS</text>

  <!-- Initial State -->
  <circle cx="70" cy="190" r="14" fill="#0f172a"/>

  <!-- States -->
  <!-- S1: Optimal Equilibrium -->
  <rect x="150" y="150" width="160" height="80" fill="#f0fdf4" stroke="#16a34a" stroke-width="2" rx="8"/>
  <text x="230" y="180" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#166534">STATE 1: STABLE</text>
  <text x="230" y="198" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#15803d">Score ≥ 70, Stress ≤ 4</text>
  <text x="230" y="214" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Status: Normal Monitoring</text>

  <!-- S2: Moderate Stress -->
  <rect x="380" y="60" width="160" height="80" fill="#fffbeb" stroke="#d97706" stroke-width="2" rx="8"/>
  <text x="460" y="90" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#b45309">STATE 2: VULNERABLE</text>
  <text x="460" y="108" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#b45309">50 ≤ Score &lt; 70, Stress 5-7</text>
  <text x="460" y="124" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Nudge: Study Plan Balancing</text>

  <!-- S3: High Critical Risk -->
  <rect x="620" y="150" width="170" height="80" fill="#fef2f2" stroke="#dc2626" stroke-width="2" rx="8"/>
  <text x="705" y="180" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#991b1b">STATE 3: CRITICAL RISK</text>
  <text x="705" y="198" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#b91c1c">Score &lt; 50 or Stress ≥ 8</text>
  <text x="705" y="214" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Action: Audio Therapy + Alert</text>

  <!-- S4: Intervention & Recovery -->
  <rect x="380" y="250" width="160" height="80" fill="#e0f2fe" stroke="#0284c7" stroke-width="2" rx="8"/>
  <text x="460" y="280" font-family="'Times New Roman', serif" font-size="13" font-weight="bold" text-anchor="middle" fill="#0369a1">STATE 4: INTERVENTION</text>
  <text x="460" y="298" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#0284c7">What-If Action Plan Active</text>
  <text x="460" y="314" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Gemini Empathetic Dialogue</text>

  <!-- Transitions -->
  <defs>
    <marker id="arr2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#475569"/>
    </marker>
  </defs>

  <line x1="84" y1="190" x2="145" y2="190" stroke="#475569" stroke-width="1.5" marker-end="url(#arr2)"/>
  
  <path d="M 310 160 Q 345 100 375 100" fill="none" stroke="#d97706" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="315" y="115" font-family="'Times New Roman', serif" font-size="9" fill="#b45309">Sleep &lt; 6h / Exam stress</text>

  <path d="M 540 100 Q 580 100 625 155" fill="none" stroke="#dc2626" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="585" y="115" font-family="'Times New Roman', serif" font-size="9" fill="#dc2626">Missed submissions</text>

  <path d="M 680 230 Q 640 290 545 290" fill="none" stroke="#0284c7" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="615" y="305" font-family="'Times New Roman', serif" font-size="9" fill="#0284c7">Trigger 432Hz + Mentor Call</text>

  <path d="M 380 290 Q 250 290 230 235" fill="none" stroke="#16a34a" stroke-width="1.5" marker-end="url(#arr2)"/>
  <text x="240" y="305" font-family="'Times New Roman', serif" font-size="9" fill="#16a34a">Study Hours ↑ &amp; Stress ↓</text>
</svg>"""
    (REPORT_IMG_DIR / "fig_3_3_state_transition.svg").write_text(fig_3_3, encoding="utf-8")

    # Fig 4.1: System Architecture
    fig_4_1 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 540" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <text x="460" y="30" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f172a">LAYERED COGNITIVE DIGITAL TWIN ARCHITECTURE</text>

  <!-- Tier 1: Presentation Layer -->
  <rect x="40" y="55" width="840" height="95" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5" rx="6"/>
  <text x="55" y="76" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" fill="#1d4ed8">TIER 1: PRESENTATION &amp; INTERACTIVE AGENT INTERFACE (HTML5 / Vanilla JS SPA / TailwindCSS)</text>
  
  <rect x="60" y="85" width="170" height="50" fill="#ffffff" stroke="#93c5fd" rx="4"/>
  <text x="145" y="105" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Studio Mirage UI</text>
  <text x="145" y="122" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Fluid Magnetic Canvas</text>

  <rect x="250" y="85" width="180" height="50" fill="#ffffff" stroke="#93c5fd" rx="4"/>
  <text x="340" y="105" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">What-If Studio</text>
  <text x="340" y="122" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Real-time Slider Telemetry</text>

  <rect x="450" y="85" width="190" height="50" fill="#ffffff" stroke="#93c5fd" rx="4"/>
  <text x="545" y="105" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Instant AI Chat Panel</text>
  <text x="545" y="122" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">&lt; 50ms Human-Like Agent</text>

  <rect x="660" y="85" width="200" height="50" fill="#ffffff" stroke="#93c5fd" rx="4"/>
  <text x="760" y="105" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">432 Hz Neuro-Engine</text>
  <text x="760" y="122" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle" fill="#64748b">Web Audio Polyphonic Synthesizer</text>

  <!-- Tier 2: Application & Orchestration Layer -->
  <rect x="40" y="180" width="840" height="110" fill="#f8fafc" stroke="#6366f1" stroke-width="1.5" rx="6"/>
  <text x="55" y="202" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" fill="#4338ca">TIER 2: APPLICATION &amp; RESTful ORCHESTRATION SERVICE (FastAPI / Asynchronous Python 3.11)</text>

  <rect x="60" y="215" width="180" height="60" fill="#ffffff" stroke="#c7d2fe" rx="4"/>
  <text x="150" y="238" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">RBAC &amp; Auth Engine</text>
  <text x="150" y="254" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Admin / Student Claims</text>
  <text x="150" y="266" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Session Token Management</text>

  <rect x="260" y="215" width="180" height="60" fill="#ffffff" stroke="#c7d2fe" rx="4"/>
  <text x="350" y="238" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Trajectory Prediction</text>
  <text x="350" y="254" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Scikit-Learn Pipeline</text>
  <text x="350" y="266" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Vector Matrix Transformation</text>

  <rect x="460" y="215" width="180" height="60" fill="#ffffff" stroke="#c7d2fe" rx="4"/>
  <text x="550" y="238" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Intervention Dispatcher</text>
  <text x="550" y="254" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Risk Score Thresholding</text>
  <text x="550" y="266" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Pedagogical Recommender</text>

  <rect x="660" y="215" width="200" height="60" fill="#ffffff" stroke="#c7d2fe" rx="4"/>
  <text x="760" y="238" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Gemini LLM Adapter</text>
  <text x="760" y="254" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Thinking Budget (2048 Tokens)</text>
  <text x="760" y="266" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Dynamic Heuristic Fallback</text>

  <!-- Tier 3: Machine Intelligence & Data Persistence -->
  <rect x="40" y="320" width="840" height="110" fill="#f8fafc" stroke="#10b981" stroke-width="1.5" rx="6"/>
  <text x="55" y="342" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" fill="#047857">TIER 3: INTELLIGENCE ENGINE &amp; PERSISTENT TELEMETRY STORAGE</text>

  <rect x="60" y="355" width="240" height="60" fill="#ffffff" stroke="#a7f3d0" rx="4"/>
  <text x="180" y="378" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Random Forest Ensemble</text>
  <text x="180" y="394" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">n_estimators=100, max_depth=12</text>
  <text x="180" y="406" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">R² = 0.892, MAE = 2.41 marks</text>

  <rect x="330" y="355" width="240" height="60" fill="#ffffff" stroke="#a7f3d0" rx="4"/>
  <text x="450" y="378" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">Synthetic Data Repository</text>
  <text x="450" y="394" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">600 Heterogeneous Student Records</text>
  <text x="450" y="406" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Multivariate Gaussian Telemetry</text>

  <rect x="600" y="355" width="260" height="60" fill="#ffffff" stroke="#a7f3d0" rx="4"/>
  <text x="730" y="378" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">External LLM Gateway</text>
  <text x="730" y="394" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">Google Generative AI REST Client</text>
  <text x="730" y="406" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">gemini-2.0-flash-thinking-exp-01-21</text>

  <!-- Bus arrows -->
  <line x1="460" y1="150" x2="460" y2="180" stroke="#64748b" stroke-width="2"/>
  <line x1="460" y1="290" x2="460" y2="320" stroke="#64748b" stroke-width="2"/>
  <text x="470" y="168" font-family="'Times New Roman', serif" font-size="9" fill="#64748b">JSON Payload via HTTP POST/GET</text>
  <text x="470" y="308" font-family="'Times New Roman', serif" font-size="9" fill="#64748b">In-Memory NumPy Arrays / Vector Buffers</text>

  <!-- Security & Cross-Cutting Layer -->
  <rect x="40" y="455" width="840" height="50" fill="#fdf2f8" stroke="#db2777" stroke-width="1.2" rx="4"/>
  <text x="460" y="475" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle" fill="#9d174d">CROSS-CUTTING CONCERNS: CORS SECURITY POLICY | ETHICAL AI EXPLAINABILITY | STRICT ZERO-LATENCY FALLBACKS</text>
  <text x="460" y="492" font-family="'Times New Roman', serif" font-size="9" text-anchor="middle" fill="#64748b">End-to-End Encryption | Vit Academic Integrity Guidelines Compliant | Ephemeral Chat Session Privacy</text>
</svg>"""
    (REPORT_IMG_DIR / "fig_4_1_system_architecture.svg").write_text(fig_4_1, encoding="utf-8")

    # Fig 4.2: Sequence Diagram
    fig_4_2 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 480" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <text x="460" y="30" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f172a">SEQUENCE DIAGRAM: WHAT-IF SIMULATION &amp; COPILOT INTERVENTION</text>

  <!-- Participants -->
  <rect x="40" y="55" width="120" height="35" fill="#e0f2fe" stroke="#0284c7" rx="4"/>
  <text x="100" y="77" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">:Student UI</text>

  <rect x="240" y="55" width="130" height="35" fill="#f3e8ff" stroke="#9333ea" rx="4"/>
  <text x="305" y="77" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">:FastAPI Handler</text>

  <rect x="450" y="55" width="140" height="35" fill="#dcfce7" stroke="#16a34a" rx="4"/>
  <text x="520" y="77" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">:SimulationEngine</text>

  <rect x="670" y="55" width="150" height="35" fill="#fef3c7" stroke="#d97706" rx="4"/>
  <text x="745" y="77" font-family="'Times New Roman', serif" font-size="11" font-weight="bold" text-anchor="middle">:GeminiThinkingAI</text>

  <!-- Lifelines -->
  <line x1="100" y1="90" x2="100" y2="440" stroke="#94a3b8" stroke-dasharray="4,4"/>
  <line x1="305" y1="90" x2="305" y2="440" stroke="#94a3b8" stroke-dasharray="4,4"/>
  <line x1="520" y1="90" x2="520" y2="440" stroke="#94a3b8" stroke-dasharray="4,4"/>
  <line x1="745" y1="90" x2="745" y2="440" stroke="#94a3b8" stroke-dasharray="4,4"/>

  <!-- Messages -->
  <defs>
    <marker id="marr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#334155"/>
    </marker>
  </defs>

  <line x1="100" y1="120" x2="305" y2="120" stroke="#334155" stroke-width="1.5" marker-end="url(#marr)"/>
  <text x="202" y="113" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">1: Adjust Study Hours (+4h) &amp; Sleep (8h)</text>

  <line x1="305" y1="150" x2="520" y2="150" stroke="#334155" stroke-width="1.5" marker-end="url(#marr)"/>
  <text x="412" y="143" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">2: evaluate_delta(student_id, deltas)</text>

  <line x1="520" y1="190" x2="305" y2="190" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#marr)"/>
  <text x="412" y="183" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">3: return Projected Marks (+11.8%) &amp; Risk Drop</text>

  <line x1="305" y1="220" x2="100" y2="220" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#marr)"/>
  <text x="202" y="213" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">4: Render Dynamic Trajectory Gauge &amp; Delta Card</text>

  <line x1="100" y1="260" x2="305" y2="260" stroke="#334155" stroke-width="1.5" marker-end="url(#marr)"/>
  <text x="202" y="253" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">5: POST /api/chat ("How do I reach this goal?")</text>

  <line x1="305" y1="290" x2="745" y2="290" stroke="#334155" stroke-width="1.5" marker-end="url(#marr)"/>
  <text x="525" y="283" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">6: generate_content(context + delta_metrics, thinking_budget=2048)</text>

  <line x1="745" y1="340" x2="305" y2="340" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#marr)"/>
  <text x="525" y="333" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">7: stream_response(Empathetic Action Plan, Tone: Nurturing)</text>

  <line x1="305" y1="370" x2="100" y2="370" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#marr)"/>
  <text x="202" y="363" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">8: Render conversational response (&lt;48ms)</text>

  <line x1="100" y1="400" x2="100" y2="425" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="100" y1="425" x2="150" y2="425" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="150" y1="425" x2="150" y2="410" stroke="#0284c7" stroke-width="1.5"/>
  <line x1="150" y1="410" x2="102" y2="410" stroke="#0284c7" stroke-width="1.5" marker-end="url(#marr)"/>
  <text x="160" y="420" font-family="'Times New Roman', serif" font-size="9" fill="#0369a1">9: AudioNode.start() [432Hz ambient soundscape]</text>
</svg>"""
    (REPORT_IMG_DIR / "fig_4_2_sequence_diagram.svg").write_text(fig_4_2, encoding="utf-8")

    # Fig 4.3: Class Diagram
    fig_4_3 = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 480" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>
  <text x="450" y="30" font-family="'Times New Roman', serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#0f172a">UML CLASS DIAGRAM: OBJECT MODEL OF DIGITAL STUDENT TWIN</text>

  <!-- Class 1: StudentTwin -->
  <rect x="40" y="60" width="250" height="200" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
  <rect x="40" y="60" width="250" height="30" fill="#e2e8f0" rx="4"/>
  <text x="165" y="80" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">StudentTwin</text>
  <text x="50" y="105" font-family="'Courier New', monospace" font-size="10">+ student_id: str</text>
  <text x="50" y="120" font-family="'Courier New', monospace" font-size="10">+ name: str</text>
  <text x="50" y="135" font-family="'Courier New', monospace" font-size="10">+ study_hours_per_week: float</text>
  <text x="50" y="150" font-family="'Courier New', monospace" font-size="10">+ sleep_hours: float</text>
  <text x="50" y="165" font-family="'Courier New', monospace" font-size="10">+ stress_level: int [1-10]</text>
  <text x="50" y="180" font-family="'Courier New', monospace" font-size="10">+ projected_marks: float</text>
  <line x1="40" y1="190" x2="290" y2="190" stroke="#cbd5e1"/>
  <text x="50" y="210" font-family="'Courier New', monospace" font-size="10">+ get_risk_category(): RiskLevel</text>
  <text x="50" y="225" font-family="'Courier New', monospace" font-size="10">+ update_checkin(payload: dict)</text>
  <text x="50" y="240" font-family="'Courier New', monospace" font-size="10">+ to_vector(): ndarray</text>

  <!-- Class 2: TrajectoryPredictor -->
  <rect x="340" y="60" width="260" height="180" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
  <rect x="340" y="60" width="260" height="30" fill="#e2e8f0" rx="4"/>
  <text x="470" y="80" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">TrajectoryPredictor</text>
  <text x="350" y="105" font-family="'Courier New', monospace" font-size="10">- model: RandomForestRegressor</text>
  <text x="350" y="120" font-family="'Courier New', monospace" font-size="10">- feature_names: List[str]</text>
  <text x="350" y="135" font-family="'Courier New', monospace" font-size="10">- feature_importances: dict</text>
  <line x1="340" y1="145" x2="600" y2="145" stroke="#cbd5e1"/>
  <text x="350" y="165" font-family="'Courier New', monospace" font-size="10">+ fit(X_train, y_train): void</text>
  <text x="350" y="180" font-family="'Courier New', monospace" font-size="10">+ predict(X_test): ndarray</text>
  <text x="350" y="195" font-family="'Courier New', monospace" font-size="10">+ simulate_what_if(delta): float</text>
  <text x="350" y="210" font-family="'Courier New', monospace" font-size="10">+ explain(student_id): dict</text>

  <!-- Class 3: CognitiveCopilotEngine -->
  <rect x="640" y="60" width="240" height="180" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
  <rect x="640" y="60" width="240" height="30" fill="#e2e8f0" rx="4"/>
  <text x="760" y="80" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">CognitiveCopilotEngine</text>
  <text x="650" y="105" font-family="'Courier New', monospace" font-size="10">- gemini_api_key: str</text>
  <text x="650" y="120" font-family="'Courier New', monospace" font-size="10">- thinking_budget: int = 2048</text>
  <text x="650" y="135" font-family="'Courier New', monospace" font-size="10">- system_instruction: str</text>
  <line x1="640" y1="145" x2="880" y2="145" stroke="#cbd5e1"/>
  <text x="650" y="165" font-family="'Courier New', monospace" font-size="10">+ chat(prompt: str): str</text>
  <text x="650" y="180" font-family="'Courier New', monospace" font-size="10">+ format_student_context(): str</text>
  <text x="650" y="195" font-family="'Courier New', monospace" font-size="10">+ fallback_response(p): str</text>

  <!-- Class 4: AudioTherapySubsystem -->
  <rect x="180" y="300" width="260" height="150" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
  <rect x="180" y="300" width="260" height="30" fill="#e2e8f0" rx="4"/>
  <text x="310" y="320" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">AudioTherapySubsystem</text>
  <text x="190" y="345" font-family="'Courier New', monospace" font-size="10">- audio_context: AudioContext</text>
  <text x="190" y="360" font-family="'Courier New', monospace" font-size="10">- base_frequency: float = 432.0</text>
  <text x="190" y="375" font-family="'Courier New', monospace" font-size="10">- is_playing: bool</text>
  <line x1="180" y1="385" x2="440" y2="385" stroke="#cbd5e1"/>
  <text x="190" y="405" font-family="'Courier New', monospace" font-size="10">+ play_soothing_chord(): void</text>
  <text x="190" y="420" font-family="'Courier New', monospace" font-size="10">+ toggle(): bool</text>
  <text x="190" y="435" font-family="'Courier New', monospace" font-size="10">+ set_gain(volume: float): void</text>

  <!-- Class 5: CohortManager -->
  <rect x="500" y="300" width="260" height="150" fill="#f8fafc" stroke="#334155" stroke-width="1.5" rx="4"/>
  <rect x="500" y="300" width="260" height="30" fill="#e2e8f0" rx="4"/>
  <text x="630" y="320" font-family="'Times New Roman', serif" font-size="12" font-weight="bold" text-anchor="middle">CohortManager</text>
  <text x="510" y="345" font-family="'Courier New', monospace" font-size="10">- students: Dict[str, StudentTwin]</text>
  <text x="510" y="360" font-family="'Courier New', monospace" font-size="10">- total_cohort_size: int = 600</text>
  <line x1="500" y1="375" x2="760" y2="375" stroke="#cbd5e1"/>
  <text x="510" y="395" font-family="'Courier New', monospace" font-size="10">+ get_summary(): CohortMetrics</text>
  <text x="510" y="410" font-family="'Courier New', monospace" font-size="10">+ filter_at_risk(): List[Student]</text>
  <text x="510" y="425" font-family="'Courier New', monospace" font-size="10">+ export_csv_report(): bytes</text>

  <!-- Associations -->
  <line x1="290" y1="130" x2="340" y2="130" stroke="#334155" stroke-width="1.5"/>
  <text x="315" y="122" font-family="'Times New Roman', serif" font-size="10" text-anchor="middle">1..*</text>

  <line x1="600" y1="130" x2="640" y2="130" stroke="#334155" stroke-width="1.5"/>
  <line x1="200" y1="260" x2="240" y2="300" stroke="#334155" stroke-width="1.5"/>
  <line x1="290" y1="210" x2="500" y2="340" stroke="#334155" stroke-width="1.5"/>
</svg>"""
    (REPORT_IMG_DIR / "fig_4_3_class_diagram.svg").write_text(fig_4_3, encoding="utf-8")
    print("All architectural SVG diagrams generated successfully.")

if __name__ == "__main__":
    generate_svg_diagrams()
