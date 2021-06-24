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

Note that if the "proxied_hostname" is "0.0.0.0", the WAF can easily be bypassed by finding the new port of the service with nmap. <br>
Anyway, even if you change it, the port is still exposed, because you can't make a docker listen on localhost and access it externally. <br>
So you have to block access to the new port of the service for all IP addresses except the IP address of the waf. <br>
Start the WAF and find its IP address in the local network by accessing the docker: <br>

```
docker ps
docker exec -it <id_of_waf_container> /bin/bash
ip address
```

Now, on your host system OR in your vulnerable service's docker (the second solution is preferred if you have iptables installed in the docker): <br>

```
iptables -A INPUT -p tcp --dport <new port of vulnerable service> -s <ip address of the waf> -j ACCEPT
iptables -A INPUT -p tcp --dport <new port of vulnerable service> -j DROP
```

Note that "new port of vulnerable service" is actually the new port of vulnerable service only if you are issuing these commands on the host system; if you are issuing them inside the docker, you must use the internal port.
