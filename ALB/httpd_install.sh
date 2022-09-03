#!/bin/sh

yum install httpd -y 

systemctl enable httpd 

mkdir /var/www/html/redapp/

tee /var/www/html/redapp/index.html <<EOF
<!DOCTYPE html>
<html>
   <head>
      <title>HTML Backgorund Color</title>
   </head>
   <body style="background-color:red;">
      <h1>Machine 1</h1>
      <p>Red app</p>
   </body>
</html>
EOF

systemctl start httpd 
