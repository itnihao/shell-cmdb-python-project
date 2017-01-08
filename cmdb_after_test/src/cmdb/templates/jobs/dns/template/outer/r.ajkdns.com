$ORIGIN .
$TTL 60

r.ajkdns.com  IN SOA r.ajkdns.com. root.r.ajkdns.com. (
                {{date}} ; serial
                1800       ; refresh (30 minutes)
                86400      ; retry (1 day)
                2419200    ; expire (4 weeks)
                604800     ; minimum (1 week)

)

        NS  ns1.ajkdns.com.
        NS  ns3.ajkdns.com.
        NS  ns4.ajkdns.com.


$ORIGIN r.ajkdns.com.

{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}
