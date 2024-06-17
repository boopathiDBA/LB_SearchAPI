# WAF
# ----------------------------------------------

module "waf_webapi" {

  source  = "umotif-public/waf-webaclv2/aws"
  version = "4.6.1"

  name_prefix = "${var.environment}-webapi-api"
  scope       = "REGIONAL"

  create_alb_association = false

  # create_logging_configuration = true
  # log_destination_configs      = [module.mod-common.blue_waf_logs_cf_kinesis_firehose_delivery_stream]

  allow_default_action = true

  visibility_config = {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.environment}-webapi-api-waf-cf-setup-main-metrics"
    sampled_requests_enabled   = true
  }

  rules = [
    {
      name     = "AWSManagedRulesCommonRuleSet"
      priority = "1"

      override_action = "none"

      visibility_config = {
        cloudwatch_metrics_enabled = true
        metric_name                = "${var.environment}AWSManagedRulesCommonRuleSet"
        sampled_requests_enabled   = true
      }

      managed_rule_group_statement = {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
        excluded_rule = [
          "SizeRestrictions_BODY",
          "GenericRFI_BODY",
          "CrossSiteScripting_BODY",
          "GenericRFI_QUERYARGUMENTS",
          "EC2MetaDataSSRF_COOKIE"
        ]
      }
    }
  ]

  tags = local.common_tags
}
