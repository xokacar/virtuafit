resource "google_container_cluster" "gke_cluster" {
  name     = "gke-${var.environment}"
  location = var.region
  remove_default_node_pool = false 

  node_pool {
    name       = "default-pool"
    node_count = var.node_count
    autoscaling {
      min_node_count = 2
      max_node_count = 8
    }
    node_config {
      machine_type = var.machine_type
      disk_size_gb = 50
    }

  }

  network    = var.network
  subnetwork = var.subnetwork

  deletion_protection = false
  
  lifecycle {
      create_before_destroy = true
    }
}
