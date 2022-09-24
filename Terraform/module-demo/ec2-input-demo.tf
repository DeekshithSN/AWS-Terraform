module "my-m-instance" {
source = "modules/input-var-ec2"
instance_type = "t2.micro"
instance_name = "module-demo"
environment = "Qa"  
}
