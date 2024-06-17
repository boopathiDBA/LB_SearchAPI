[
  {
    "name": "${CONTAINER_NAME}",
    "image": "${REGISTRY_IMAGE}",
    "linuxParameters": {
       "initProcessEnabled": true
    },
    "networkMode": "awsvpc",
    "essential": true,
    "command": ["npm", "run", "start:prod"],
    "pseudoTerminal": true,
    "interactive": true,
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-create-group": "true",
          "awslogs-group": "${CLOUDWATCH_LOG_NAME}",
          "awslogs-stream-prefix": "svc-${CONTAINER_NAME}",
          "awslogs-region": "${AWS_REGION}"
        }
    },
    "environment": ${jsonencode(MAPAS)},
    "secrets": ${jsonencode(SECRETS)},
    "portMappings": ${jsonencode(portMappings)},
    "ulimits": [
      {
          "name": "nofile",
          "softLimit": 10240,
          "hardLimit": 65536
       }
     ]
  }
]
