import sqlite3 as sql1

con = sql1.connect("netviz_dev.db")


with con:
    con.execute("""
        create table CUSTOMER_DETAIL (
            CUS_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            CUS_FIRST_NAME VARCHAR NOT NULL,
            CUS_MIDDLE_NAME VARCHAR,
            CUS_LAST_NAME VARCHAR,
            CUS_TYPE VARCHAR NOT NULL,
            CUS_DOB VARCHAR NOT NULL,
            CUS_EST_DTE VARCHAR NOT NULL,
            OPEN_DT DATE NOT NULL,
            CLOSE_DT DATE NOT NULL
        );
    """)

with con:
    con.execute("""
        create table CUSTOMER_ADDRESS (
            CUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ADDRESS_LINE_1 INTEGER,
            ADDRESS_LINE_2 VARCHAR,
            ADDRESS_LINE_3 VARCHAR,
            SUBURB VARCHAR NOT NULL,
            CITY VARCHAR NOT NULL,
            ZIP_CODE INTEGER NOT NULL,
            ADDRESS_TYPE VARCHAR,
            OPEN_DT DATE NOT NULL,
            CLOSE_DT DATE NOT NULL
        );
    """)

with con:
    con.execute("""
        create table CUSTOMER_CONTACT (
            CUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CONTACT_METHOD VARCHAR,
            CONTACT_NUMBER VARCHAR,
            EMAIL_ID VARCHAR,
            OPEN_DT DATE NOT NULL,
            CLOSE_DT DATE NOT NULL
        );
    """)

with con:
    con.execute("""
        create table CUSTOMER_IDN_DOC (
            CUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            IDENTIFICATION_ID VARCHAR,
            IDENTIFICATION_TYPE VARCHAR,
            EXPIRY_DTE DATE,    
            EMAIL_ID VARCHAR,
            OPEN_DT DATE NOT NULL,
            CLOSE_DT DATE NOT NULL
        );
    """)

with con:
    con.execute("""
        create table LOOKUP_TABLE (
            Lookup_Name VARCHAR PRIMARY KEY,
            Lookup_Description VARCHAR NOT NULL
        );
    """)
    
with con:
    con.execute("""
        create table AUTHENTICATION (
            USER_NAME VARCHAR PRIMARY KEY,
            PASSWORD VARCHAR NOT NULL
        );
    """)
