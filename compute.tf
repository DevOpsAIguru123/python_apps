

// Create a cluster first (if you haven't already)
resource "databricks_cluster" "shared_cluster" {
  cluster_name            = "shared-cluster"
  spark_version          = "15.4.x-scala2.12"
  node_type_id           = "Standard_DS3_v2"
  driver_node_type_id    = "Standard_DS3_v2"
  policy_id              = "Shared Compute"
  autotermination_minutes = 120

  autoscale {
    min_workers = 1
    max_workers = 4
  }
}
