provider "aws" {
   region     = "ap-south-1"
   
}

resource "aws_instance" "ec2_example" {

    ami = "ami-06489866022e12a14"  
    instance_type = "t2.micro" 
    key_name= "sndee"
    vpc_security_group_ids = [aws_security_group.main.id]

  provisioner "file" {
    source      = "/home/test.txt"
    destination = "/home/test-file.txt"
  }
  connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ubuntu"
      private_key = file("/home/sndee")
      timeout     = "4m"
   }
}

resource "aws_security_group" "main" {
  egress = [
    {
      cidr_blocks      = [ "0.0.0.0/0", ]
      description      = ""
      from_port        = 0
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "-1"
      security_groups  = []
      self             = false
      to_port          = 0
    }
  ]
 ingress                = [
   {
     cidr_blocks      = [ "0.0.0.0/0", ]
     description      = ""
     from_port        = 22
     ipv6_cidr_blocks = []
     prefix_list_ids  = []
     protocol         = "tcp"
     security_groups  = []
     self             = false
     to_port          = 22
  }
  ]
}

resource "aws_key_pair" "deployer" {
  key_name   = "sndee"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCmxaA//hHK4TJkAcYm5ia3sFmH8vPAzcqZgNPIiBexKYDFZ95+Gt1B4ItBUfWO7hFdC1DJ436e+VxDRQcRFxGoxAD7MoE2Bhiuup3s5RcCESBXf7QCNPuOHdHeLULPQ5ueOnEuv95GcknZytaYzMsTW2qBHIzj7zXl+jZwmLGMfZFW40bSTV6hmEzo4Ej+zPGPDIcTRcZrw/aPoLvQ6zRvKDjJj76OET0LasjfPH3HIKNXFPfnBJ/CGFETIjjfbRC6+oOceGiUv5yFUhBGTUrldC1jbH2qgT43voXxTGhvcgn5vAUnz4AJeOk0FWTuPoUg/F9rRGWjKSZdfkKPSsHl root@ip-172-31-40-57.ap-south-1.compute.internal"
}
