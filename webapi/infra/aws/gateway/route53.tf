
resource "aws_route53_record" "www-live" {
  zone_id = data.aws_route53_zone.public.zone_id
  name    = "z.${var.domain_name}"
  type    = "CNAME"
  ttl     = 5

  weighted_routing_policy {
    weight = 100
  }

  set_identifier = "live"
  records        = [aws_alb.main.dns_name]
}

resource "aws_route53_record" "www-internal" {
  zone_id = data.aws_route53_zone.public.zone_id
  name    = "g.${var.domain_name}"
  type    = "CNAME"
  ttl     = 5

  weighted_routing_policy {
    weight = 100
  }

  set_identifier = "live"
  records        = [aws_alb.main-internal.dns_name]
}

resource "aws_route53_record" "www-cache" {
  zone_id = data.aws_route53_zone.public.zone_id
  name    = "a.${var.domain_name}"
  type    = "CNAME"
  ttl     = 5

  weighted_routing_policy {
    weight = 100
  }

  set_identifier = "cache"
  records        = [aws_cloudfront_distribution.webapi.domain_name]
}
