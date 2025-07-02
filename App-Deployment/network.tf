resource "aws_vpc" "app-vpc" {
  cidr_block       = local.vpc_cidr_block
  instance_tenancy = "default"

  tags = merge(
    {
      Name = "web-app-vpc"
    },
    var.project_environment
  )
}

resource "aws_subnet" "public_subnet" {
  for_each = {
    subnet1 = {
      cidr_block        = local.public_subnet_cidr_blocks[0]
      availability_zone = var.availability_zones[0]
      name              = "Public-Web-Subnet-AZ-1"
    }
    subnet2 = {
      cidr_block        = local.public_subnet_cidr_blocks[1]
      availability_zone = var.availability_zones[1]
      name              = "Public-Web-Subnet-AZ-2"
    }
  }

  vpc_id            = aws_vpc.app-vpc.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.availability_zone

  tags = merge(
    {
      Name = each.value.name
    },
    var.project_environment
  )
}

resource "aws_subnet" "private_subnet" {
  for_each = {
    subnet1 = {
      cidr_block        = local.private_subnet_cidr_blocks[0]
      availability_zone = var.availability_zones[0]
      name              = "Private-App-Subnet-AZ-1"
    }
    subnet2 = {
      cidr_block        = local.private_subnet_cidr_blocks[1]
      availability_zone = var.availability_zones[1]
      name              = "Private-App-Subnet-AZ-2"
    }
    subnet3 = {
      cidr_block        = local.private_subnet_cidr_blocks[2]
      availability_zone = var.availability_zones[0]
      name              = "Private-DB-Subnet-AZ-1"
    }
    subnet4 = {
      cidr_block        = local.private_subnet_cidr_blocks[3]
      availability_zone = var.availability_zones[1]
      name              = "Private-DB-Subnet-AZ-2"
    }
  }

  vpc_id            = aws_vpc.app-vpc.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.availability_zone

  tags = merge(
    {
      Name = each.value.name
    },
    var.project_environment
  )
}

resource "aws_internet_gateway" "web-app-gw" {
  vpc_id = aws_vpc.app-vpc.id

  tags = merge(
  {
    Name = "web-app-igw"
  },
  var.project_environment
  )
}

resource "aws_eip" "example" {
  for_each = aws_subnet.public_subnet

  tags = {
    Name = "nat-eip-${each.key}"
  }
}

resource "aws_nat_gateway" "example" {
  for_each = aws_subnet.public_subnet

  allocation_id = aws_eip.example[each.key].id
  subnet_id     = each.value.id

  tags = {
    Name = "nat-gateway-${each.key}"
  }

}