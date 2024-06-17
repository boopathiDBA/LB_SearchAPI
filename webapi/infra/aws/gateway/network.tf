# Create CIDR for VPC
module "addrs" {
  source = "hashicorp/subnets/cidr"

  base_cidr_block = var.vpc_base_cidr_block
  networks = [
    {
      name     = "${var.environment}-api-private"
      new_bits = 1
    },
    {
      name     = "${var.environment}-api-public"
      new_bits = 1
    },
  ]
}

# Split CIDR for private subnets
module "private_subnets" {
  source = "hashicorp/subnets/cidr"

  base_cidr_block = lookup(module.addrs.network_cidr_blocks, "${var.environment}-api-private", null)
  networks = [
    {
      name     = "${var.environment}-api-private-00"
      new_bits = 2
    },
    {
      name     = "${var.environment}-api-private-01"
      new_bits = 2
    },
    {
      name     = "${var.environment}-api-private-02"
      new_bits = 2
    },
  ]
}

# Split CIDR for public subnets
module "public_subnets" {
  source = "hashicorp/subnets/cidr"

  base_cidr_block = lookup(module.addrs.network_cidr_blocks, "${var.environment}-api-public", null)
  networks = [
    {
      name     = "${var.environment}-api-public-00"
      new_bits = 2
    },
    {
      name     = "${var.environment}-api-public-01"
      new_bits = 2
    },
    {
      name     = "${var.environment}-api-public-02"
      new_bits = 2
    },
  ]
}

# Create VPC and subnets
module "api-network" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.10"

  name                                 = "${var.environment}-api"
  cidr                                 = var.vpc_base_cidr_block
  azs                                  = data.aws_availability_zones.available.names[*]
  private_subnets                      = sort(values(module.private_subnets.network_cidr_blocks))
  public_subnets                       = sort(values(module.public_subnets.network_cidr_blocks))
  enable_nat_gateway                   = true
  single_nat_gateway                   = var.deployment_profile == "development" ? true : false
  enable_dns_hostnames                 = true
  enable_dns_support                   = true
  enable_classiclink                   = true
  enable_classiclink_dns_support       = true
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true
  flow_log_max_aggregation_interval    = 60
  tags                                 = local.common_tags
}

# Attach networks to transit gateway
resource "aws_ec2_transit_gateway_vpc_attachment" "api" {
  subnet_ids         = module.api-network.private_subnets
  transit_gateway_id = data.aws_ec2_transit_gateway.main.id
  vpc_id             = module.api-network.vpc_id
  depends_on         = [module.api-network]
}

# Routes to others VPC using TGW
resource "aws_route" "api" {
  count                  = length(module.api-network.private_route_table_ids)
  route_table_id         = element(module.api-network.private_route_table_ids, count.index)
  destination_cidr_block = var.destination_cidr_block
  transit_gateway_id     = data.aws_ec2_transit_gateway.main.id
  depends_on             = [module.api-network]
}

resource "aws_route" "database" {
  count                  = length(module.api-network.private_route_table_ids)
  route_table_id         = element(module.api-network.private_route_table_ids, count.index)
  destination_cidr_block = var.database_cidr_block
  transit_gateway_id     = data.aws_ec2_transit_gateway.main.id
  depends_on             = [module.api-network]
}

resource "aws_route" "aladdin" {
  count                  = length(module.api-network.private_route_table_ids)
  route_table_id         = element(module.api-network.private_route_table_ids, count.index)
  destination_cidr_block = var.aladdin_cidr_block
  transit_gateway_id     = data.aws_ec2_transit_gateway.main.id
  depends_on             = [module.api-network]
}

resource "aws_route" "ror" {
  count                  = length(module.api-network.private_route_table_ids)
  route_table_id         = element(module.api-network.private_route_table_ids, count.index)
  destination_cidr_block = var.ror_cidr_block
  transit_gateway_id     = data.aws_ec2_transit_gateway.main.id
  depends_on             = [module.api-network]
}
