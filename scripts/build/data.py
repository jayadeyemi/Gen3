#!/usr/bin/env python3
from string import Template

# Descriptions for controllers
controller = "data"
description = "Chart for Data Resources on AWS"
add_description_override(full_descriptions, controller, description)

# insert controller name into chart stub
data_chart_stub1 = Template("""apiVersion: v2
name: $controller
description: $descriptions
version: 0.1.0
appVersion: "latest"
dependencies:
  - name: _globals
    repository: file://../_globals
    version: 0.1.0
""")
data_chart_stub1 = data_chart_stub1.substitute(controller=controller, descriptions=description)
add_value_override(chart_overrides, controller, data_chart_stub1)

data_values_stub1 = """enabled: true

# ──────────────────────────────────────────────────────────────────
# RDS (three standalone instances OR Aurora)
# ──────────────────────────────────────────────────────────────────
deployAurora:           false
aurora:
  clusterIdentifier:    aurora-cluster
  instanceIdentifier:   aurora-cluster-instance
  engine:               aurora-postgresql
  engineVersion:        "13.7"
  instanceClass:        db.serverless
  engineMode:           provisioned
  serverlessV2Scaling:
    minACU:            "0.5"
    maxACU:            "8"
  storageEncrypted:     true
  applyImmediate:       true
  masterUsername:       postgres
  password:             ""     # use Secrets

standaloneRds:
  deployRds:            true
  fence:
    size:              10
    instance:          db.t3.small
    password:          ""
  sheepdog:
    size:              10
    instance:          db.t3.small
    password:          ""
  indexd:
    size:              10
    instance:          db.t3.small
    password:          ""

rdsInstanceStorageEncrypted: true
rdsMaxAllocated:
  fence:              0
  sheepdog:           0
  indexd:             0

# ──────────────────────────────────────────────────────────────────
# Elasticsearch / OpenSearch
# ──────────────────────────────────────────────────────────────────
deployEs:               true
es:
  name:                ""
  instanceType:        m4.large.elasticsearch
  instanceCount:       3
  volumeSize:          20
  version:             "7.10"
  encryption:          true
  linkedRole:          true
  roleArn:             ""

# ──────────────────────────────────────────────────────────────────
# S3 buckets (manifest & users bucket)
# ──────────────────────────────────────────────────────────────────
manifestBuckets:
  - nameSuffix:        manifestservice
    aesEncryption:     false
    kmsKeyId:          ""
    versioning:        false
    publicAccessBlock: true
    bucketLifecycle:   ""
    loggingBucketName: ""
    ownership:         BucketOwnerPreferred
    policyRoleArn:     ""

# users bucket for config-reader policy
usersBucketName:        cdis-gen3-users
configFolder:           dev

# ──────────────────────────────────────────────────────────────────
# Random passwords & crypto keys (all generated if blank)
# ──────────────────────────────────────────────────────────────────
randomSecrets:
  hmacEncryptionKey:    ""
  sheepdogSecretKey:    ""
  sheepdogIndexdPassword:""
  passwordLength:       20
"""
add_value_override(values_overrides, controller, data_values_stub1)

wafv2_template_stub1_1 = """{{- if .Global.Values.installCRD }}
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: webacls.wafv2.services.k8s.aws
  annotations:
    controller-gen.kubebuilder.io/version: v0.16.2
spec:
  group: wafv2.services.k8s.aws
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                name:
                  type: string
                scope:
                  type: string
                description:
                  type: string
                defaultAction:
                  type: object
                rules:
                  type: array
                visibilityConfig:
                  type: object
                tags:
                  type: object
      subresources:
        status: {}
  scope: Namespaced
  names:
    plural: webacls
    singular: webacl
    kind: WebACL
    shortNames:
      - waf
{{- end }}
"""
add_template_stub(template_overrides, controller, "web-acl-crd.yaml", wafv2_template_stub1_1)

wafv2_template_stub1_2 = """{{- if .Values.enabled }}
{{- $vpc := include "waf.vpcname" . | required "global.vpcName vpcName must be set" }}
apiVersion: wafv2.services.k8s.aws/v1alpha1
kind: WebACL
metadata:
  name: {{ include "waf.fullname" . }}
  labels:
    {{ include "waf.labels" . | indent 4 }}
spec:
  name: {{ required "Values.vpcName is required" .Values.Global.vpcName | printf "%s-waf" }}
  description: {{ .Values.description | quote }}
  scope: {{ .Values.scope | upper }}
  defaultAction:
    allow: {}
  rules:
    {{- $all := append .Values.baseRules .Values.additionalRules }}
    {{- range $i, $r := $all }}
    - name: AWS-{{ $r.managedRuleGroupName }}
      priority: {{ $r.priority }}
      overrideAction:
        none: {}
      statement:
        managedRuleGroupStatement:
          vendorName: AWS
          name: {{ $r.managedRuleGroupName | quote }}
          {{- if $r.overrideToCount }}
          ruleActionOverrides:
            {{- range $r.overrideToCount }}
            - name: {{ . | quote }}
              actionToUse:
                count: {}
            {{- end }}
          {{- end }}
      visibilityConfig:
        sampledRequestsEnabled: true
        cloudwatchMetricsEnabled: true
        metricName: AWS-{{ $r.managedRuleGroupName }}
    {{- end }}
{{ include "waf.tags" . | indent 2 }}
  visibilityConfig:
    cloudwatchMetricsEnabled: {{ .Values.visibilityConfig.cloudwatchMetricsEnabled }}
    sampledRequestsEnabled: {{ .Values.visibilityConfig.sampledRequestsEnabled }}
    metricName: {{ .Values.visibilityConfig.metricName | quote }}
{{- else }}
# WAF is disabled; no WebACL will be created.
{{- end }}
"""
add_template_stub(template_overrides, controller, "web-acl.yaml", wafv2_template_stub1_2)

wafv2_helper_stub1_1 = """{{- /*
Return the chart's fullname: <release-name>-<chart-name>
*/ -}}
{{- define "waf.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- /*
Common labels for all resources
*/ -}}
{{- define "waf.labels" -}}
app.kubernetes.io/name: {{ include "waf.fullname" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- /*
Helper to render .Values.tags YAML with templating
*/ -}}
{{- define "waf.vpcname" -}}
{{ .Values.Global.vpcName }}
{{- end -}}
{{- define "waf.tags" -}}
tags: |
  Environment: {{ include "waf.vpcname" . }}
  Owner: {{ .Release.Service }}
  Project: {{ .Release.Name }}
  Organization: {{ .Values.organization }}
{{- end -}}
"""
add_helper_stub(helper_overrides, controller, "helpers.tpl", wafv2_helper_stub1_1)