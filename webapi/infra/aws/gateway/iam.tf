variable "service" {
  default = "webapi"
}

# Assume role policy
# ---------------------------------------------------

data "aws_iam_policy_document" "ecs_task_execution_role" {
  version = "2012-10-17"
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com", "lambda.amazonaws.com"]
    }
  }
}

# Container policy document
# ---------------------------------------------------

data "aws_iam_policy_document" "ecs_task_execution_policy_document" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    actions = [
      "cloudwatch:DescribeAlarms",
      "cloudwatch:PutMetricAlarm",
    ]
    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
    ]
    resources = [
      "*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
    ]
    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:DescribeLogStreams",
    ]
    resources = [
      "*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "xray:PutTraceSegments",
      "xray:PutTelemetryRecords",
      "xray:GetSamplingRules",
      "xray:GetSamplingTargets",
    ]
    resources = [
      "*",
    ]
  }
}

# Build policy using the above definition
# ---------------------------------------------------

resource "aws_iam_policy" "ecs_task_execution_iam_policy" {
  name   = "${var.environment}-${var.service}-ecs-iam-policy"
  path   = "/"
  policy = data.aws_iam_policy_document.ecs_task_execution_policy_document.json
}

# Create IAM role for container
# ---------------------------------------------------

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.environment}-${var.service}-ecs-execution-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

# Attach container policy document to the IAM role
# ---------------------------------------------------

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = aws_iam_policy.ecs_task_execution_iam_policy.arn
}
