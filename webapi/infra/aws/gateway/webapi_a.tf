# Create blue ECS task definition
# ---------------------------------------

resource "aws_ecs_task_definition" "webapi_a" {
  family                   = "${var.environment}-webapi-a"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.webapi_a_service_cpu
  memory                   = var.webapi_a_service_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  container_definitions = templatefile("${path.module}/templates/webapi_a.template", {
    MAPAS               = var.webapi_a_external
    SECRETS             = local.webapi_a_secrets
    portMappings        = var.portMappings
    IMAGE               = var.webapi_a_image == null ? "${data.aws_ecr_repository.webapi_a.repository_url}@${data.aws_ecr_image.webapi_a.image_digest}" : var.webapi_a_image
    AWS_REGION          = var.aws_region
    CONTAINER_NAME      = "${var.environment}-webapi-a"
    CLOUDWATCH_LOG_NAME = aws_cloudwatch_log_group.webapi_a.name
  })

  tags = local.common_tags
}

# Create blue ECS service
# ---------------------------------------
resource "aws_ecs_service" "webapi_a" {
  name                  = "${var.environment}-webapi-a"
  cluster               = module.ecs_cluster.id
  task_definition       = aws_ecs_task_definition.webapi_a.arn
  desired_count         = var.webapi_a_container_min
  launch_type           = "FARGATE"
  platform_version      = "1.4.0"
  force_new_deployment  = true
  wait_for_steady_state = true

  network_configuration {
    security_groups  = [aws_security_group.ecs.id]
    subnets          = module.api-network.private_subnets
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.webapi_a_public.arn
    container_name   = "${var.environment}-webapi-a"
    container_port   = 8080
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.webapi_a_internal.arn
    container_name   = "${var.environment}-webapi-a"
    container_port   = 8080
  }

  lifecycle {
    ignore_changes = [desired_count]
  }

  tags = local.common_tags
}
