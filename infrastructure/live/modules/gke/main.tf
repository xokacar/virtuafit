resource "google_container_cluster" "gke_cluster" {
  name     = "gke-${var.environment}"
  location = var.region

  node_pool {
    name       = "default-pool"
    node_count = var.node_count
    node_config {
      machine_type = var.machine_type
      disk_size_gb = 50
    }

  }

  network    = var.network
  subnetwork = var.subnetwork

  deletion_protection = false
}
