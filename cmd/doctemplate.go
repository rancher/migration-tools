package cmd

const (
	documentedConstructs = `
Certs:
  name: certs
CgroupParent:
  name: cgroup_parent
DefaultCert:
  name: default_cert
DNS:
  name: dns
DNSOpt:
  name: dns_opt
DNSSearch:
  name: dns_search
DeviceReadBps:
  name: device_read_bps
DeviceReadIOps:
  name: device_read_iops
Devices:
  name: devices
DeviceWriteBps:
  name: device_write_bps
DeviceWriteIOps:
  name: device_write_iops
DependsOn:
  name: depends_on
DrainTimeoutMs: 
  name: drain_timeout_ms
Expose:
  name: expose
  doclink: https://rancher.com/blog/2018/2018-08-14-expose-and-monitor-workloads/
  helptext: Please add a hostPort or a nodePort to your Kubernetes workload to expose the ports used.
ExternalIps:
  name: external_ips
ExternalLinks:
  name: external_links
  doclink: https://rancher.com/blog/2018/2018-09-04-service_discovery_2dot0/
  helptext: Please add the necessary Service Discovery Records for your Rancher 2.0 Kubernetes workload to implement the links.
HealthCheck:
  name: health_check
  doclink: https://rancher.com/blog/2018/2018-08-22-k8s-monitoring-and-healthchecks/
  helptext:
Isolation:
  name: isolation
Labels:
  name: labels
  special: true
  doclink:
  helptext:
LbConfig:
  name: lb_config
  doclink: https://rancher.com/blog/2018/2018-09-13-load-balancing-options-2dot0/
  helptext: Please refer to load balancer documentation on Rancher 2.0 for alternatives available.
Links:
  name: links
  doclink: https://rancher.com/blog/2018/2018-09-04-service_discovery_2dot0/
  helptext: Please add the necessary Service Discovery Records for your Rancher 2.0 Kubernetes workload to implement the links.
LegacyLoadBalancerConfig:
  name: load_balancer_config
NetworkMode:
  name: network_mode
Networks:
  name: networks
NetworkDriver:
  name: network_driver
Ports:
  name: ports
  doclink: https://rancher.com/blog/2018/2018-08-14-expose-and-monitor-workloads/
  helptext: Please add a hostPort or a nodePort to your Kubernetes workload to expose the ports used.
RetainIP:
  name: retain_ip
Scale: 
  name: scale
ScalePolicy:
  name: scale_policy
ServiceSchemas:
  name: service_schemas
StorageDriver:
  name: storage_driver
Secrets:
  name: secrets
SecurityOpt:
  name: security_opt
StartOnCreate:
  name: start_on_create
StopSignal:
  name: stop_signal
Sysctls:
  name: sysctls
VolumesFrom:
  name: volumes_from
Volumes:
  name: volumes
VolumeDriver:
  name: volume_driver
UpgradeStrategy:
  name: upgrade_strategy
Ulimits:
  name: ulimits
`

	outputTemplate = `{{- if .serviceConstructs}}## This is the service-wise list of constructs that need to be handled specially.
Please refer https://rancher.com/docs/rancher/v2.x/en/v1.6-migration/ to transition these to Rancher 2.0.
  {{- range $service, $constructsMap := .serviceConstructs}}
{{$service}}:
    {{- range $key, $constructsArray := $constructsMap}}
  {{$key}}:
      {{- range $i, $construct := $constructsArray -}}
	      {{- if ne $construct.Name "" -}}
	        {{- if ne $construct.Name $key}}
    >>{{$construct.Name}}
            {{- if ne $construct.DocLink ""}}
      Refer: {{$construct.DocLink}}
            {{- end -}}
            {{- if ne $construct.HelpText ""}}
      {{$construct.HelpText}}
            {{- end -}}
          {{- else -}}
            {{- if ne $construct.DocLink ""}}
    Refer: {{$construct.DocLink}}
            {{- end -}}
            {{- if ne $construct.HelpText ""}}
    {{$construct.HelpText}}
            {{- end -}}
          {{- end -}}
        {{- end -}}
	    {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end}}

## More Docker/Rancher1.6 constructs that need to be transitioned to Kubernetes/Rancher 2.0 in a special way:
{{- if .usesNetworks}}
  networks
{{- end}}
{{- if .usesVolumes}}
  volumes
{{- end}}
  Rancher Metadata - Incase your applications depend on metadata.
  Rancher 1.6 FQDN resolution format

Please contact Rancher Support for more help to migrate these to Rancher 2.0, as there is no direct translation available.
`
)
