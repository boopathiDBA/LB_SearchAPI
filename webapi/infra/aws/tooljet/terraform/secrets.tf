# Create a variable with default values
# --------------------------------------

variable "self" {
  default = {
    SECRET_KEY_BASE    = "UPDATE_ME"
    PG_HOST            = "UPDATE_ME"
    PG_DB              = "UPDATE_ME"
    PG_USER            = "UPDATE_ME"
    PG_PASS            = "UPDATE_ME"
    PG_PORT            = "UPDATE_ME"
    LOCKBOX_MASTER_KEY = "UPDATE_ME"
  }

  type = map(string)
}

# Populate secret with variable
# --------------------------------------

resource "aws_secretsmanager_secret_version" "tooljet" {
  secret_id     = aws_secretsmanager_secret.tooljet.id
  secret_string = jsonencode(var.self)

  lifecycle {
    ignore_changes = [
      secret_string,
    ]
  }
}

# Create secrets
# --------------------------------------

resource "aws_secretsmanager_secret" "tooljet" {
  name = "/${var.environment}/webapi/tooljet/secrets"
  tags = local.common_tags
}
