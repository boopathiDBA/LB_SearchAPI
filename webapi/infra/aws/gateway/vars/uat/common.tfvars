environment               = "uat"
aws_region                = "ap-southeast-2"
vpc_base_cidr_block       = "172.20.212.0/24"
domain_name               = "web.littlebirdie.dev"
subject_alternative_names = ["a.web.littlebirdie.dev", "z.web.littlebirdie.dev"]
destination_cidr_block    = "172.16.252.0/24"
database_cidr_block       = "172.16.212.0/24"
aladdin_cidr_block        = "172.19.240.0/20"
ror_cidr_block            = "172.30.0.0/16"
webapi_a_container_min    = 1
webapi_a_container_max    = 1

webapi_a_external = [
  { Name = "DEPLOY_ENV", Value = "uat" },
  { Name = "REGION", Value = "ap-southeast-2" },
  { Name = "SENTRY_DSN", Value = "https://270c7bc3b4ad0aaf9b5eeafd1328a081@o1071790.ingest.us.sentry.io/4507150803402752" },
  { Name = "OPENSEARCH_HOST", Value = "https://search.stream.littlebirdie.dev" },
  { Name = "OPENSEARCH_DEALS_INDEX", Value = "a_deals" },
  { Name = "DATABASE_URL", Value = "dbw.web.littlebirdie.dev" },
  { Name = "DATABASE_USER", Value = "postgres" },
  { Name = "DATABASE_DBNAME", Value = "project-deals-staging" },
  { Name = "IMAGE_BASE_URL", Value = "https://project-deals-staging.s3.ap-southeast-2.amazonaws.com/uploads" },
  { Name = "DEFAULT_PROFILE_IMAGE", Value = "https://uat.littlebirdie.dev/assets/avatar-ddba12e05258094eb8ed250ba33155806926f1c5f311fd7e9edad4f34a589708.svg" },
  # see `src/common/logging.py` for supported values
  { Name = "LOG_LEVEL", Value = "WARNING" }
]
