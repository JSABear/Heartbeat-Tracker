def db_handler(bpm,sns,pns):
    import mysql.connector
    import random
    #Connect to database
    mydb = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        database="health",
    )
    # Create a cursor object
    mycursor = mydb.cursor()

    # Define the values to be inserted
    bpm_value = bpm
    sns_value = sns
    pns_value = pns

    # Define the SQL query to insert values into the table
    sql = "INSERT INTO patient_data (BPM, SNS, PNS) VALUES (%s, %s, %s)"

    # Define the values to be inserted as a tuple
    val = (bpm_value, sns_value, pns_value)

    # Execute the query
    mycursor.execute(sql, val)

    # Commit the changes
    mydb.commit()

    # Print the number of inserted rows
    print(mycursor.rowcount, "record inserted.")