resource "aws_iam_role" "ecs-autoscale-role" {
  name = "webapi-ecs-scale-application"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "application-autoscaling.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-autoscale" {
  role       = aws_iam_role.ecs-autoscale-role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole"
}

#------------------------------------------------------------------------------
# Note. See README.md for more information on why the following scaling
# policies are configured
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# AWS Auto Scaling - CloudWatch Alarm
#------------------------------------------------------------------------------
resource "aws_cloudwatch_metric_alarm" "scaling_alarm" {
  alarm_name          = "${var.environment}-cpu-utilization"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1 # Number of periods before alarm is triggered. This is set to the mimimum to trigger alarm as soon as possible
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = 60        # Number of seconds. This is set to the minimum value to trigger alarm as soon as possible
  statistic           = "Average" # Average is used to smooth out the data
  threshold           = 0         # We always want to alarm and let the scaling policy decide if it is appropriate to scale up and down
  dimensions = {
    ClusterName = "${var.environment}-webapi-apis"
    ServiceName = "${var.environment}-webapi-a"
  }
  alarm_actions = [
    aws_appautoscaling_policy.step_scaling_policy.arn,
  ]
}


#------------------------------------------------------------------------------
# AWS Auto Scaling - Step Scaling Policy
#------------------------------------------------------------------------------
resource "aws_appautoscaling_policy" "step_scaling_policy" {
  name               = "${var.environment}-step-scaling-policy"
  depends_on         = [aws_appautoscaling_target.scale_target]
  service_namespace  = "ecs"
  resource_id        = "service/${var.environment}-webapi-apis/${var.environment}-webapi-a"
  scalable_dimension = "ecs:service:DesiredCount"
  step_scaling_policy_configuration {
    # Number of seconds to wait before scaling again. 
    # This is set to 2 minutes to allow time for containers to spin up and start taking in traffic. 
    # If this is set too low, the scaling policy triggers a scale down due to the reduction of 
    # CPU utilisation when new container are spinning up without taking any traffic.
    adjustment_type         = "PercentChangeInCapacity"
    cooldown                = 120
    metric_aggregation_type = "Average"

    #  If Average CPU utilisation is at 0% - 30% this will scale the number of nodes down 30%.
    step_adjustment {
      metric_interval_upper_bound = 30
      scaling_adjustment          = -30
    }

    #  If Average CPU utilisation is at 30% - 40% this will scale the number of nodes down 10%.
    step_adjustment {
      metric_interval_lower_bound = 30
      metric_interval_upper_bound = 40
      scaling_adjustment          = -10
    }

    # Between 40% - 60% CPU utilisation, we want to keep the number of nodes the same. 
    # Hence a gap in step adjustment

    #  If Average CPU utilisation is at 40% - 60% this will scale the number of nodes down 10%.
    step_adjustment {
      metric_interval_lower_bound = 40
      metric_interval_upper_bound = 60
      scaling_adjustment          = -10
    }

    #  If Average CPU utilisation is at 60% - 70% this will scale the number of nodes up 10%.
    step_adjustment {
      metric_interval_lower_bound = 60
      metric_interval_upper_bound = 70
      scaling_adjustment          = 10
    }

    #  If Average CPU utilisation is more than 70% this will scale the number of nodes up 30%.
    step_adjustment {
      metric_interval_lower_bound = 70
      scaling_adjustment          = 30
    }

  }
}

#------------------------------------------------------------------------------
# AWS Auto Scaling - Scaling Target
#------------------------------------------------------------------------------
resource "aws_appautoscaling_target" "scale_target" {
  service_namespace  = "ecs"
  resource_id        = "service/${var.environment}-webapi-apis/${var.environment}-webapi-a"
  scalable_dimension = "ecs:service:DesiredCount"
  min_capacity       = var.webapi_a_container_min
  max_capacity       = var.webapi_a_container_max
  role_arn           = aws_iam_role.ecs-autoscale-role.arn
}

