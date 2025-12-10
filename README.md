# Client-Query-Management
Project aims to provide a real-time interface for clients to submit queries and for support teams to manage them efficiently.

This client query management portal is a full-stack web application built with Streamlit, Python, MySQL, and pandas to streamline handling client inquiries, support tickets, and admin tasks for freelance or small business use.

Project Overview
The app serves as a centralized dashboard for logging, viewing, executing, and managing client queries. It features role-based pages (e.g., support/admin views), form inputs like multiselect and checkboxes for query selection, and dynamic display of SQL query results fetched from a MySQL database.

Development Approach
Development occurred in VS Code on Windows, starting with MySQL schema setup using mysql-connector for connectivity. Key steps included designing tables for queries/storage, implementing password hashing with hashlib for basic authentication, and using pandas to process/execute SQL queries pulled from the database. Recent enhancements involved schema tweaks (e.g., converting integer to varchar columns, handling primary keys/auto-increment) and building interactive Streamlit pages for query fetching, execution, and result visualization.

Setup and running
Installation & Setup: Steps to clone the repo, create a virtual environment, install requirements, and ensure MySQL is running and accessible.​

Database Configuration: Instructions to create the database and tables, update connection details, and optionally load initial data (e.g., past queries from CSV into MySQL).​

How to Run: Exact Streamlit commands to run register.py and login.py, plus a short note on the login flow (register, then log in, then redirected as Client or Support
