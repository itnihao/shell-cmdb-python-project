$ORIGIN jinpu.com.
$TTL 60 ; 1 day

@  IN SOA ns.jinpu.com. root.jinpu.com. (
        {{date}} ; serial time()
        1d  6h  3d  600
        )

        86400  NS  ns1.ajkdns.com.
        86400  NS  ns3.ajkdns.com.
        86400  NS  ns4.ajkdns.com.

{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}
