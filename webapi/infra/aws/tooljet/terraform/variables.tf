# Declare tags to be applied on every resource
# ---------------------------------------------------
locals {
  common_tags = {
    Environment         = var.environment
    Maintainer_Software = "Terraform"
    Revision            = "master"
    Project             = "https://github.com/little-birdie/webapi.git"
    team                = "Product Discovery"
    service_name        = "Webapi"
  }

  secrets = [
    { "name" : "LOCKBOX_MASTER_KEY", "valueFrom" : "${aws_secretsmanager_secret.tooljet.arn}:LOCKBOX_MASTER_KEY::" },
    { "name" : "PG_DB", "valueFrom" : "${aws_secretsmanager_secret.tooljet.arn}:PG_DB::" },
    { "name" : "PG_PASS", "valueFrom" : "${aws_secretsmanager_secret.tooljet.arn}:PG_PASS::" },
    { "name" : "PG_PORT", "valueFrom" : "${aws_secretsmanager_secret.tooljet.arn}:PG_PORT::" },
    { "name" : "PG_USER", "valueFrom" : "${aws_secretsmanager_secret.tooljet.arn}:PG_USER::" },
    { "name" : "SECRET_KEY_BASE", "valueFrom" : "${aws_secretsmanager_secret.tooljet.arn}:SECRET_KEY_BASE::" },
  ]

}

# Declare here the common variables
#----------------------------------
variable "environment" {
  default = "uat"
}

variable "aws_region" {
  default = "ap-southeast-2"
}

variable "domain_name" {
  default = null
}

variable "subject_alternative_names" {
  type = list(any)
}

variable "deployment_profile" {
  type    = any
  default = "development"
}

variable "desired_count" {
  type    = any
  default = "2"
}

variable "retention_in_days" {
  type    = any
  default = "7"
}

variable "service_cpu" {
  type    = string
  default = "4096"
}

variable "service_memory" {
  type    = string
  default = "8192"
}

variable "portMappings" {
  type = any
  default = [
    { "hostPort" : 3000, "protocol" : "tcp", "containerPort" : 3000 },
  ]
}

variable "webapi_tooljet_image" {
  type    = string
  default = "tooljet/tooljet-ce"
}

variable "webapi_tooljet_external_vars" {
  type    = any
  default = []
}

variable "cloudwatch_log_pattern" {
  type        = string
  description = "The awslogs-multiline-pattern option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages."
  default     = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])T([0-2][0-9]):([0-5][0-9]):([0-5][0-9])\\\\.([0-9]{3})[+-][0-1][0-9]{3}"
}
