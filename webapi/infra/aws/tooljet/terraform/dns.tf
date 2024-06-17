
resource "aws_route53_record" "www-search" {
  zone_id = data.aws_route53_zone.public.zone_id
  name    = var.subject_alternative_names[0]
  type    = "CNAME"
  ttl     = 5

  weighted_routing_policy {
    weight = 100
  }

  set_identifier = "live"
  records        = [aws_alb.middleware.dns_name]
}
