variable "project_id" { type = string }
variable "region" {
  type    = string
  default = "us-central1"
}
variable "db_tier" {
  type    = string
  default = "db-f1-micro" # smallest; review billing
}
variable "web_image" { type = string } # artifact registry image for lugha-web
variable "api_image" { type = string } # artifact registry image for lugha-api
