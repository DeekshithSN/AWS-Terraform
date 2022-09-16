provider "aws" {
   region     = "eu-central-1"
   access_key = "AKIATQ37NXB2AYK7R6PQ"
   secret_key = "S1Yg1Qm2JNSej8EHdhPTiu5l5ZD36URsedf32kNT"
}
resource "aws_instance" "ec2_example" {

   ami           = "ami-0767046d1677be5a0"
   instance_type =  var.instance_type

  tags = {
           Name = var.environment_name
   }

} 



variable "instance_type" {
}

variable "environment_name" {
}
