# Create webapi public listener rule https documents
# ---------------------------------------
resource "aws_lb_listener_rule" "webapi_a_https_public_docs" {

  listener_arn = aws_alb_listener.web-https.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webapi_a_public.arn
  }

  condition {
    host_header {
      values = var.subject_alternative_names
    }
  }

  condition {
    path_pattern {
      values = ["/docs*", "/openapi.json"]
    }
  }

  condition {
    source_ip {
      values = var.allowed_cidr_blocks
    }
  }
}

# Create webapi public listener rule https
# ---------------------------------------
resource "aws_lb_listener_rule" "webapi_a_https_public" {

  listener_arn = aws_alb_listener.web-https.arn
  priority     = 2

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webapi_a_public.arn
  }

  condition {
    host_header {
      values = var.subject_alternative_names
    }
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}

# Create webapi private listener rule https
# ---------------------------------------
resource "aws_lb_listener_rule" "webapi_a_https_private" {

  listener_arn = aws_alb_listener.main-internal-443.arn
  priority     = 1

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webapi_a_internal.arn
  }

  condition {
    host_header {
      values = var.subject_alternative_names
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}

# Create a webapi A target group
# ---------------------------------------
resource "aws_lb_target_group" "webapi_a_public" {
  name                          = "${var.environment}-webapi-a-public"
  port                          = 8080
  protocol                      = "HTTP"
  vpc_id                        = module.api-network.vpc_id
  target_type                   = "ip"
  load_balancing_algorithm_type = "least_outstanding_requests"
  health_check {
    protocol            = "HTTP"
    healthy_threshold   = 2
    interval            = 30
    path                = "/api/healthcheck"
    timeout             = 10
    unhealthy_threshold = 3
    matcher             = "200"
  }

  stickiness {
    type        = "app_cookie"
    enabled     = false
    cookie_name = "_devise-omniauth_session"
  }

  tags = merge(
    local.common_tags,
    {
      "Service" = "webapi_a_public"
    }
  )
}

# Create a webapi A internal target group
# ---------------------------------------
resource "aws_lb_target_group" "webapi_a_internal" {
  name                          = "${var.environment}-webapi-a-private"
  port                          = 8080
  protocol                      = "HTTP"
  vpc_id                        = module.api-network.vpc_id
  target_type                   = "ip"
  load_balancing_algorithm_type = "least_outstanding_requests"
  health_check {
    protocol            = "HTTP"
    healthy_threshold   = 2
    interval            = 120
    path                = "/api/healthcheck"
    timeout             = 90
    unhealthy_threshold = 10
    matcher             = "200"
  }

  stickiness {
    type        = "app_cookie"
    enabled     = false
    cookie_name = "_devise-omniauth_session"
  }

  tags = merge(
    local.common_tags,
    {
      "Service" = "webapi_a_private"
    }
  )
}

# Create a webapi ALB internal target group
# ---------------------------------------
resource "aws_lb_target_group" "webapi_alb_internal" {
  name                          = "${var.environment}-webapi-a-alb"
  port                          = 80
  protocol                      = "TCP"
  vpc_id                        = module.api-network.vpc_id
  target_type                   = "alb"
  health_check {
    protocol            = "HTTP"
    healthy_threshold   = 2
    interval            = 120
    path                = "/api/healthcheck"
    timeout             = 90
    unhealthy_threshold = 10
    matcher             = "200"
  }

  tags = merge(
    local.common_tags,
    {
      "Service" = "webapi_a_alb"
    }
  )
}


# Attach ALB target group to internal LB
# --------------------------------------
resource "aws_lb_target_group_attachment" "webapi_alb_internal" {
  target_group_arn = aws_lb_target_group.webapi_alb_internal.arn
  target_id        = aws_alb.main-internal.arn
  port             = 80
}

# HTTPS ALB listener
# --------------------------------------

resource "aws_alb_listener" "web-https" {
  depends_on        = [aws_alb.main]
  load_balancer_arn = aws_alb.main.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = module.acm.this_acm_certificate_arn

  default_action {
    type = "fixed-response"

    fixed_response {
      content_type = "text/plain"
      message_body = <<-EOF
 ____________________________________
( Chuck Norris counted to infinity - )
( twice.                             )
 ------------------------------------
        o   ^__^
         o  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
         ________________________
        ( You shouldn't be here )
         ------------------------
EOF
      status_code  = "200"
    }
  }

  tags = local.common_tags
}

resource "aws_alb_listener" "web-http" {
  depends_on        = [aws_alb.main]
  load_balancer_arn = aws_alb.main.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }

  tags = local.common_tags
}

resource "aws_alb_listener" "main-internal-443" {
  depends_on        = [aws_alb.main-internal]
  load_balancer_arn = aws_alb.main-internal.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = module.acm.this_acm_certificate_arn

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
      host        = "littlebirdie.com.au"
    }
  }

  tags = local.common_tags
}

resource "aws_alb_listener" "main-internal-80" {
  depends_on        = [aws_alb.main-internal]
  load_balancer_arn = aws_alb.main-internal.arn
  port              = "80"
  protocol          = "HTTP"

  # Don't redirect to https, send to internal ALB
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webapi_a_internal.arn
  }

  tags = local.common_tags
}

resource "aws_lb_listener" "main-network" {
  depends_on        = [aws_lb.main-network]
  load_balancer_arn = aws_lb.main-network.arn
  port              = "80"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webapi_alb_internal.arn
  }
}

# HTTP ALB
# --------------------------------------

resource "aws_alb" "main" {
  name            = "${var.environment}-webapi-alb-public"
  internal        = false
  subnets         = module.api-network.public_subnets
  security_groups = [aws_security_group.main.id]

  tags = local.common_tags
}

resource "aws_alb" "main-internal" {
  name            = "${var.environment}-webapi-alb-private"
  internal        = true
  subnets         = module.api-network.private_subnets
  security_groups = [aws_security_group.main.id]

  tags = local.common_tags
}

# HTTP NLB (Static IPs)
# --------------------------------------
resource "aws_lb" "main-network" {
  name               = "${var.environment}-webapi-nlb-canary"
  load_balancer_type = "network"
  internal           = true
  security_groups    = [aws_security_group.main.id]

  subnet_mapping {
    subnet_id            = module.api-network.private_subnets[0]
    private_ipv4_address = cidrhost(module.api-network.private_subnets_cidr_blocks[0], 20)
  }

  subnet_mapping {
    subnet_id            = module.api-network.private_subnets[1]
    private_ipv4_address = cidrhost(module.api-network.private_subnets_cidr_blocks[1], 21)
  }

  subnet_mapping {
    subnet_id            = module.api-network.private_subnets[2]
    private_ipv4_address = cidrhost(module.api-network.private_subnets_cidr_blocks[2], 22)
  }
}
