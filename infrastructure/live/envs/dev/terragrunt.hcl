terraform {
  source = "../../"
}

inputs = {
  # Environment
  environment      = "dev"
  region           = "europe-west1"
  credentials_file = get_env("GOOGLE_APPLICATION_CREDENTIALS", "")

  # VPC
  subnet_cidr = "10.0.0.0/16"

  # GKE Cluster
  node_count   = 4
  machine_type = "n1-standard-4"

}

# Remote state 
remote_state {
  backend = "gcs"
  config  = {
    bucket  = "vf-tf-state-bucket"
    prefix  = "terraform/state/dev"
    project = "virtuafit"
  }
}