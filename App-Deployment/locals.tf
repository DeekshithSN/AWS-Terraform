locals {
  vpc_cidr_block = "10.0.0.0/16"
  public_subnet_cidr_blocks = [ "10.0.0.0/24", "10.0.10.0/24"]
  private_subnet_cidr_blocks = [ "10.0.20.0/24","10.0.30.0/24","10.0.40.0/24","10.0.50.0/24"]
}