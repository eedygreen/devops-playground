## Task-2 IaC

The following files 
- `variable.tf`
- `resources.tf`
- `main.tf`
- `ecs.tf`
- `availability_zones.tf`

### The varibale file
This is a place holder for referencing 

### The main file
The provider configuration, in this case it is the aws provider and it also reference the credentials.

### The availability zone
Default network configuration vpc subnets for resources to connects 

### The ecr file
Definition to create the ecr repository to host the Docker image built in Task-1. Also to create a policy that permits uploads of the image

### The ECS file
Definition to create
- ecs cluster
- ecs service
- task definition to run the image built in Task-1
    -  mount an efs volume with an access point /export
- IAM role to permits ecs to execute tasks

| Note: The docker image should be pushed manually to ecr and change the address.