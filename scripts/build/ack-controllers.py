#!/usr/bin/env python3
from string import Template

# Descriptions for controllers
controller = 'ack-controllers'
description = 'Umbrella Chart for all Resources on AWS'
add_description_stub(description_overrides, controller, description)

# Chart.yaml stub
glob_chart_stub1 = Template('''apiVersion: v2
name: $controller
description: $descriptions
version: 0.1.1
type: application
appVersion: "master"
dependencies:
  - name: acm-chart
    alias: acm
    version: 1.0.8
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: acm.enabled
  - name: apigateway-chart
    alias: apigateway
    version: 1.1.0
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: apigateway.enabled
  - name: cloudfront-chart
    alias: cloudfront
    version: 1.0.10
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: cloudfront.enabled
  - name: cloudtrail-chart
    alias: cloudtrail
    version: 1.0.22
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: cloudtrail.enabled
  - name: ec2-chart
    alias: ec2
    version: 1.4.3
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: ec2.enabled
  - name: eks-chart
    alias: eks
    version: 1.7.1
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: eks.enabled
  - name: kms-chart
    alias: kms
    version: 1.0.25
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: kms.enabled
  - name: lambda-chart
    alias: lambda
    version: 1.6.4
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: lambda.enabled
  - name: s3-chart
    alias: s3
    version: 1.0.29
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: s3.enabled
  - name: sqs-chart
    alias: sqs
    version: 1.1.10
    repository: oci://public.ecr.aws/aws-controllers-k8s
    condition: sqs.enabled
''')
glob_chart_stub1 = glob_chart_stub1.substitute(controller=controller, descriptions=description)
add_chart_stub(chart_overrides, controller, glob_chart_stub1)

# values.yaml stub
glob_values_stub1 = '''# Default values for global chart
global:
  aws:
  vpcName: "Commons1"
  environment: "prod"
  organization: "Basic Service"

  awsRegion: "us-east-1"
  awsEndpointUrl: ""



acm:
  enabled: false
acmpca:
  enabled: false
ecr:
  enabled: false
ecs:
  enabled: false
elbv2:
  enabled: false
emrcontainers:
  enabled: false

applicationautoscaling:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

cloudfront:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

cloudtrail:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

cloudwatch:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

cloudwatchlogs:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

ec2:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
  watchNamespace: [] 
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

eks:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

iam:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

kms:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

lambda:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

opensearchservice:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

rds:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

route53resolver:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

s3:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

s3control:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

secretsmanager:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

sns:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

sqs:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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

wafv2:
  enabled: true
  namespace: ack-system
  replicas: 1
  enableDevelopmentLogging: false
  logLevel: info
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
'''
add_values_stub(values_overrides, controller, glob_values_stub1)

glob_template_stub1_1 = """{{- range $ctrl, $cfg := .Values }}
  {{- if and (kindIs "map" $cfg) ($cfg.enabled | default false) }}
apiVersion: v1
kind: Namespace
metadata:
  name: {{ include "ack.fullname" $ }}
  labels:
    name: {{ include "ack.fullname" $ }}
{{- end }}
{{- end }}
"""
add_template_stub(template_overrides, controller, "namespace.yaml", glob_template_stub1_1)

glob_template_stub1_3 = """{{- range $ctrl, $cfg := .Values }}
  {{- if and (kindIs "map" $cfg) ($cfg.enabled | default false) }}
    {{- define "ack.ctrlname" -}}
    {{ printf "%s-%s-ack" .Values.global.vpcName $ctrl }}{{- end -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "ack.ctrlname" $ }}
  namespace: {{ include "ack.fullname" $ }}
  labels:
    app.kubernetes.io/name: {{ include "ack.ctrlname" $ }}
    app.kubernetes.io/part-of:  {{ .Release.Name }}
spec:
  replicas: {{ $cfg.replicas }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "ack.ctrlname" $ }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "ack.ctrlname" $ }}
    spec:
      serviceAccountName: {{ printf "%s-%s-ack-sa" .Values.global.vpcName $ctrl }}
      containers:
        - name: controller
          image: {{ $cfg.image.repository }}:{{ $cfg.image.tag }}
          args:
            - --aws-region
            - {{ $.Values.global.awsRegion | quote }}
            - --aws-endpoint-url
            - {{ $.Values.global.awsEndpointUrl | quote }}
            - --enable-development-logging={{ $cfg.enableDevelopmentLogging }}
            - --log-level
            - {{ $cfg.logLevel | quote }}
            - --resource-tags
            - {{ $cfg.resourceTags | quote }}
            - --enable-leader-election={{ $cfg.leaderElection.enabled }}
            {{- if $cfg.leaderElection.enabled }}
            - --leader-election-namespace
            - {{ $cfg.leaderElection.namespace | quote }}
            {{- end }}
            - --watch-namespace
            - {{ include "ack.fullname" $ }}
          env:
            - name: WATCH_NAMESPACE
              value: {{ include "ack.fullname" $ }}
            - name: AWS_REGION
              value: {{ $.Values.global.awsRegion | quote }}
            - name: AWS_ENDPOINT_URL
              value: {{ $.Values.global.awsEndpointUrl | quote }}
            - name: ENABLE_DEVELOPMENT_LOGGING
              value: {{ $cfg.enableDevelopmentLogging | quote }}
            - name: LOG_LEVEL
              value: {{ $cfg.logLevel | quote }}
            - name: ENABLE_LEADER_ELECTION
              value: {{ $cfg.leaderElection.enabled | quote }}
            - name: LEADER_ELECTION_NAMESPACE
              value: {{ $cfg.leaderElection.namespace | quote }}

          resources:
            {{- toYaml $cfg.resources | nindent 12 }}
  {{- end }}
{{- end }}
"""
add_template_stub(template_overrides, controller, "deployment.yaml", glob_template_stub1_3)

glob_template_stub1_4 = """{{- range $ctrl, $cfg := .Values }}
  {{- if and (kindIs "map" $cfg) ($cfg.enabled | default false) ($cfg.leaderElection.enabled | default false) }}
---
apiVersion: v1
kind: Namespace
metadata:
  name: {{ $cfg.leaderElection.namespace }}
  labels:
    {{- include "ack.labels" $ | nindent 4 }}
{{- end }}
{{- end }}
"""
add_template_stub(template_overrides, controller, "leader-election.yaml", glob_template_stub1_4)

glob_helper_stub1_1 = """{{- /*
Return the chart's fullname: <vpcName>-<environment>-ack
This is used to name the namespace for the umbrella chart.
*/ -}}
{{- define "ack.fullname" -}}
{{ printf "%s-%s-ack" .Values.global.vpcName Values.global.environment }}
{{- end -}}
"""
add_helper_stub(helper_overrides, controller, "helpers.tpl", glob_helper_stub1_1)

glob_notes_stub1 = """The umbrella chart installs AWS ACK controllers selected in `values.yaml`.

• Each controller Deployment lives in the `ack-system` namespace (or the
  namespace you set in its block).
• Disable or tune a controller simply by editing values and running:
    helm upgrade --install <release> .
"""
add_notes_stub(notes_overrides, controller, "_helpers.tpl", glob_notes_stub1)