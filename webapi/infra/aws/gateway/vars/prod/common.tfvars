environment               = "prod"
aws_region                = "ap-southeast-2"
vpc_base_cidr_block       = "172.20.208.0/20"
domain_name               = "web.littlebirdie.com.au"
subject_alternative_names = ["a.web.littlebirdie.com.au", "z.web.littlebirdie.com.au"]
destination_cidr_block    = "172.16.250.0/24"
database_cidr_block       = "10.0.0.0/16"
aladdin_cidr_block        = "172.18.240.0/20"
ror_cidr_block            = "10.0.0.0/16"
webapi_a_container_min    = 2
webapi_a_container_max    = 20

webapi_a_external = [
  { Name = "DEPLOY_ENV", Value = "prod" },
  { Name = "REGION", Value = "ap-southeast-2" },
  { Name = "SENTRY_DSN", Value = "https://270c7bc3b4ad0aaf9b5eeafd1328a081@o1071790.ingest.us.sentry.io/4507150803402752" },
  { Name = "OPENSEARCH_HOST", Value = "https://search.stream.littlebirdie.com.au" },
  { Name = "OPENSEARCH_DEALS_INDEX", Value = "a_deals" },
  { Name = "DATABASE_URL", Value = "lb-web-ap-1-cluster.cluster-ro-cgpf1upkkv4x.ap-southeast-2.rds.amazonaws.com" },
  { Name = "DATABASE_USER", Value = "web_user" },
  { Name = "DATABASE_DBNAME", Value = "web" },
  { Name = "IMAGE_BASE_URL", Value = "https://assets.littlebirdie.com.au/uploads" },
  { Name = "DEFAULT_PROFILE_IMAGE", Value = "https://blue.littlebirdie.com.au/assets/avatar-ddba12e05258094eb8ed250ba33155806926f1c5f311fd7e9edad4f34a589708.svg" },
  # see `src/common/logging.py` for supported values
  { Name = "LOG_LEVEL", Value = "WARNING" }
]
