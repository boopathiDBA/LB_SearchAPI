resource "random_id" "secret" {
  byte_length = 4
}

variable "self" {
  default = {
    SECRET_KEY_BASE           = "UPDATE_ME"
    SENTRY_DSN                = "UPDATE_ME"
    SIMPLE_AUTH_PWD           = "UPDATE_ME"
    DATABASE_PASSWORD         = "UPDATE_ME"
    JWT_SIGNING_KEY           = "UPDATE_ME"
    REPLICA_DATABASE_PASSWORD = "UPDATE_ME"
    MONGODB_PASSWORD          = "UPDATE_ME"
    DEALS_DATABASE_PASS       = "UPDATE_ME"
    AMAZON_S3_ACCESS_SECRET   = "UPDATE_ME"
    AMAZON_SES_PWD            = "UPDATE_ME"
    FACEBOOK_APP_SECRET       = "UPDATE_ME"
    GOOGLE_APP_SECRET         = "UPDATE_ME"
    HTTP_PUBLIC_API_TOKEN     = "UPDATE_ME"
    ELASTIC_PASSWORD          = "UPDATE_ME"
    BRAZE_API_KEY             = "UPDATE_ME"
  }

  type = map(string)
}

resource "aws_secretsmanager_secret_version" "main" {
  secret_id     = aws_secretsmanager_secret.main_app_secrets.id
  secret_string = jsonencode(var.self)

  lifecycle {
    ignore_changes = [
      secret_string,
    ]
  }
}

resource "aws_secretsmanager_secret" "main_app_secrets" {
  name = "/${var.environment}/webapi/app-${random_id.secret.hex}"
  tags = merge(
    local.common_tags,
    {
      "secret" = "webapi_app"
    }
  )
}
