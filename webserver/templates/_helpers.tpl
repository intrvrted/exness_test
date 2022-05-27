{{/*
Define the name of the chart.
*/}}
{{- define "webserver.fullname" -}}
{{- default .Chart.Name | trunc 63 }}
{{- end }}
