resource "aws_cloudwatch_log_group" "webapi_a" {
  name              = "/aws/ecs/${var.environment}/webapi_a"
  retention_in_days = var.logs_retention_in_days
  tags              = local.common_tags
}
