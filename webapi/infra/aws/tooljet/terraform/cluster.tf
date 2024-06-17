# Configures an AWS Fargate cluster
# ---------------------------------------------------

module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  version = "~> 3.0"

  name               = "${var.environment}-webapi-tooljet"
  container_insights = true
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  default_capacity_provider_strategy = [
    {
      capacity_provider = "FARGATE"
    }
  ]

  tags = local.common_tags
}
