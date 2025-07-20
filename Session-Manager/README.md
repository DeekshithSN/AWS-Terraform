Policies that we need to assoaciate for session manager 

custom policy 
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
```

aws managed policy 
```
AmazonSSMManagedInstanceCore
```

Pre requsites in windows to connect via aws ssm commands 

1. AWS cli
   ``` choco install awscli ```
2. Session Manager Plugin
  ``` choco install awscli-session-manager ```

Command to connect to ec2 via ssm 
```
aws ssm start-session --target <instance-id>
```
