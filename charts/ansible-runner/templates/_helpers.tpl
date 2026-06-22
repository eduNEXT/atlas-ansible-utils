{{/*
Expand the name of the chart.
*/}}
{{- define "ansible-runner.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "ansible-runner.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "ansible-runner.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create Ansible Runner app version
*/}}
{{- define "ansible-runner.defaultTag" -}}
{{- default .Chart.AppVersion .Values.image.tag }}
{{- end -}}

{{- define "ansible-runner.namespace" -}}
{{- default .Release.Namespace .Values.namespaceOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "ansible-runner.labels" -}}
helm.sh/chart: {{ include "ansible-runner.chart" . }}
{{ include "ansible-runner.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "ansible-runner.selectorLabels" -}}
app.kubernetes.io/name: {{ include "ansible-runner.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
AWS credentials Secret name for SSM mode
*/}}
{{- define "ansible-runner.awsSecretName" -}}
{{- if .Values.aws.existingSecret -}}
{{- .Values.aws.existingSecret -}}
{{- else -}}
aws-credentials
{{- end -}}
{{- end -}}

{{/*
Validate connection-specific required configuration
*/}}
{{- define "ansible-runner.validateConnectionConfig" -}}
{{- if eq .Values.connection.type "ssm" -}}
{{- if and (not .Values.aws.existingSecret) (or (not .Values.awsSecret.accessKeyId) (not .Values.awsSecret.secretAccessKey)) -}}
{{- fail "connection.type is ssm but neither aws.existingSecret nor awsSecret credentials are configured" -}}
{{- end -}}
{{- else if eq .Values.connection.type "ssh" -}}
{{- if not .Values.sshSecret.key -}}
{{- fail "connection.type is ssh but sshSecret.key is not configured" -}}
{{- end -}}
{{- else -}}
{{- fail (printf "connection.type must be ssh or ssm, got %q" .Values.connection.type) -}}
{{- end -}}
{{- end -}}
