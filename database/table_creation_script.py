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
            CUS_DOB VARCHAR,
            CUS_EST_DTE VARCHAR,
            GENDER VARCHAR,
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
        );
    """)

with con:
    con.execute("""
        create table CUSTOMER_ADDRESS (
            CUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ADDRESS_LINE_1 INTEGER,
            ADDRESS_LINE_2 VARCHAR,
            ADDRESS_LINE_3 VARCHAR,
            CITY VARCHAR NOT NULL,
            STATE VARCHAR NOT NULL,
            ZIP_CODE INTEGER NOT NULL,
            ADDRESS_TYPE VARCHAR,
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
        );
    """)

with con:
    con.execute("""
        create table CUSTOMER_CONTACT (
            CUS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            CONTACT_METHOD VARCHAR,
            CONTACT_NUMBER VARCHAR,
            EMAIL_ID VARCHAR,
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
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
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
        );
    """)

with con:
    con.execute("""
        create table ACCOUNT_DETAIL (
            ACCOUNT_ID VARCHAR PRIMARY KEY,
            ACCOUNT_STATUS VARCHAR,
            PROD_CDE VARCHAR,            
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
        );
    """)

with con:
    con.execute("""
        create table ACCOUNT_BALANCE (
            ACCOUNT_ID VARCHAR PRIMARY KEY,
            OUTSTANDING_BALANCE VARCHAR,
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
        );
    """)

with con:
    con.execute("""
        create table CUS_ACC_RLTSHP (
            ACCOUNT_ID VARCHAR,
            CUS_ID INTEGER,
            OPEN_DT DATETIME DEFAULT CURRENT_TIMESTAMP,
            CLOSE_DT DATETIME DEFAULT '9999-12-31 23:59:59.999'
        );
    """)

with con:
    con.execute("""
        create table TRANSACTION_DETAIL (
            TRANSACTION_REFERENCE VARCHAR,
            ACCOUNT_ID VARCHAR,
            TRANSACTION_TYPE VARCHAR,
            AMOUNT DECIMAL,
            TRANSACTION_DATE DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(TRANSACTION_REFERENCE, ACCOUNT_ID)
        );
    """)

with con:
    con.execute("""        
        create view CUSTOMER_ALL_V
        as
        select
            cd.cus_id,
            case
                when cd.cus_middle_name <> "" 
                    then cd.cus_first_name || ' ' || cd.cus_middle_name || ' ' || cd.cus_last_name
                else cd.cus_first_name || ' ' || cd.cus_last_name
            end as cus_name,
            cd.gender,
            cd.cus_type,
            case
                when cd.cus_type = 'IND' then cd.cus_dob
                when cd.cus_type = 'ORG' then cd.cus_est_dte
            end as cus_start_dte,
            case
                when ca.address_line_1 = "" and ca.address_line_2 = "" and ca.address_line_3 = "" 
                    then ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 = "" and ca.address_line_2 = "" and ca.address_line_3 <> ""
                    then ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 = "" and ca.address_line_2 <> "" and ca.address_line_3 = ""
                    then ca.address_line_2 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 = "" and ca.address_line_2 <> "" and ca.address_line_3 <> ""
                    then ca.address_line_2 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 <> "" and ca.address_line_2 = "" and ca.address_line_3 = ""
                    then ca.address_line_1 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 <> "" and ca.address_line_2 = "" and ca.address_line_3 <> ""
                    then ca.address_line_1 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 <> "" and ca.address_line_2 <> "" and ca.address_line_3 = ""
                    then ca.address_line_1 || ',' || ca.address_line_2 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
                when ca.address_line_1 <> "" and ca.address_line_2 <> "" and ca.address_line_3 <> ""
                    then ca.address_line_1 || ',' || ca.address_line_2 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code            
            end as cus_address,
            ca.address_type,
            case
                when cc.contact_method = 'PHN' and cc.contact_number <> "" then printf("%d",cc.contact_number)
                when cc.contact_method = 'PHN' and cc.contact_number = "" then cc.email_id
                when cc.contact_method = 'MBL' then printf("%d",cc.contact_number)
                when cc.contact_method = 'EML' then cc.email_id
            end as cus_contact,
            cid.identification_id,
            case
                when cid.expiry_dte >= DATE() then cid.identification_type
                else "New Document Required"
            end as cus_identification_doc,
            ad.account_id,
            lt.lookup_description as account_detail,
            ab.outstanding_balance,
            td.transaction_reference,
            td.transaction_type,
            td.amount,
            td.transaction_date
        from    
            customer_detail cd,
            customer_address ca,
            customer_contact cc,
            customer_idn_doc cid,
            account_detail ad,
            account_balance ab,
            cus_acc_rltshp car,
            lookup_table lt,
            (
            select     
                td1.account_id,
                td1.transaction_reference,
                td1.transaction_type,
                td1.amount,
                td1.transaction_date
            from
                transaction_detail td1
            where
                td1.transaction_reference in(
                select
                    td2.transaction_reference
                from
                    transaction_detail td2
                where
                    td1.account_id = td2.account_id
                order by 
                    td2.transaction_reference desc
                limit 5
                )
            ) td
        where
            cd.cus_id = ca.cus_id
        and cd.cus_id = cc.cus_id
        and cd.cus_id = cid.cus_id
        and car.cus_id = cd.cus_id
        and car.account_id = ad.account_id
        and ad.account_id = ab.account_id
        and td.account_id = ad.account_id
        and ad.prod_cde = lt.lookup_name        
        order by 
            cd.cus_id,
            td.account_id,
            td.transaction_reference desc;
        """)
    
with con:
    con.execute("""
    create view SEARCH_RESULT_V
    as
    select
        cd.cus_id,
        case
            when cd.cus_middle_name <> ""  then cd.cus_first_name || ' ' || cd.cus_middle_name || ' ' || cd.cus_last_name
            else cd.cus_first_name || ' ' || cd.cus_last_name
        end as cus_name,
        case
            when ca.address_line_1 = "" and ca.address_line_2 = "" and ca.address_line_3 = "" 
                then ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 = "" and ca.address_line_2 = "" and ca.address_line_3 <> ""
                then ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 = "" and ca.address_line_2 <> "" and ca.address_line_3 = ""
                then ca.address_line_2 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 = "" and ca.address_line_2 <> "" and ca.address_line_3 <> ""
                then ca.address_line_2 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 = "" and ca.address_line_3 = ""
                then ca.address_line_1 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 = "" and ca.address_line_3 <> ""
                then ca.address_line_1 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 <> "" and ca.address_line_3 = ""
                then ca.address_line_1 || ',' || ca.address_line_2 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 <> "" and ca.address_line_3 <> ""
                then ca.address_line_1 || ',' || ca.address_line_2 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code            
        end as cus_address,
        case
            when cc.contact_method = 'PHN' and cc.contact_number <> "" then printf("%d",cc.contact_number)
            when cc.contact_method = 'PHN' and cc.contact_number = "" then cc.email_id
            when cc.contact_method = 'MBL' then printf("%d",cc.contact_number)        
        end as cus_contact,
        ad.account_id    
    from
        customer_detail cd,
        customer_address ca,
        cus_acc_rltshp car,
        customer_contact cc,
        account_detail ad
    where
        cd.cus_id = ca.cus_id
    and cd.cus_id = car.cus_id
    and cd.cus_id = cc.cus_id
    and car.account_id = ad.account_id
    order by
        cd.cus_id;
    """)
    
with con:
    con.connect("""
    create view search_suggestion_v
    as
    select
        cus_id,
        cus_name as cus_details
    from
    (
    select
        cd.cus_id,
        case
            when cd.cus_middle_name <> ""  then cd.cus_first_name || ' ' || cd.cus_middle_name || ' ' || cd.cus_last_name
            else cd.cus_first_name || ' ' || cd.cus_last_name
        end as cus_name
    from
        customer_detail cd
    union all
    select
        ca.cus_id,
        case
            when ca.address_line_1 = "" and ca.address_line_2 = "" and ca.address_line_3 = "" 
                then ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 = "" and ca.address_line_2 = "" and ca.address_line_3 <> ""
                then ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 = "" and ca.address_line_2 <> "" and ca.address_line_3 = ""
                then ca.address_line_2 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 = "" and ca.address_line_2 <> "" and ca.address_line_3 <> ""
                then ca.address_line_2 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 = "" and ca.address_line_3 = ""
                then ca.address_line_1 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 = "" and ca.address_line_3 <> ""
                then ca.address_line_1 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 <> "" and ca.address_line_3 = ""
                then ca.address_line_1 || ',' || ca.address_line_2 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code
            when ca.address_line_1 <> "" and ca.address_line_2 <> "" and ca.address_line_3 <> ""
                then ca.address_line_1 || ',' || ca.address_line_2 || ',' || ca.address_line_3 || ',' || ca.city || ',' || ca.state || ',' || ca.zip_code            
        end as cus_address
    from
        customer_address ca
    union all
    select
        cc.cus_id,
        case
            when cc.contact_method = 'PHN' and cc.contact_number <> "" then printf("%d",cc.contact_number)
            when cc.contact_method = 'PHN' and cc.contact_number = "" then cc.email_id
            when cc.contact_method = 'MBL' then printf("%d",cc.contact_number)        
        end as cus_contact
    from
        customer_contact cc)
    order by
        cus_id;
    """)