variable "environment" {
  description = "The environment name (dev/staging/prod)"
  type        = string
}

variable "region" {
    description = "The region for GKE CLuster"
    type        = string
}

variable "node_count" {
    description = "Number of nodes in the GKE cluster's default node pool"
    type        = number
    default     = 3
}

variable "machine_type" {
    description = "the machine type for the node pool"
    type        = string
    default     = "e2-medium"
}

variable "network" {
    description = "the vpc net name to attach the gke"
    type        = string
}

variable "subnetwork" {
    description = "the subnet name of the vpc attached to the gke"
    type        = string
}