resource "aws_security_group" "lambdas" {
  name        = "${var.environment}-webapi-lambdas"
  description = "Allow TLS inbound traffic"
  vpc_id      = module.api-network.vpc_id

  ingress {
    description = "TLS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_base_cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common_tags,
    {
      "Name" = "${var.environment}-webapi-lambdas"
    }
  )
}

resource "aws_security_group" "main" {
  name        = "${var.environment}-webapi-main"
  description = "Allow TLS inbound traffic"
  vpc_id      = module.api-network.vpc_id

  ingress {
    description = "TLS from Anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP from Anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common_tags,
    {
      "Name" = "${var.environment}-webapi-main"
    }
  )
}

resource "aws_security_group" "ecs" {
  name        = "${var.environment}-webapi-ecs"
  description = "Allow inbound traffic to ECS task"
  vpc_id      = module.api-network.vpc_id

  ingress {
    description     = "App access from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.main.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    local.common_tags,
    {
      "Name" = "${var.environment}-webapi-ecs"
    }
  )
}
