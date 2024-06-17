# Public Security group
# -----------------------------------------------------
resource "aws_security_group" "middleware" {
  name        = "${var.environment}-webapi-tooljet-sg"
  description = "Allow access to Tooljet"
  vpc_id      = data.aws_vpc.main.id

  tags = local.common_tags
}

resource "aws_security_group_rule" "middleware-ingress" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = -1
  cidr_blocks       = [data.aws_vpc.main.cidr_block]
  security_group_id = aws_security_group.middleware.id
  description       = "Allow access ingress access"
}

resource "aws_security_group_rule" "middleware-ingress-443" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.middleware.id
  description       = "Allow access ingress access"
}

resource "aws_security_group_rule" "middleware-ingress-80" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.middleware.id
  description       = "Allow access ingress access"
}

resource "aws_security_group_rule" "middleware-egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = -1
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.middleware.id
  description       = "Allow access egress access"
}

# Private Security group
# -----------------------------------------------------
resource "aws_security_group" "middleware-private" {
  name        = "${var.environment}-tooljet-private-sg"
  description = "Allow access to Tooljet"
  vpc_id      = data.aws_vpc.main.id

  tags = local.common_tags
}

resource "aws_security_group_rule" "middleware-public-egress" {
  type              = "ingress"
  from_port         = 0
  to_port           = 0
  protocol          = -1
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.middleware-private.id
  description       = "Allow access egress access"
}

resource "aws_security_group_rule" "middleware-private-egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = -1
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.middleware-private.id
  description       = "Allow access egress access"
}
