$ORIGIN fang.anjuke.com.
$TTL 60 ; 1 day

@  IN SOA ns.fang.anjuke.com. root.fang.anjuke.com. (
        {{date}} ; serial time()
        1800                ; Refresh
        600                 ; Retry
        3600               ; Expire
        3600 )             ; Negative Cache TTL

                86400        NS          ns1.ajkdns.com.
                86400        NS          ns3.ajkdns.com.
                86400        NS          ns4.ajkdns.com.


{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}
