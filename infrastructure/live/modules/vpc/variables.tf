variable "environment" {
  description = "The environment name (dev/staging/prod)"
  type        = string
}

variable "subnet_cidr" {
  description = "CIDR range for the subnet"
  type        = string
}

variable "region" {
  description = "The region to deploy the resources"
  type        = string
  default     = "europe-west1"
}
