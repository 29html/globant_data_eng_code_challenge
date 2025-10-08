# Globant Data Engineering Code Challenge
This is a engineering coding challenge

# CSV Uploader to Database
This Python Flask application provides a simple API for uploading CSV files and storing their data into a specified SQL table. It's particularly useful for processing large CSV files that may not fit entirely in memory.

# Features
1. CSV Upload: Allows users to upload CSV files via HTTP POST requests.
2. Dynamic Table Selection: Enables users to specify the target SQL table where the CSV data will be inserted.
3. Efficient Processing: Utilizes pandas to read CSV files in chunks for efficient processing, especially with large files.
4. Validation: Ensures the validity of the provided table name and the presence of the uploaded file.
5. Error Handling: Provides informative error messages for missing parameters, invalid table names, and no file selected scenarios.

   
# Installation
## Clone this repository to your local machine:
https://github.com/29html/gbecc.git

  
## Install the required dependencies using pip:
pip install -r requirements.txt

Set up your PostgreSQL database and update the DATABASE_URI variable in app.py with your database connection details.

Usage
Start the Flask server by running the following command:


python app.py
Make POST requests to the /upload-csv endpoint with the following parameters:

file: The CSV file to be uploaded. Expected as part of the multipart/form-data under the "file" key.
table_name: The name of the target SQL table where the CSV content will be stored. Passed as a form parameter.
Example using cURL:


curl -X POST -F "file=@/path/to/your/file.csv" -F "table_name=your_table_name" http://localhost:5000/upload-csv
# API Documentation
/upload-csv Endpoint
Method: POST
Uploads a CSV file and inserts its data into a specified table.

# Parameters:
file (FileStorage): The CSV file uploaded via HTTP request. Expected as part of the multipart/form-data under the "file" key.
table_name (str): The name of the target table where the CSV content will be stored. Passed as a form parameter.

# Responses:
200 OK: If the file was successfully uploaded and inserted into the specified table.
Response Body: { "message": "File uploaded and inserted in <table_name> table successfully" }
400 Bad Request: If there are missing parameters, an invalid table name, or no file selected.
Response Body: { "error": "<error_message>" }