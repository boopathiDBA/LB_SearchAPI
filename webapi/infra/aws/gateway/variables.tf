# Declare tags to be applied on every resource
# ---------------------------------------------------
locals {
  common_tags = {
    Environment         = var.environment
    Maintainer_Software = "Terraform"
    Revision            = "master"
    Project             = "https://github.com/little-birdie/webapi.git"
    team                = "Core Platform"
    service_name        = "webapi"
  }

  # Secrets set here will inject "name" as an environment variable and will fetch the value from the AWS Secret (This needs to be updated manually)
  webapi_a_secrets = [
    { "name" : "DATABASE_PASSWORD", "valueFrom" : "${aws_secretsmanager_secret.main_app_secrets.arn}:DATABASE_PASSWORD::" },
    { "name" : "JWT_SIGNING_KEY", "valueFrom" : "${aws_secretsmanager_secret.main_app_secrets.arn}:JWT_SIGNING_KEY::" },
    { "name" : "BRAZE_API_KEY", "valueFrom" : "${aws_secretsmanager_secret.main_app_secrets.arn}:BRAZE_API_KEY::" },
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

variable "vpc_base_cidr_block" {
  default = null
}

variable "allowed_cidr_blocks" {
  default     = ["202.142.49.122/32"]
  description = "These CIDR blocks are allowed to access internal private rosources"
}

variable "destination_cidr_block" {
  default     = ""
  description = "CIDR to connect transit gateway"
}

variable "database_cidr_block" {
  default     = ""
  description = "CIDR to connect transit gateway"
}

variable "aladdin_cidr_block" {
  default     = ""
  description = "CIDR to connect transit gateway"
}

variable "ror_cidr_block" {
  default     = ""
  description = "CIDR to connect transit gateway"
}

variable "domain_name" {
  default = null
}

variable "subject_alternative_names" {
  type = list(any)
}

variable "enable_waf" {
  type    = bool
  default = false
}

variable "deployment_profile" {
  type    = any
  default = "development"
}

variable "python_aws_powertools" {
  type    = any
  default = "arn:aws:lambda:ap-southeast-2:017000801446:layer:AWSLambdaPowertoolsPythonV2:18"
}

variable "python_sentry_layer" {
  type    = any
  default = "arn:aws:lambda:ap-southeast-2:943013980633:layer:SentryPythonServerlessSDK:47"
}

variable "layers" {
  type        = list(any)
  default     = []
  description = "Lambda layers"
}

variable "logs_retention_in_days" {
  default = 7
}

variable "webapi_a_external" {
  type    = any
  default = []
}

variable "authorizer_external_vars" {
  type    = map(any)
  default = {}
}

variable "webapi_a_service_cpu" {
  default = "256"
}

variable "webapi_a_service_memory" {
  default = "512"
}

variable "webapi_a_container_min" {
  default = "1"
}

variable "webapi_a_container_max" {
  default = "1"
}

variable "webapi_a_image" {
  default = null
}

variable "portMappings" {
  type = any
  default = [
    { "hostPort" : 8080, "protocol" : "tcp", "containerPort" : 8080 },
  ]
}

variable "cloudwatch_log_pattern" {
  type        = string
  description = "The awslogs-multiline-pattern option defines a multiline start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don’t match the pattern. Thus the matched line is the delimiter between log messages."
  default     = "([0-9]{4})-([0-1][0-9])-([0-3][0-9])T([0-2][0-9]):([0-5][0-9]):([0-5][0-9])\\\\.([0-9]{3})[+-][0-1][0-9]{3}"
}
