provider "aws" {
   region     = "eu-central-1"
}

resource "aws_instance" "ec2_example" {

   ami           = "ami-0767046d1677be5a0"
   instance_type =  var.instance_type

   tags = {
           Name = "Terraform EC2"
   }
} 


variable "instance_type" {
}
