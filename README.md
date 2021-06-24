# py-waf

A simple, self-contained python proxy to be used as a WAF. <br>
It's not perfect because it's not easy to build a generic proxy, but it's a good starting point. <br>
I think that the best way to use it is to adapt it to the service to be protected, defining the appropriate routes and their parameters. <br>
It could be useful in attack/defense CTFs: you use different instances of this waf, with modified code, and you configure config.json in /volume: <br>

```
{
	"proxied_hostname": <ip address of the docker of the vulnerable service>,
	"proxied_port": <new port of the docker of the vulnerable service>,
	"waf_hostname": "0.0.0.0",
	"waf_port": <original port of the vulnerable service>,
	"debug": false
}
```

Note that if you set "proxied_hostname" to "0.0.0.0", the WAF can easily be bypassed by finding the new port of the service with nmap. <br>
