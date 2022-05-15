### Out4Vuln  (*Under maintainence*)
Web vulnerability scanner and OSINT tool.
---

Out4Vuln is a basic web application vulnerability scanner written from scratch. It employs older projects of mine [ Raptor ](https://github.com/HJ23/Raptor) and UrlGatherer.

Still improving its functionalities and adding new modules to make it more capable. This scanner consists of
two main components OSINT finder and Vulnerability finder.

OSINT finder uses different API's as well as free resources to identify attack surface.

On the other hand Vulnerability finder fuzz's for vulnerabilities.

For better results I highly encourage you to get API keys.

Think this is useful? ⭐ Star us on GitHub — it helps!

Out4Vuln can :

- Find subdomains of given domain (active,passive)
- Find all the available url's (passive,active)
- Classify found urls for better understanding
- Fuzz for hidden directories
- Bypass 403 unauthorized code
- Has Out-Of-Bound plugin
- Hidden API key finder
- HttpProber
- Spider
- Slack notifier
- Nmap plugin
- HTML report generator

---

Currently can identify:

-    Open-redirect
-    Host Header Injection
-    LFI 
-    CRLF injection

and many more will be added soon.


TODO list:

- [ ] add oob support
- [ ] WAF detect (bypass techniques 8mb limits,obfuscated payloads)
- [ ] proxy option
- [ ] cidr,ip port range
- [ ] Vulnerable lib/soft version detect
- [ ] CMS detector
- [ ] Routing over TOR
- [ ] Scan modes Light,Medium,Aggressive
- [ ] Handle nmap outputs
- [ ] Active subdomain support