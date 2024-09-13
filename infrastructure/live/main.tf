terraform {
  backend "gcs" {}
}

provider "google" {
  project     = "virtuafit"
  region      = var.region
  credentials = file(var.credentials_file)
}

module "vpc" {
  source      = "./modules/vpc"
  environment = var.environment
  subnet_cidr = var.subnet_cidr
  region      = var.region
}

module "gke" {
  source       = "./modules/gke"
  environment  = var.environment
  region       = var.region
  node_count   = var.node_count
  machine_type = var.machine_type
  network      = module.vpc.vpc_name
  subnetwork   = module.vpc.subnet_name
  count        = var.environment == "dev" ? 1 : 0
  depends_on   = [module.vpc]
}
