$ORIGIN .
$TTL 60

i.ajkdns.com  IN SOA i.ajkdns.com. root.i.ajkdns.com. (
                {{date}} ; serial
                1800       ; refresh (30 minutes)
                86400      ; retry (1 day)
                2419200    ; expire (4 weeks)
                604800     ; minimum (1 week)

)

        NS  ns1.ajkdns.com.
        NS  ns3.ajkdns.com.
        NS  ns4.ajkdns.com.


$ORIGIN i.ajkdns.com.

{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}
