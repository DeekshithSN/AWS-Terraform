provider "aws" {
   region     = "eu-central-1"
   access_key = "AKIATQ37NXBxxxxxxxxx"
   secret_key = "JzZKiCia2vjbq4zGGGewdbOhnacmxxxxxxxxxxxx"
   
}

resource "aws_instance" "ec2_example" {

    ami = "ami-0767046d1677be5a0"  
    instance_type = "t2.micro" 
    tags = {
        Name = "Terraform EC2"
    }

  provisioner "local-exec" {
    command = "touch hello.txt"
  }
}
