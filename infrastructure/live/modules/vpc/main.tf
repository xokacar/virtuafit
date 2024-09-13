resource "google_compute_network" "vpc" {
  name                    = "vpc-${var.environment}"
  auto_create_subnetworks  = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "subnet-${var.environment}"
  network       = google_compute_network.vpc.name
  ip_cidr_range = var.subnet_cidr
  region        = var.region
}
