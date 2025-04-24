
# See https://www.postgresql.org/docs/9.6/static/runtime-config-logging.html
# and https://www.postgresql.org/docs/9.6/static/runtime-config-query.html#RUNTIME-CONFIG-QUERY-ENABLE
# for detail parameter descriptions
locals {
  pg_family_version = replace(var.engine_version, "/\\.[0-9]/", "")
}



resource "aws_key_pair" "automation_dev" {
  key_name   = "${var.vpc_name}_automation_dev"
  public_key = var.kube_ssh_key
}


# user.yaml bucket read policy
# This bucket is in the 'bionimbus' account -
#   modify the permissions there as necessary.  Ugh.

