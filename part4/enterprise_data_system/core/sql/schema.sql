-- Base tables from Part 3
CREATE TABLE Account (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name2 VARCHAR(255),
    company_code INTEGER NOT NULL,
    tax_id VARCHAR(20) NOT NULL,
    emp_count INTEGER NOT NULL,
    status CHAR(1) NOT NULL,
    status_date DATE NOT NULL
);

CREATE TABLE AccountLocation (
    account_id INTEGER PRIMARY KEY REFERENCES Account(id),
    address1 VARCHAR(255) NOT NULL,
    address2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip VARCHAR(20) NOT NULL
);

CREATE TABLE BillingAccount (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    name2 VARCHAR(255),
    group_num VARCHAR(20) NOT NULL,
    tax_id VARCHAR(20) NOT NULL,
    geo_code INTEGER NOT NULL,
    online_billing CHAR(1) NOT NULL,
    status CHAR(1) NOT NULL,
    status_date DATE NOT NULL
);

CREATE TABLE BillingLocation (
    billing_id INTEGER PRIMARY KEY REFERENCES BillingAccount(id),
    address1 VARCHAR(255) NOT NULL,
    address2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip VARCHAR(20) NOT NULL
);

CREATE TABLE Customer (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_init CHAR(1),
    suffix VARCHAR(10),
    salutation VARCHAR(10),
    gender CHAR(1) NOT NULL,
    language VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE
);

CREATE TABLE CustomerIdentity (
    customer_id INTEGER PRIMARY KEY REFERENCES Customer(id),
    dob DATE NOT NULL,
    ssn VARCHAR(11) NOT NULL,
    ssn_type CHAR(1) NOT NULL,
    legacy_id VARCHAR(20),
    withholding CHAR(1) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE LineOfBusiness (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE SeriesName (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE PlanName (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Contract (
    id SERIAL PRIMARY KEY,
    contract_num VARCHAR(20) NOT NULL UNIQUE,
    business_id INTEGER NOT NULL REFERENCES LineOfBusiness(id),
    series_id INTEGER NOT NULL REFERENCES SeriesName(id),
    plan_id INTEGER NOT NULL REFERENCES PlanName(id),
    status CHAR(1) NOT NULL,
    status_date DATE NOT NULL,
    coverage VARCHAR(50) NOT NULL,
    account_id INTEGER NOT NULL REFERENCES Account(id),
    in_force CHAR(1) NOT NULL,
    language VARCHAR(50) NOT NULL,
    duration INTEGER NOT NULL
);

CREATE TABLE ContractPayment (
    contract_id INTEGER PRIMARY KEY REFERENCES Contract(id),
    bill_method VARCHAR(50) NOT NULL,
    premium DECIMAL(10,2) NOT NULL,
    auto_loan CHAR(1) NOT NULL,
    payment_limit DECIMAL(10,2) NOT NULL
);

CREATE TABLE ContractBankAccount (
    contract_id INTEGER PRIMARY KEY REFERENCES Contract(id),
    transit_num VARCHAR(20) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    account_num VARCHAR(20) NOT NULL
);

CREATE TABLE ContractCreditCard (
    contract_id INTEGER PRIMARY KEY REFERENCES Contract(id),
    card_num VARCHAR(20) NOT NULL,
    exp_date DATE NOT NULL,
    card_type VARCHAR(50) NOT NULL
);

CREATE TABLE Invoice (
    id SERIAL PRIMARY KEY,
    invoice_num VARCHAR(20) NOT NULL UNIQUE,
    billing_id INTEGER NOT NULL REFERENCES BillingAccount(id),
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    paid_date DATE,
    due_date DATE NOT NULL,
    run_date DATE NOT NULL
);

-- Analytics tables
CREATE TABLE CustomerFeedback (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    feedback_text TEXT NOT NULL,
    sentiment_score FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    key_topics TEXT[] NOT NULL
);

CREATE TABLE CallRecord (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    call_text TEXT NOT NULL,
    duration INTEGER NOT NULL,
    call_time TIMESTAMP NOT NULL,
    sentiment_score FLOAT NOT NULL,
    key_topics TEXT[] NOT NULL
);

CREATE TABLE ChronicDiseaseRisk (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    risk_score FLOAT NOT NULL,
    risk_factors TEXT[] NOT NULL,
    prediction_date TIMESTAMP NOT NULL,
    confidence_score FLOAT NOT NULL
);

CREATE TABLE ChurnPrediction (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    churn_probability FLOAT NOT NULL,
    contributing_factors TEXT[] NOT NULL,
    prediction_date TIMESTAMP NOT NULL
);

CREATE TABLE ProductRecommendation (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES Customer(id),
    plan_id INTEGER NOT NULL REFERENCES PlanName(id),
    recommendation_score FLOAT NOT NULL,
    recommendation_date TIMESTAMP NOT NULL
);

-- New tables for Part 4
CREATE TABLE MLModelVersion (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(20) NOT NULL,
    version VARCHAR(50) NOT NULL,
    accuracy FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    model_path VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT false,
    metadata JSONB,
    UNIQUE (model_type, version)
);

CREATE TABLE MLModelTrainingJob (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    metrics JSONB
);

CREATE TABLE DataUpdateLog (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(20) NOT NULL,
    record_count INTEGER NOT NULL,
    processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    requires_retraining BOOLEAN NOT NULL DEFAULT false
);

-- Create indexes
CREATE INDEX idx_account_status ON Account(status);
CREATE INDEX idx_account_company ON Account(company_code);
CREATE INDEX idx_billing_status ON BillingAccount(status);
CREATE INDEX idx_billing_group ON BillingAccount(group_num);
CREATE INDEX idx_customer_name ON Customer(last_name, first_name);
CREATE INDEX idx_customer_dates ON Customer(start_date, end_date);
CREATE INDEX idx_contract_num ON Contract(contract_num);
CREATE INDEX idx_contract_status ON Contract(status);
CREATE INDEX idx_invoice_dates ON Invoice(due_date, paid_date);
CREATE INDEX idx_feedback_sentiment ON CustomerFeedback(sentiment_score);
CREATE INDEX idx_call_sentiment ON CallRecord(sentiment_score);
CREATE INDEX idx_risk_score ON ChronicDiseaseRisk(risk_score);
CREATE INDEX idx_churn_prob ON ChurnPrediction(churn_probability);
CREATE INDEX idx_recommendation ON ProductRecommendation(recommendation_score);
CREATE INDEX idx_model_version ON MLModelVersion(model_type, version);
CREATE INDEX idx_training_job ON MLModelTrainingJob(model_type, status);
CREATE INDEX idx_data_update ON DataUpdateLog(table_name, processed_at);

-- Create materialized views for analytics
CREATE MATERIALIZED VIEW customer_risk_summary AS
SELECT 
    c.id,
    c.last_name,
    c.first_name,
    cdr.risk_score as disease_risk,
    cp.churn_probability,
    COUNT(pr.id) as recommendation_count
FROM Customer c
LEFT JOIN ChronicDiseaseRisk cdr ON c.id = cdr.customer_id
LEFT JOIN ChurnPrediction cp ON c.id = cp.customer_id
LEFT JOIN ProductRecommendation pr ON c.id = pr.customer_id
GROUP BY c.id, c.last_name, c.first_name, cdr.risk_score, cp.churn_probability;

CREATE MATERIALIZED VIEW customer_interaction_summary AS
SELECT 
    c.id,
    c.last_name,
    c.first_name,
    COUNT(cf.id) as feedback_count,
    AVG(cf.sentiment_score) as avg_feedback_sentiment,
    COUNT(cr.id) as call_count,
    AVG(cr.sentiment_score) as avg_call_sentiment
FROM Customer c
LEFT JOIN CustomerFeedback cf ON c.id = cf.customer_id
LEFT JOIN CallRecord cr ON c.id = cr.customer_id
GROUP BY c.id, c.last_name, c.first_name;

-- Function to refresh materialized views
CREATE OR REPLACE FUNCTION refresh_analytics_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY customer_risk_summary;
    REFRESH MATERIALIZED VIEW CONCURRENTLY customer_interaction_summary;
END;
$$ LANGUAGE plpgsql;

-- Function to log data updates
CREATE OR REPLACE FUNCTION log_data_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO DataUpdateLog (table_name, operation, record_count, requires_retraining)
    VALUES (TG_TABLE_NAME, TG_OP, 1, true);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for logging data updates
CREATE TRIGGER log_customer_feedback_update
AFTER INSERT OR UPDATE ON CustomerFeedback
FOR EACH ROW EXECUTE FUNCTION log_data_update();

CREATE TRIGGER log_call_record_update
AFTER INSERT OR UPDATE ON CallRecord
FOR EACH ROW EXECUTE FUNCTION log_data_update();
