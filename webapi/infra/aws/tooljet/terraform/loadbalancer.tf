# HTTPS ALB listener
# --------------------------------------

resource "aws_alb_listener" "web-https" {
  depends_on        = [aws_alb.middleware]
  load_balancer_arn = aws_alb.middleware.arn
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
}

resource "aws_alb_listener" "web-http" {
  depends_on        = [aws_alb.middleware]
  load_balancer_arn = aws_alb.middleware.arn
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
}

# HTTP ALB
# --------------------------------------

resource "aws_alb" "middleware" {
  name            = "${var.environment}-webapi-tooljet"
  internal        = false
  subnets         = data.aws_subnets.public.ids
  security_groups = [aws_security_group.middleware.id]

  tags = local.common_tags
}
