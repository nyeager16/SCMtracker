WORK IN PROGRESS

Requires following modules:
bs4
selenium
pandas
numpy
ast

Requires ChromeDriver from:
https://chromedriver.chromium.org/downloads

Download and move "chromedriver.exe" to cscasetracker folder for correct version of Chrome.


To use:

Enter working directory in cmd

type "python scm.py [ARGUMENT]"

where [ARGUMENT] can be a CS2 case name as listed on the steam community market OR a group of cases
as defined in data.py.

Examples: 
python scm.py "Clutch Case"
python scm.py "active"

where "active" is a group of all active case drops.