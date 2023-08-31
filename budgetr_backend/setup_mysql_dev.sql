-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS budgetr_dev_db;
CREATE USER IF NOT EXISTS 'budgetr_dev'@'localhost' IDENTIFIED BY 'budgetr_dev_pwd';
GRANT ALL PRIVILEGES ON `budgetr_dev_db`.* TO 'budgetr_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'budgetr_dev'@'localhost';
FLUSH PRIVILEGES;
