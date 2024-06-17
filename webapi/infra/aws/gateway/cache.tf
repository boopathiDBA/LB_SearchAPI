# cache cookies, headers, and query
resource "aws_cloudfront_cache_policy" "CachingCookiesHeadersQuery" {
  name        = "${var.environment}CachingCookiesHeadersQuery"
  comment     = "Browser Extension Cache Policy"
  default_ttl = 3000
  max_ttl     = 3600
  min_ttl     = 1
  parameters_in_cache_key_and_forwarded_to_origin {
    cookies_config {
      cookie_behavior = "all"
    }
    headers_config {
      header_behavior = "whitelist"
      headers {
        items = ["webapi"]
      }
    }
    query_strings_config {
      query_string_behavior = "all"
    }
  }
}

# no cache policy
data "aws_cloudfront_cache_policy" "CachingDisabled" {
  name = "Managed-CachingDisabled"
}

# cache cloudfront distribution
resource "aws_cloudfront_distribution" "webapi" {
  provider = aws.edge

  # application load balancer for fastapi
  origin {
    domain_name = "z.${var.domain_name}"
    origin_id   = "webapi"
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "${var.environment} WeabAPI cached endpoint"
  default_root_object = "index.html"

  /*
  logging_config {
    include_cookies = false
    bucket          = "mylogs.s3.amazonaws.com"
    prefix          = "myprefix"
  }
  */

  aliases = ["a.${var.domain_name}"]

  # disabled cache on new endpoints unless declared individually
  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["HEAD", "GET", "OPTIONS"]
    target_origin_id = "webapi"

    viewer_protocol_policy = "allow-all"

    cache_policy_id = data.aws_cloudfront_cache_policy.CachingDisabled.id
  }

  ordered_cache_behavior {
    path_pattern     = "/api/top_lists/stores"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "webapi"

    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    cache_policy_id = aws_cloudfront_cache_policy.CachingCookiesHeadersQuery.id
  }

  # Cache behavior with precedence 0
  ordered_cache_behavior {
    path_pattern     = "/api/departments"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "webapi"

    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    cache_policy_id = aws_cloudfront_cache_policy.CachingCookiesHeadersQuery.id
  }

  # Cache behavior with precedence 1
  ordered_cache_behavior {
    path_pattern     = "/api/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "webapi"

    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    cache_policy_id = data.aws_cloudfront_cache_policy.CachingDisabled.id
  }

  price_class = "PriceClass_All"

  restrictions {
    geo_restriction {
      restriction_type = "blacklist"
      locations        = ["RU"]
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.edge.arn
    ssl_support_method  = "sni-only"
  }

  tags = merge(
    local.common_tags,
    {
      "Group" = "destination-refactor"
    }
  )
}
