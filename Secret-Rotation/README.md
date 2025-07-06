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
Policies that need to attch it to lambda function 

```
AmazonRDSFullAccess
AWSLambdaVPCAccessExecutionRole
CloudWatchFullAccess
SecretsManagerReadWrite
```

Important steps to launch lambda in in VPC and connect to RDS

```
Create NAT (Attach it public subnet) --> create private subnet --> create route table ( add NAT gateway into route table ) --> associate rt to private subnet --> use this in Lambda  
```

Commands to create, lambda layer

```
pip install pymysql -t python
zip -r9 lambda-layer.zip .\python
```

```
mkdir -p lambda-layer/python
cd lambda-layer/python
pip3 install --platform manylinux2014_x86_64 --target . --python-version 3.9 --only-binary=:all: python-gitlab
zip -r layer.zip python
```

other useful commands
```
aws secretsmanager get-secret-value --secret-id <secret-arn> --version-id <version-d> --query SecretString --output text
```

Testing gitlab Pat token
```
curl --header "PRIVATE-TOKEN: <YOUR_PAT>" \
  "https://gitlab.com/api/v4/projects?owned=true&per_page=100" \
  | jq -r '.[].name'
```
