terraform {
  required_version = "= 1.5.4"


  backend "s3" {
    bucket       = "littlebirdie-git-private-runners"
    key          = "platform/webapi-tooljet/terraform.tfstate"
    encrypt      = true
    region       = "ap-southeast-2"
    session_name = "webapi-tooljet"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4"
    }
  }
}

data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["${var.environment}-api"]
  }
}

data "aws_subnets" "current" {
  filter {
    name   = "tag:Name"
    values = ["*-api-private-*"]
  }
}

data "aws_subnets" "public" {
  filter {
    name   = "tag:Name"
    values = ["*-api-public-*"]
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

provider "aws" {
  alias  = "cloudfront"
  region = "us-east-1"
}

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

data "aws_route53_zone" "public" {
  name         = var.domain_name
  private_zone = false
}
