$ORIGIN corp.anjuke.com.
$TTL 60 ; 1 day

@  IN SOA ns.corp.anjuke.com. root.corp.anjuke.com. (
        {{date}} ; serial time()
        1d 3d 1w 1d
)

        NS  ns1.ajkdns.com.
        NS  ns3.ajkdns.com.
        NS  ns4.ajkdns.com.


{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}


