Create Ec2 with docker installed and have role which have acces to RDS. Below Command is used connect to database
 ```
 docker run -it --rm mysql mysql -h<host-name> -u<master-username> -p
```

Below commands can be used to create databse, create and insert data to table

```
CREATE DATABASE jira_data;
USE jira_data;

CREATE TABLE jira_tickets (
  ticket_key VARCHAR(20) PRIMARY KEY,
  summary TEXT,
  status VARCHAR(50),
  created_at DATETIME
);

INSERT INTO jira_tickets (ticket_key, summary, status, created_at) VALUES ('PROJ-101', 'Login button not working', 'To Do', '2025-07-01 09:15:00');

select * from jira_tickets;
```

Commands to create, lambda layer

```
pip install pymysql -t python
zip -r9 lambda-layer.zip .\python
```

other useful commands
```
aws secretsmanager get-secret-value --secret-id <secret-arn> --version-id <version-d> --query SecretString --output text
```

