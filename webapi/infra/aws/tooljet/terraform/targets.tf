
# Create a query-intention target group
# ---------------------------------------

resource "aws_lb_target_group" "query-intention-public" {
  name                          = "${var.environment}-webapi-tooljet"
  port                          = 3000
  protocol                      = "HTTP"
  vpc_id                        = data.aws_vpc.main.id
  target_type                   = "ip"
  load_balancing_algorithm_type = "least_outstanding_requests"
  health_check {
    protocol            = "HTTP"
    healthy_threshold   = 2
    interval            = 12
    path                = "/api/health"
    timeout             = 10
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
      "Service" = "webapi-tooljet"
    }
  )
}

# Create query-intention https
# ---------------------------------------

resource "aws_lb_listener_rule" "query-intention-public" {

  priority     = 1
  listener_arn = aws_alb_listener.web-https.arn

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.query-intention-public.arn
  }

  condition {
    host_header {
      values = [var.subject_alternative_names[0]]
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}
