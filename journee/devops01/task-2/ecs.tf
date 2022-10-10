resource "aws_ecs_cluster" "journee-interview-cluster" {
  name = "i-idris-interview"
}

resource "aws_ecs_service" "journee-interview-ecs" {
  name            = "i-idris-app"
  cluster         = aws_ecs_cluster.journee-interview-cluster.id
  task_definition = aws_ecs_task_definition.i-idris-interview-task-definition.arn
  launch_type     = var.launch_type
  network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}", "${aws_default_subnet.default_subnet_c.id}"]
    assign_public_ip = true
  }
  desired_count = var.desired_count
}

resource "aws_ecs_task_definition" "i-idris-interview-task-definition" {
  family                   = "i-idris-interview-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  memory                   = "1024"
  cpu                      = "512"
  execution_role_arn       = aws_iam_role.ecsTaskExecutionRole.arn
  container_definitions    = <<EOF
[
  {
    "name": "minterview",
    "image": "123456789012.dkr.ecr.eu-central-1.amazonaws.com/journee-interview:1.0",
    "memory": 1024,
    "cpu": 512,
    "essential": true,
    "entryPoint": ["/"],
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ]
    "mountPoints": [
                {
                    "sourceVolume": "service-storage",
                    "containerPath": "/journee",
                    "readOnly": true
                }
            ]

        ]
  },
  
EOF
  volume {
    name = "service-storage"

    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.service-storage.id
      root_directory     = "/export"
      transit_encryption = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.service-storage.id
        iam             = "ENABLED"
      }
    }

  }

}

resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "ecs-tasks.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
        }
    ]
    }
  EOF
}