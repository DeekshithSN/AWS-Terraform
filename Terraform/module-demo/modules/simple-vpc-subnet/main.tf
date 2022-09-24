resource "aws_vpc" "staging-vpc" {
  cidr_block = var.cidir_block

  tags = {
    Name = var.name
  }
}

resource "aws_subnet" "staging-subnet" {
  vpc_id = aws_vpc.staging-vpc.id
  cidr_block = var.cidir_block

  tags = {
    Name = var.name
  }
}
