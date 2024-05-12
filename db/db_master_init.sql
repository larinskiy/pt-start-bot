CREATE TABLE IF NOT EXISTS Phones (
    PhoneID SERIAL PRIMARY KEY,
    Phone VARCHAR(64) NOT NULL
);

INSERT INTO Phones (PhoneID, Phone) VALUES
(1, '88005555555'),
(2, '84990519301');

CREATE TABLE IF NOT EXISTS Emails (
    EmailID SERIAL PRIMARY KEY,
    Email VARCHAR(64) NOT NULL
);

INSERT INTO Emails (EmailID, Email) VALUES
(1, 'first@email.com'),
(2, 'second@email.com');

