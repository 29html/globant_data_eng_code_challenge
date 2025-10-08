from io import StringIO

import pandas as pd
from flask import Flask, request, jsonify
from sqlalchemy import create_engine

app = Flask(__name__)

DATABASE_URI = "postgresql+psycopg2://user:password@localhost:5432/globant_db"
engine = create_engine(url=DATABASE_URI)
tables = ["departments", "jobs", "employees"]


def is_valid_table(table_name) -> bool:
    """
    Checks if the provided table name is valid.

    Determines whether the table name given as input is among a predefined list of valid table names.

    Parameters:
    - table_name (str): The name of the table to be validated.

    Returns:
    - bool: True if the table name is valid (i.e., it is one of the predefined valid names); False otherwise.

    The function supports validation for a fixed set of table names: "departments", "jobs", and "employees".
    """
    return table_name in tables


def read_csv(file_stream) -> object:
    """
    Reads a CSV file from a file stream in chunks.

    This function utilizes pandas to read a CSV file provided via a file stream, dividing the file into chunks for efficient processing.

    Parameters:
    - file_stream (IO): The file stream of the CSV file to be read.

    Returns:
    - Iterator[pd.DataFrame]: An iterator that yields chunks of the CSV file as pandas DataFrames, each chunk being of size 1000 rows.

    This approach is particularly useful for processing large CSV files that may not fit entirely in memory.
    """
    return pd.read_csv(file_stream, chunksize=1000)


def store_data(df, table_name) -> object:
    """
    Stores a pandas DataFrame into a SQL table.

    Inserts the contents of a pandas DataFrame into a specified SQL table, appending the rows to the table if it already exists.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data to be stored.
    - table_name (str): The name of the target SQL table where the DataFrame's data will be inserted.

    Returns:
    - None

    The function uses the pandas to_sql method to append the DataFrame to the specified table without including the index.
    It assumes that a SQLAlchemy engine (`engine`) is already defined and available for connecting to the database.
    """
    df.to_sql(table_name, con=engine, if_exists="append", index=False)


@app.route("/upload-csv", methods=["POST"])
def upload_csv():
    """
    Uploads a CSV file and inserts its data into a specified table.

    This route handler processes a POST request containing a CSV file and a target table name.
    It validates the presence of the file and the table name in the request, checks the table name's validity,
    and then reads and inserts the CSV file's content into the specified table.

    Parameters:
    - file (FileStorage): The CSV file uploaded via HTTP request. Expected as part of the multipart/form-data under
    the "file" key.
    - table_name (str): The name of the target table where the CSV content will be stored. Passed as a form parameter.

    Returns:
    - JSONResponse: A JSON object containing either a success message with a
    200 status code if the file was successfully uploaded and inserted,
      or an error message with a 400 status code indicating what went wrong
      (missing parameters, invalid table name, or no file selected).

    The function first checks for the presence of 'file' and 'table_name'
    in the request. If either is missing, it returns an error.
    If the table name is not valid, it returns an error.
    If a file is present, it reads the file, inserts its data into the specified table,
    and returns a success message. If no file is found, it returns an error.
    """
    if "file" not in request.files or tables not in request.form:
        return jsonify({"error": "Missing file or table_name parameter"}), 400

    file = request.files["file"]
    table_name = request.form["table_name"]

    if not is_valid_table(table_name):
        return jsonify({"error": "Invalid table_name parameter"}), 400

    if file:
        file_stream = StringIO(file.read().decode("utf-8"))
        for df in read_csv(file_stream=file_stream):
            store_data(df=df, table_name=table_name)
        return jsonify({"message": f"File uploaded and inserted in {table_name} table successfully"}), 200
    else:
        return jsonify({"error": "No file selected"}), 400


if __name__ == "__main__":
    app.run(debug=True)
