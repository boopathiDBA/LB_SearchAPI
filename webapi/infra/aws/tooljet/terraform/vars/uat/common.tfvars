environment               = "uat"
aws_region                = "ap-southeast-2"
domain_name               = "web.littlebirdie.dev"
subject_alternative_names = ["admin.web.littlebirdie.dev"]


# https://docs.tooljet.com/docs/setup/env-vars/
webapi_tooljet_external_vars = [
  { Name = "DEPLOYMENT_PLATFORM", Value = "aws:ecs" },
  { Name = "TOOLJET_HOST", Value = "https://admin.web.littlebirdie.dev" },
  { Name = "ORM_LOGGING", Value = "all" },
  { Name = "PG_HOST", Value = "project-deals-staging.cmonyogxq1or.ap-southeast-2.rds.amazonaws.com" },
]
