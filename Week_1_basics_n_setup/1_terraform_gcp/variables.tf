

variable "credentials" {
    description = "My Default Credentials"
    default = "./keys/my-creds.json"
  
}


variable "project" {
  description = "My Default Project"
  default     = "qwiklabs-gcp-04-ad82aa0bab62"
}

variable "region" {
  description = "My Default Region"
  default     = "us-east-1"
}


variable "location" {
  description = "My Default location"
  default     = "US"
}


variable "bq_dataset_name" {
  description = "My Bigquery Dataset Name"
  default     = "demo_dataset"
}


variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "tf-demo-qwiki-bucket"

}


variable "gcs_storage_class" {
  description = "bucket Storage Class"
  default     = "STANDARD"
}