#!/usr/bin/env python3
from string import Template

# Descriptions for controllers
controller = 'ack-controller'
description = 'Umbrella Chart for all Resources on AWS'
add_description_override(full_descriptions, controller, description)

# Chart.yaml stub
glob_chart_stub1 = Template('''apiVersion: v2
name: $controller
description: $descriptions
version: 0.1.1
type: application
appVersion: "master"

dependencies:
  - name: ack-controllers
    version: 46.22.5
    repository: "oci://public.ecr.aws/aws-controllers-k8s/ack-chart"
''')
glob_chart_stub1 = glob_chart_stub1.substitute(controller=controller, descriptions=description)
add_chart_stub(chart_overrides, controller, 'Chart.yaml', glob_chart_stub1)

# values.yaml stub
glob_values_stub1 = '''# Default values for global chart
global:
  enabled: true
  vpcName: "Commons1"
  organization: "Basic Service"

  awsRegion: "us-east-1"
  awsEndpointUrl: ""

controller:
  namespace: ack-system
  replicas: 1

  enableDevelopmentLogging: false
  logLevel: info
  watchNamespace: ""

  reconcileDefaultMaxConcurrentSyncs: 1
  featureGates: ""

  resourceTags: ""

  leaderElection:
    enabled: false
    namespace: leader-election-namespace

  image:
    repository: controller
    tag: latest

  resources:
    requests:
      cpu: 100m
      memory: 200Mi
    limits:
      cpu: 100m
      memory: 300Mi

# controller enabled?
acm:
  enabled: false
acmpca:
  enabled: false
applicationautoscaling:
  enabled: false
cloudfront:
  enabled: false
cloudtrail:
  enabled: false
cloudwatch:
  enabled: false
cloudwatchlogs:
  enabled: false
ec2:
  enabled: false
ecr:
  enabled: false
ecs:
  enabled: false
eks:
  enabled: false
elbv2:
  enabled: false
emrcontainers:
  enabled: false
iam:
  enabled: false
kms:
  enabled: false
lambda:
  enabled: false
opensearchservice:
  enabled: false
rds:
  enabled: false
route53resolver:
  enabled: false
s3:
  enabled: false
s3control:
  enabled: false
secretsmanager:
  enabled: false
sns:
  enabled: false
sqs:
  enabled: false
wafv2:
  enabled: false
'''
add_value_override(values_overrides, controller, glob_values_stub1)

glob_template_stub1_1 = """{{- $g := .Values.global -}}
{{- $c := .Values.controller -}}
{{- range .Dependencies }}
{{- if .Enabled }}

---
apiVersion: v1
kind: Namespace
metadata:
  name: {{ $c.namespace }}

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ack-{{ .Name }}-controller
  namespace: {{ $c.namespace }}
  labels:
    app.kubernetes.io/name: ack-{{ .Name }}-controller
    app.kubernetes.io/part-of: {{}}
spec:
  replicas: {{ $c.replicas }}
  selector:
    matchLabels:
      app.kubernetes.io/name: ack-{{ .Name }}-controller
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ack-{{ .Name }}-controller
    spec:
      serviceAccountName: ack-{{ .Name }}-controller
      securityContext:
        seccompProfile:
          type: RuntimeDefault
      terminationGracePeriodSeconds: 10
      containers:
      - name: controller
        image: {{ $c.image.repository }}:{{ $c.image.tag }}
        args:
        - --aws-region
        - "{{ $g.awsRegion }}"
        - --aws-endpoint-url
        - "{{ $g.awsEndpointUrl }}"
        - --enable-development-logging={{ $c.enableDevelopmentLogging }}
        - --log-level
        - "{{ $c.logLevel }}"
        - --watch-namespace
        - "{{ $c.watchNamespace }}"
        - --reconcile-default-max-concurrent-syncs
        - "{{ $c.reconcileDefaultMaxConcurrentSyncs }}"
        - --feature-gates
        - "{{ $c.featureGates }}"
        - --resource-tags
        - "{{ $c.resourceTags }}"
        - --enable-leader-election={{ $c.leaderElection.enabled }}
        - --leader-election-namespace
        - "{{ $c.leaderElection.namespace }}"
        env:
        - name: AWS_REGION
          value: "{{ $g.awsRegion }}"
        - name: AWS_ENDPOINT_URL
          value: "{{ $g.awsEndpointUrl }}"
        - name: ACK_ENABLE_DEVELOPMENT_LOGGING
          value: "{{ $c.enableDevelopmentLogging }}"
        - name: ACK_LOG_LEVEL
          value: "{{ $c.logLevel }}"
        - name: ACK_RESOURCE_TAGS
          value: "{{ $c.resourceTags }}"
        - name: ACK_WATCH_NAMESPACE
          value: "{{ $c.watchNamespace }}"
        - name: ENABLE_LEADER_ELECTION
          value: "{{ $c.leaderElection.enabled }}"
        - name: LEADER_ELECTION_NAMESPACE
          value: "{{ $c.leaderElection.namespace }}"
        - name: RECONCILE_DEFAULT_MAX_CONCURRENT_SYNCS
          value: "{{ $c.reconcileDefaultMaxConcurrentSyncs }}"
        - name: FEATURE_GATES
          value: "{{ $c.featureGates }}"
        resources:
          requests:
            cpu: {{ $c.resources.requests.cpu }}
            memory: {{ $c.resources.requests.memory }}
          limits:
            cpu: {{ $c.resources.limits.cpu }}
            memory: {{ $c.resources.limits.memory }}

{{- end }}
{{- end }}
"""
add_template_stub(template_overrides, controller, "deployment.yaml", glob_template_stub1_1)