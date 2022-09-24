module "my-vpc" {
source = "modules/simple-vpc-subnet"
cidir_block = "10.5.0.0/16"
name = "module-demo"
}
  
module "my-m-instance" {
source = "modules/ec2-module-interpollation"
instance_type = "t2.micro"
instance_name = "module-demo"
environment = "Qa"  
subnet-id = module.my-vpc.subnet_id
}
