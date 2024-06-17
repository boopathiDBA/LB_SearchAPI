terraform {
  required_version = "= 1.5.2"


  backend "s3" {
    bucket       = "littlebirdie-git-private-runners"
    key          = "platform/webapiv2/terraform.tfstate"
    encrypt      = true
    region       = "ap-southeast-2"
    session_name = "webapiv2"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

provider "aws" {
  alias  = "edge"
  region = "us-east-1"
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

data "aws_route53_zone" "public" {
  name         = "${var.domain_name}."
  private_zone = false
}

data "aws_ec2_transit_gateway" "main" {
  filter {
    name   = "state"
    values = ["available"]
  }
}

data "aws_canonical_user_id" "current" {}

data "aws_ecr_repository" "webapi_a" {
  name = "webapi"
}

data "aws_ecr_image" "webapi_a" {
  repository_name = "webapi"
  image_tag       = "latest"
}
