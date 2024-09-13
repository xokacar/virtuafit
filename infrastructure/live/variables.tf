variable "environment" {
  description = "Environment (dev/staging/prod)"
  default     = "dev"
}

variable "subnet_cidr" {
  description = "CIDR range for the subnet"
  default     = "10.0.0.0/16"
}

variable "region" {
  description = "Region to deploy resources"
  default     = "europe-west1"
}

variable "node_count" {
  description = "Number of nodes in the GKE cluster's default node pool"
  type        = number
  default     = 3
}

variable "machine_type" {
  description = "Machine type for the node pool in GKE cluster"
  type        = string
  default     = "n1-standard-1"
}

variable "credentials_file" {
  description = "The path to the gc service account json file"
  type        = string
}
