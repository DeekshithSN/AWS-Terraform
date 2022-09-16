provider "aws" {
   region     = "eu-central-1"
   access_key = "AKIATQ37NXB2OBQHAALW"
   secret_key = "ilKygurap8zSErv7jySTDi2796WGqMkEtN6txNHf"
}
resource "aws_instance" "ec2_example" {

   ami           = "ami-0767046d1677be5a0"
   instance_type =  "t2.micro"

   tags = var.project_environment

}


variable "project_environment" {
  description = "project name and environment"
  type        = map(string)
  default     = {
    project     = "project-alpha",
    environment = "dev"
  }
}
BASH
