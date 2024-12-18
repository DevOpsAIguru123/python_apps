// Create a cluster policy for shared compute
resource "databricks_cluster_policy" "shared_compute_policy" {
  name = "databricks-sbx"
  definition = jsonencode({
    "spark_version": {
      "type": "fixed",
      "value": "15.4.x-scala2.12"
    },
    "node_type_id": {
      "type": "fixed",
      "value": "Standard_DS3_v2"
    },
    "driver_node_type_id": {
      "type": "fixed",
      "value": "Standard_DS3_v2"
    },
    "autotermination_minutes": {
      "type": "fixed",
      "value": 120
    },
    "autoscale.min_workers": {
      "type": "fixed",
      "value": 1
    },
    "autoscale.max_workers": {
      "type": "fixed",
      "value": 4
    },
    "custom_tags.PolicyName": {
      "type": "fixed",
      "value": "Shared Compute"
    }
  })
}

// Create a cluster first (if you haven't already)
resource "databricks_cluster" "shared_cluster" {
  cluster_name            = "shared-cluster"
  spark_version          = "15.4.x-scala2.12"
  node_type_id           = "Standard_DS3_v2"
  driver_node_type_id    = "Standard_DS3_v2"
  policy_id              = databricks_cluster_policy.shared_compute_policy.id
  autotermination_minutes = 120

  autoscale {
    min_workers = 1
    max_workers = 4
  }
}
