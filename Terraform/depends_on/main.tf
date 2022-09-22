provider "aws" {
   region     = "ap-south-1"
   
}

resource "aws_key_pair" "deployer" {
  key_name   = "aws_key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDi+oyzCZgToE3nw6Xf1hKt23cYHPDDPzdgwcWPlkPKk7IYguNt6F+CgkRRwtA04v1bISRp4+g+FoGz0lEfzUHZ2VJlQNYDZZv9HygxcPYBQ3F1IpXEdvZxxkUbaAdjZJYVMbv/8t3TwHqyFHQmpb32HxYoEqcmpHW7cD2cR8mO9OA73IDFaQl9FGcia5KjzcHs4zf/1KIqlo/uVYOetC/TmcRWit8q1YRu8RMmL8965VZHwtq4z38ifKlqgOyRgzirsU8BZ+C6tCiNhagN8fO+ra5VNzFAqNxcGPchQNl+nZiIxs4x+Kiy7rgY/k5pk2ma7M80eyUUCIF3i/XY/14P root@ip-172-31-41-240.ap-south-1.compute.internal"
}

resource "aws_s3_bucket" "example" {
  bucket = "test-dee-depends-test"
}

resource "null_resource" "name" {

  provisioner "local-exec" {
     command = "echo ${aws_s3_bucket.example.bucket_domain_name} > /home/s3-details.txt"
  }
  
  depends_on = [
    aws_instance.ec2_example
  ]
  
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
    ami = "ami-06489866022e12a14"  
    instance_type = "t2.micro" 
    key_name= "aws_key"
    vpc_security_group_ids = [aws_security_group.main.id]
    tags = {
        Name = "Terraform EC2"
    }

}        

resource "null_resource" "machine_details" {
 provisioner "file" {
    source      = "/home/s3-details.txt"
    destination = "/home/ec2-user/s3-details.txt"
  }
  connection {
      type        = "ssh"
      host        = aws_instance.ec2_example.public_ip
      user        = "ec2-user"
      private_key = file("/home/aws_key")
      timeout     = "4m"
   }
}



