
data "aws_ami" "app_ami" {
  most_recent = true
  owners = ["amazon"]
  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
  
  
   filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-gp2"]
  } 
 
}

resource "aws_instance" "app" {
  ami           = "${data.aws_ami.app_ami.id}"
  instance_type = var.instance_type
  subnet_id = var.subnet-id
  tags = {
    Name = var.instance_name
    Env = var.environment
   }
}
