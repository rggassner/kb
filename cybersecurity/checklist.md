# Surface analysis 


1. Check for IPV4 and IPV6 availability. Repeat every check on each stack.

  Tools - ping

2. Check if domain resolves for multiple ip addresses (round robin), and list observed addresses.

  Tools - ping
   
3. Check for opened ports. 

  Tools - nmap (-sV --open -sT)
   
4. Check for robots.txt

  Tools - Browser, wget, curl
  
5. Crawl website within domain in scope.

  Tools - Crawling2sqlite

6. Brute force for directories, files and parameters.

  Tools - dirsearch, dirb, dirbuster
  
7. Inspect page objects.

  Tools - Browser

8. Check for directory traversal candidates.

  Tools - Browser. Yummy files: passwd, cron, vi history, bash history, profile, shadow, logs
  
9. Check for product vulnerability if any description was found in nmap.

  Tools - https://www.cvedetails.com/

10. Check if authentication error message returns valuable information for user enumeration.

  Tools - Browser

11. Check for weak users/passwords.

  Tools - hydra
  
12. Check for user enumeration in email addresses or other content in crawler database.

  Tools - crawling2sqlite
  
13. Check for sqlinjection

  Tools - sqlmap
  
14. Check for XSS

  Tools - browser
  
15. Check for google dorking existence

  Tools - pagodo
  
16. Search for public exposed and password protected documents (pdf, zip, etc) hosted in the domain, and brute force documents.

  Tools - crawling2sqlite, hashcat
  
# Got milk?

1. Check for interfaces addresses and evaluate pivoting.

  Tools - ip, ifconfig

2. Check for arp entrances.

  Tools - arp

3. Evaluate uploading static-binaries 

  Tools - https://github.com/andrew-d/static-binaries
