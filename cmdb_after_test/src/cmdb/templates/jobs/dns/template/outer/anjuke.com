$ORIGIN anjuke.com.
$TTL 60 ; 1 day

@  IN SOA ns.anjuke.com. root.anjuke.com. (
        {{date}} ; serial time()
        1800                ; Refresh
        600                 ; Retry
        3600               ; Expire
        3600 )             ; Negative Cache TTL

                86400        NS          ns1.ajkdns.com.
                86400        NS          ns3.ajkdns.com.
                86400        NS          ns4.ajkdns.com.

corp                         NS          ns1.ajkdns.com.
corp                         NS          ns3.ajkdns.com.
corp                         NS          ns4.ajkdns.com.
fang                         NS          ns1.ajkdns.com.
fang                         NS          ns3.ajkdns.com.
fang                         NS          ns4.ajkdns.com.
qa                  3600     NS          ns.vm.qa.test1


{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}
