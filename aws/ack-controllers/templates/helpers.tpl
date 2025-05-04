{{- /*
Return the chart's fullname: <vpcName>-<environment>-ack
This is used to name the namespace for the umbrella chart.
*/ -}}
{{- define "ack.fullname" -}}
{{ printf "%s-%s-ack" .Values.global.vpcName Values.global.environment }}
{{- end -}}

