provider "aws" {
  region = "ap-south-1"
}

resource "aws_key_pair" "deployer" {
  key_name   = "aws_key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+WJOVuSyI4CQpeHyC4pEyB3FxQqlgoJFxoOezNK7mgARxUaTLBpo+oEb89vkhCUVBU9HryRyqITWCl9jxqmsaI/scuCXsZEsyIPNgQ5vxIaXgoKwlrOdyan0RNuGFDQswpOgmDNeV8tefmtaF3Z9cLvvRaOEAN3uoUXBlS9UndQJGMnn1v5+S/5QBnLUSdE3cXOyVZu68KmKwmI5xhOHntbOPL+OaTAb6feaYp/vbbJex+DupN7ls0wmNt72tOdVlD6yNFuE9m98vH/k16w4PCYvgRA354N/CjUUmVx8WgxKaGDyONaMWktF07avHSZyimrYDRq+9+IH87SdhOyCZ root@ip-172-31-42-60.ap-south-1.compute.internal"
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

resource "aws_instance" "ec2_example" {
   
   ami           = "ami-06489866022e12a14"
   instance_type = "t2.micro"
   key_name      = "aws_key"
   vpc_security_group_ids = [aws_security_group.main.id]

   tags = {
    Name = "file-provisioner-ec2"
    Env = "Dev"
   }
}

resource "null_resource" "cluster" {

  provisioner "file" {
      source      = "/home/test.txt"
      destination = "/home/test-file.txt"
  }
    
    connection {
      type        = "ssh"
      host        =  aws_instance.ec2_example.public_ip
      user        = "ec2-user"
      private_key = file("/home/aws_key")
      timeout     = "4m"
   }
}
