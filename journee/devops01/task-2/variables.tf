variable "aws_region" {
  description = "AWS Region for infratructure resources"
  type        = string
  default     = "eu-central-1"
}

variable "desired_count" {
  description = "value for desired_count"
  type        = number
  default     = 1

}

variable "launch_type" {
  description = "value for launch_type"
  type        = string
  default     = "FARGATE"

}