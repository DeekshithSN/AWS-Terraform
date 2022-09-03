yum install httpd -y 

systemctl enable httpd 

mkdir /var/www/html/redapp/

tee /var/www/html/redapp/index.html <<EOF
<!DOCTYPE html>
<html>
   <head>
      <title>HTML Backgorund Color</title>
   </head>
   <body style="background-color:grey;">
      <h1>Products</h1>
      <p>We have developed more than 10 products till now.</p>
   </body>
</html>
EOF

systemctl start httpd 
