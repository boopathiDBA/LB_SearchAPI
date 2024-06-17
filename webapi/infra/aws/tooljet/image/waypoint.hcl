project = "tooljet-backend"

app "tooljet-backend" {

  labels = {
    "service" = "tooljet-backend"
  }

  build {
    use "docker" {
      dockerfile = "tooljet.dockerfile"
      disable_entrypoint = true
    }

    registry {
      use "aws-ecr" {
        region     = "ap-southeast-2"
        repository = "tooljet-backend"
        tag        = gitrefpretty()
      }
    }
  }

  deploy {
    use "null" {}
  }
}
