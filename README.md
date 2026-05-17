Atomberg In-House Goal Setting and Tracking Portal
==================================================

An optimized, high-performance web tracking application designed to handle internal employee lifecycle goal alignment, validation parameters, and structured performance milestones. Built specifically to fulfill the core tracking pipeline with a zero infrastructure overhead execution model.

Technical Architecture Stack
----------------------------
* Application Framework: Python 3.x with Flask Micro-architecture
* Embedded Storage Layer: SQLite Engine (Full relational ACID-compliance, zero-cost cloud footprint)
* Frontend Interface Wrapper: Single-file HTML5 UI structured using utility-first Tailwind CSS
* Security Interceptor Layer: Automated business-rule validation pipeline

Implemented System Validation Parameters
---------------------------------------
The engine enforces specific business logic parameters before processing records into the reviewer tables:

1. Total Weightage Balance: The collective sum of goal weights inside a sheet must hit exactly 100%.
2. Minimum Weight Floor: Every single structural goal must carry a weight value of at least 10%.
3. Maximum Volume Boundary: An employee sheet is limited to a maximum of 8 individual goals.

Ready-to-Run Setup Instructions
-------------------------------

1. Initialize Local Requirements
Ensure you have Python installed on your local environment, then initialize the framework wrapper:
pip install flask

2. Launch the Application Server
Run the unified script file to build the self-contained SQLite tables and spin up the transaction pipeline listener:
python app.py

3. Connect and Execute Check-ins
* Local Web URL: Open http://127.0.0.1:8080 inside any web browser.
* Evaluation Engine Toggles: Tap the built-in action triggers to fire validation intercept benchmarks and read the real-time feedback response logs.

