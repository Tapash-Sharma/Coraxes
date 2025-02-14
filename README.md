###Coraxes
Coraxes is a easy-to-use, resource friendly and efficient cybersecurity tool designed to predict incoming mails as healthy or malicious by using Machine Learning Algorithms. The tool consists of two components: 
A Central Decision System 
An Input/Output Pipeline

####Central Decision System
The Central Decision System or CDS is the brains of Coraxes. This module is responsible for the processing tasks involved in the tool. It takes email features as inputs and based on the characteristics of those features classifies it as healthy or malicious. 
Components:
5 ML models [3 for prediction, 1 for ensemble, and 1 for learning]
Email Parser
Features:
- Breaks down the input into feature components
- Processes the features
- Provides the output

####Input/Output Pipeline
The Input/Output Pipeline is the heart of Coraxes. This module is responsible for the input and output processes of Coraxes. This module's whole feature is rooted around transportation of data. This module alerts the user in-real time, if suspicious mails are sent to the user. 
Components:
Discord Bot
Flask API
Features: 
- Accepts input from the user
- Provides the input to the CDS
- Provides the output to the user
- Consists of the real-time alert system

####Requirements 
Discord Account 
Cloudfare Account [Other compatible services can too be used in the I/O pipeline instead of Cloudfare]
Docker 
Flask Framework
Scikit Library
NumPy
Pandas
[And other requirements like notebooks and code editors which are not case specific]

####Installation 
- Download the files from GitHub 
- Edit the discord token in main.py to your personal static discord token
- run main.py

####Note
The current version of the tool only supports custom email addresses. the current address for the tool is tapash@unthinkable.me. The way the tool works is that you forward incoming emails to the aforementioned address. 

Thank you for visiting my project page. 
