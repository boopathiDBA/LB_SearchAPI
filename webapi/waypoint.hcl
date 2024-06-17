project = "webapi"

app "webapi" {

  labels = {
    "service" = "webapi"
  }

  build {
    use "docker" {
      dockerfile = ".docker/webapi/Dockerfile"
      disable_entrypoint = true
      buildkit = true
      platform = "linux/amd64"
    }

    registry {
      use "aws-ecr" {
        region     = "ap-southeast-2"
        repository = "webapi"
        tag        = gitrefpretty()
      }
    }
  }

  deploy {
    use "null" {}
  }
}

app "webapi-latest" {

  labels = {
    "service" = "webapi"
  }

  build {
    use "docker" {
      dockerfile = ".docker/webapi/Dockerfile"
      disable_entrypoint = true
      buildkit = true
      platform = "linux/amd64"
    }

    registry {
      use "aws-ecr" {
        region     = "ap-southeast-2"
        repository = "webapi"
        tag        = "latest"
      }
    }
  }

  deploy {
    use "null" {}
  }
}
