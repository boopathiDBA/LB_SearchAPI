# Cloudwatch group (Agreggate logs here)
# ---------------------------------------------------

resource "aws_cloudwatch_log_group" "query-intention" {
  name              = "/${var.environment}/webapi-tooljet"
  retention_in_days = var.retention_in_days
  tags              = local.common_tags
}

# Create ECS task definition
# ---------------------------------------

resource "aws_ecs_task_definition" "webapi_tooljet" {
  family                   = "${var.environment}-webapi-tooljet"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.service_cpu
  memory                   = var.service_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = templatefile("${path.module}/templates/ap-webapi-tooljet-template.tpl", {
    MAPAS                  = var.webapi_tooljet_external_vars
    SECRETS                = local.secrets
    portMappings           = var.portMappings
    AWS_REGION             = var.aws_region
    CONTAINER_NAME         = "webapi-tooljet"
    REGISTRY_IMAGE         = var.webapi_tooljet_image
    ENVIRONMENT            = var.environment
    CLOUDWATCH_LOG_PATTERN = var.cloudwatch_log_pattern
    CLOUDWATCH_LOG_NAME    = aws_cloudwatch_log_group.query-intention.name
  })

  tags = local.common_tags
}

# Create ECS service
# ---------------------------------------

resource "aws_ecs_service" "lb_webapi_tooljet" {
  name                   = "lb-webapi-tooljet"
  cluster                = module.ecs.ecs_cluster_id
  task_definition        = aws_ecs_task_definition.webapi_tooljet.arn
  desired_count          = var.desired_count
  launch_type            = "FARGATE"
  platform_version       = "1.4.0"
  wait_for_steady_state  = false
  force_new_deployment   = true
  enable_execute_command = true

  network_configuration {
    security_groups  = [aws_security_group.middleware.id]
    subnets          = data.aws_subnets.current.ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.query-intention-public.arn
    container_name   = "webapi-tooljet"
    container_port   = 3000
  }

  /*
  lifecycle {
    ignore_changes = [desired_count]
  }
  */

  tags = local.common_tags
}
