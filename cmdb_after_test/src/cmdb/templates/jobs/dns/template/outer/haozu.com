$ORIGIN haozu.com.
$TTL 60 ; 1 day

@  IN SOA ns.haozu.com. root.haozu.com. (
        {{date}} ; serial time()
        60         ; Refresh
        30         ; Retry
        2419200         ; Expire
        604800 )       ; Negative Cache TTL

        86400        IN      NS      ns1.ajkdns.com.
        86400        IN      NS      ns3.ajkdns.com.
        86400        IN      NS      ns4.ajkdns.com.

qa  3600 NS ns.vm.qa.test1.anjuke.com.
dnspod  NS  ns1.dnsv3.com.
dnspod  NS  ns2.dnsv3.com.

{%for item in domain%}
{{item.prefix}} {{item.type}} {{item.value}}{%endfor%}
