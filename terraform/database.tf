resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "lugha"
  format        = "DOCKER"
  depends_on    = [google_project_service.enabled]
}

resource "google_sql_database_instance" "pg" {
  name             = "lugha-postgres"
  database_version = "POSTGRES_15"
  region           = var.region
  settings {
    tier = var.db_tier
    ip_configuration { ipv4_enabled = true } # demo; private IP for real use
  }
  deletion_protection = false
  depends_on          = [google_project_service.enabled]
}

resource "google_sql_database" "lugha" {
  name     = "lugha"
  instance = google_sql_database_instance.pg.name
}
