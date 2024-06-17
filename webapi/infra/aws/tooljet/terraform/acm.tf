# Create ACM certificate to be used on ALBs
# ------------------------------------------

module "acm" {
  source  = "terraform-aws-modules/acm/aws"
  version = "~> v2.0"

  domain_name = var.domain_name
  zone_id     = data.aws_route53_zone.public.zone_id

  subject_alternative_names = var.subject_alternative_names
  validate_certificate      = true

  tags = merge(
    local.common_tags,
    {
      "Name" = "webapi-tooljet"
    }
  )

}
