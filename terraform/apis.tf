locals {
  apis = [
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "sqladmin.googleapis.com",
    "aiplatform.googleapis.com",        # Vertex AI / Gemini
    "texttospeech.googleapis.com",
    "speech.googleapis.com",
    "secretmanager.googleapis.com",
  ]
}
resource "google_project_service" "enabled" {
  for_each           = toset(local.apis)
  service            = each.value
  disable_on_destroy = false
}
