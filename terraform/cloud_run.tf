# Two independent Cloud Run services — frontend and backend scale separately.

resource "google_cloud_run_v2_service" "api" {
  name     = "lugha-api"
  location = var.region
  template {
    scaling { max_instance_count = 2 }
    containers {
      image = var.api_image
      ports { container_port = 8080 }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project_id
      }
      env {
        name  = "VERTEX_AI_LOCATION"
        value = var.region
      }
    }
  }
  depends_on = [google_project_service.enabled]
}

resource "google_cloud_run_v2_service" "web" {
  name     = "lugha-web"
  location = var.region
  template {
    scaling { max_instance_count = 2 }
    containers {
      image = var.web_image
      ports { container_port = 8080 }
      env {
        name  = "NEXT_PUBLIC_API_BASE"
        value = google_cloud_run_v2_service.api.uri
      }
    }
  }
  depends_on = [google_cloud_run_v2_service.api]
}

# Public access (demo). Lock down with auth for real use.
resource "google_cloud_run_v2_service_iam_member" "web_public" {
  location = var.region
  name     = google_cloud_run_v2_service.web.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
resource "google_cloud_run_v2_service_iam_member" "api_public" {
  location = var.region
  name     = google_cloud_run_v2_service.api.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
