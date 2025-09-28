-- Create the database
-- Create Database financetracker;

-- Create the schema
-- Create Schema financetracker;
-- SET search_path TO financetracker;

-- Create the category table
Create Table financetracker.category (
    category_id serial,
    name VARCHAR(50) Not Null,
    description VARCHAR(255)
);

-- Add primary key to category
ALTER TABLE category
ADD CONSTRAINT PK_Category PRIMARY KEY (category_id);

-- Create the transactions table
Create Table financetracker.transactions (
    transaction_id serial,
    amount DECIMAL(10, 2) Not Null,
    transaction_date DATE Not Null,
    category_id INT,
    description VARCHAR(255)
);

-- Add primary key to transactions
ALTER TABLE financetracker.transactions
ADD CONSTRAINT PK_Transactions PRIMARY KEY (transaction_id);

-- Add foreign key from transactions to category
ALTER TABLE financetracker.transactions
ADD CONSTRAINT FK_Transactions_Category
FOREIGN KEY (category_id)
REFERENCES FinanceTracker.category(category_id);

-- Basic categories
INSERT INTO financetracker.category (name, description)
VALUES 
  ('Rent', 'Monthly housing payment'),
  ('Groceries', 'Food and essential household items'),
  ('Utilities', 'Electricity, water, gas, internet, etc.'),
  ('Transportation', 'Gas, rideshare, public transit'),
  ('Dining Out', 'Restaurants, fast food, cafes'),
  ('Entertainment', 'Movies, games, events, streaming'),
  ('Health', 'Doctor visits, prescriptions, health insurance, etc'),
  ('Education', 'Books, tuition, school supplies'),
  ('Shopping', 'Clothes, tech, online orders'),
  ('Savings', 'Transfers to savings'),
  ('Investments', 'Stocks, crypto, or retirement accounts'),
  ('Income', 'Paychecks, freelance, side hustle'),
  ('Travel', 'Flights, hotels')
  ;




Select * From financetracker.transactions;
Select * from financetracker.category;
