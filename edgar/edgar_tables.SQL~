-- DROP TABLE edgar_filings;
CREATE TABLE IF NOT EXISTS edgar_filings
(
    fil_id SERIAL PRIMARY KEY, 
    cpy_id INT REFERENCES company(cpy_id), 
    fil_title VARCHAR(254) NOT NULL, 
    fil_type VARCHAR(16) NOT NULL, 
    fil_name VARCHAR(255) NOT NULL, 
    fil_acc_num VARCHAR(32) NOT NULL, 
    fil_items VARCHAR(64) NOT NULL, 
    fil_url VARCHAR(256) NOT NULL, 
    fil_date TIMESTAMP NOT NULL
);

CREATE OR REPLACE FUNCTION fs_pgsql_store_edgar_filings(INT, VARCHAR, VARCHAR, 
                           VARCHAR, VARCHAR, VARCHAR, VARCHAR, TIMESTAMP)
RETURNS VOID AS $$
DECLARE 
    known_id INT; 
    
BEGIN
    SELECT INTO known_id fil_id FROM edgar_filings WHERE fil_acc_num = $5; 
    CASE known_id is NULL
    WHEN FALSE THEN
        UPDATE edgar_filings 
        SET cpy_id = $1, fil_title=$2, fil_type = $3, 
            fil_name = $4, fil_acc_num = $5, fil_items =$6, 
            fil_url=$7, fil_date=$8 
        
        WHERE fil_id = known_id; 
    ELSE
        INSERT INTO edgar_filings(cpy_id, fil_title, fil_type, 
                             fil_name, fil_acc_num, fil_items, 
                             fil_url, fil_date)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8); 
    END CASE; 
END; 
$$ LANGUAGE PLPGSQL;

--------------- 

---  ADMIN TABLES TO MANAGE THE QUOTE REQUESTS


--- 
CREATE TABLE IF NOT EXISTS quote_requests
(
    req_id SERIAL PRIMARY KEY, 
    cpy_id INT REFERENCES ticker(cpy_id), 
    exg_id INT REFERENCES ticker(exg_id), 
    requestor_node_id INT, -- node of the requestor for the quote. 
    assigned_node_id INT, -- node that is assigned to parsing of a pair
    src_id INT REFERENCES ticker(src_id),
    active BOOLEAN
);


-- functions to kill requests when a req_node dies
-- 





