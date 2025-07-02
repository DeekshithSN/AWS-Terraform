variable "project_environment" {
  description = "project name and environment"
  type        = map(string)
  default = {
    project     = "project-alpha",
    environment = "dev"
  }
}

variable "availability_zones" {
    description = "values for availability zones"
    type        = list(string)
    default     = ["us-east-1a", "us-east-1b"]
}