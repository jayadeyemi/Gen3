#!/usr/bin/env python3
from string import Template

# Descriptions for controllers
controller = "network"
description = "Chart for Network Resources on AWS"
add_description_override(full_descriptions, controller, description)

# insert controller name into chart stub
ntwk_chart_stub1 = Template("""apiVersion: v2
name: $controller
description: $descriptions
version: 0.1.0
appVersion: "latest"
dependencies:
  - name: _globals
    repository: file://../_globals
    version: 0.1.0
""")
ntwk_chart_stub1 = ntwk_chart_stub1.substitute(controller=controller, descriptions=description)
add_value_override(chart_overrides, controller, ntwk_chart_stub1)

ntwk_values_stub1 = """enabled: true

# ──────────────────────────────────────────────────────────────────
# VPC & basic networking
# ──────────────────────────────────────────────────────────────────
vpc:
  cidrBlock:           172.24.17.0/20
  secondaryCidrBlock:  ""
  flowLogs:
    enabled:          false
    trafficType:      ALL
  peering:
    cidr:             10.128.0.0/20
    peerVpcId:        vpc-e2b51d99
    create:           true
  csocManaged:        true

sshKeyName:            ""
csocAccountId:         "433568766270"

# ha‑squid / proxy
squid:
  deployHa:            false
  deploySingle:        false
  instanceType:        t3.medium
  instanceDriveSize:   8
  imageSearch:         "ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"
  bootstrapScript:     squid_running_on_docker.sh
  extraVars:           ""
  branch:              master

# Route 53 private zone
route53:
  internalZoneId:      ""

# Flow‑log IAM toggle (if you prefer separate role here)
flowLogIam:
  createRole:          true
"""
add_value_override(values_overrides, controller, ntwk_values_stub1)

vpc_vpc_stub1_1 = """{{- if .Values.enabled }}
apiVersion: ec2.services.k8s.aws/v1alpha1
kind: VPC
metadata:
  name: {{ .Release.Name }}-vpc
spec:
  cidrBlock: {{ .Values.vpc.cidrBlock | quote }}
{{- end }}
"""
add_template_stub(template_overrides, controller, "vpc.yaml", vpc_vpc_stub1_1)

vpc_subnet_stub1_2 = """{{- if .Values.enabled }}
{{- range .Values.subnets }}
apiVersion: ec2.services.k8s.aws/v1alpha1
kind: Subnet
metadata:
  name: {{ .name }}
spec:
  cidrBlock: {{ .cidrBlock | quote }}
  vpcRef:
    name: {{ $.Release.Name }}-vpc
{{- end }}
{{- end }}
"""
add_template_stub(template_overrides, controller, "subnet.yaml", vpc_subnet_stub1_2)

