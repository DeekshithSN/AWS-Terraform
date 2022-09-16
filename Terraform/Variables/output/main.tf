provider "aws" {
   region     = "eu-central-1"
   access_key = "AKIATQ37NXB2G2LXXXXX"
   secret_key = "r1oaShokKPw+YY7qaHxj8mD2T8BpxRUVXXXXXXXX"
}

resource "aws_instance" "ec2_example" {
   
   ami           = "ami-0767046d1677be5a0"
   instance_type = "t2.micro"
   subnet_id = aws_subnet.staging-subnet.id
   
   tags = {
           Name = "test - Terraform EC2"
   }
}


output "my_console_output" {
  value = aws_instance.ec2_example.public_ip
} 
