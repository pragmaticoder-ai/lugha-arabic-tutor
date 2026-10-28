output "web_url" { value = google_cloud_run_v2_service.web.uri }
output "api_url" { value = google_cloud_run_v2_service.api.uri }
output "db_instance" { value = google_sql_database_instance.pg.connection_name }
