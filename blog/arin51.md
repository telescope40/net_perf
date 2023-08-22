# ARIN 51 

I was fortunate enough to be selected to particpate in the ARIN51 fellowship program attending the event in Tampa gave 
me a glimpse of how the policies discussed shape the broader internet. ARIN 51 discussed a number of draft policy 
recommendations , service improvements , and community grants initatives. 

### **Secure Routing**
One the key themes of ARIN 51 in my opinion was RPKI. Securing routing is clearly of the most important initiatves based 
on the ROA-Thon hosted by Brad Gorman , The Draft Policy Recommendations ARIN-2021-8 , The Grants Presentation from the
DNS Research Federation on the state of RPKI. 

**The Draft Policy Recommendations ARIN-2021-8**
This was a Draft Policy Recommendation to remove the ‘Autonomous System Originations’ Field. The OriginAS field has
real world use case for organizations that do not use Internet Routing Registries which groups Public Prefixes --- ASN 
under some object name . While most organization are likley using IRR , With removing the OrginAS field and the 
retirement of the legacy unauthorized ARIN-NONAUTH IRR. The community is driven to making routing more secure and 
embracing solutions that ensure more accurate , cryotographic secure records. 

**"ROA-THON"**
The ROA-THON hosted by Brad Gorman, where  explained the technical details , benefits and limits of how RPKI can create \
more secure routing and how the hosted ARIN RPKI product functions today and new features such as certificates never expiring.  
The key take away from the ROA-THON , lunch tabletop topics and presentation is to at LEAST sign the ROA for the resources
, even if your organization is not ready to make decision with RPKI , Signing the routes only benefits and protects 
the resource holder. 


#### **Tech Brief of RPKI**
I recommend reviewing `https://rpki.readthedocs.io/en/latest/` in details for specifics. 
- Great tool  `https://irrexplorer.nlnog.net/`
- Resource Public Key Infrastructure - RPKI 
- Route Origin Authorization - ROA
- Allows Holders of Internet Number Resources to make signed statements about them 
- Third Party resources can download these statements as x509 Certificates 
- These signed certificates assure that a person who administers the Number Resources. Limits attack Surface 
- Does not address Path Validation 
- ROAs allow holders to secure resources so ISPs that make decisions based on RPKI can ensure validity of the ROA
- Protects against BGP Hijacking 
- Protects against human error , ROA have prefix lengths that can be used to ensure correct advertisements are expected
- There is a limit of 100,000 ROA for an organization and a limite 20,000 ROAs that can be revoked at any given time 
  *This is for ARIN HOSTED RPKI*

**DNS Research Federation** 
ARIN provides grants to orgsanization that aim to improve the overall intenet. One of the grant recepients was the DNS
Research Federation. `https://dnsrf.org/` DNSRF was given a grant to evaluate the state of deployment of RPKI in the ARIN 
region and encourage greater scrutiny over routing and security . 
The project analyzed the number of RPKIs in use ARIN for ipv4 , ipv6 versus the global deployment. The ARIN region has 
about 25% of IPv4 covered under RPKLI and ~50% for ipv6. 




### **IPV6**
Since ARIN is one the five RIR responsible for adminstring policy for Numbered Resources , it is in the best interest
to move away from the scarcity limitation that ipv4 address space is facing. During ARIN 51 there was a number of success
stories of IPV6 deployments including for speakers from Virgina Tech , AWS and Telus. 
All of these institutions deployed ipv6 into their networks , Virgina Tech did it 25 years ago ! The mobile carriers of the 
world are IPV6 .The point is that ipv6 is a real , robust protocol that is becoming superior to *legacy ip*. 
Albeit some challenges with IPv6 are in the application development space , if an organization treats ipv6 as a requirement 
wants to  *simplifying* their network (GOODBYE NAT!) . IPv6 is an excellent solution that is not that difficult to deploy considering. 

**Number Resource Policy Manual & IPv6** 
One of the more interesting items I discovered is that ARIN in order to facilitate the adoption of IPV6 makes special use 
cases of IPv4 including micro-allocation to support network infrastructure. Under NRPM section 4.4 this allocation includes
space for Internet Peering Exchange points. I found it interesting since this is services like de-cix which I realized 
when reading the IP Assignments. 
NRPM Section 4.10 is also another interesting item , under this policy , ARIN set aside a /10 of ipv4 space to promote ipv6
deloyments. An applicant must demonstrate an immediate need for a dual stack deployment and never recieved resources under
the policy previously nor have other allocations that will satisfy the need. 

- `https://www.arin.net/reference/research/statistics/microallocations/`



### Comm 
**NTP**


The Internet Number Registry System 
- https://www.rfc-editor.org/rfc/rfc7020.html


RPKI 
- Hosted RPKI vs Delegated 
- Changes to the services at ARIN 
- https://irrexplorer.nlnog.net/
- 


IPV6 
- Success stories

IANA 
- Trusted Signers for DNS 

ARIN Advisory Council 

NRPM

NRO 
- the function of how rir collaborate 
- Agreements for the Internet Number Registry System 
- 3 new programs for the NRO 
  - RPKI 
  - Cybersecurity 
  - Gov Engagement 
  - ASRO , NRO , IANA Review committee meeting 
  - NRO Meetings 
- RPKI Adoption reports 
  - nro.net/statistics 
- IANA Review Committee
  - New ASN or IPv6 Block requests from IANA from any of the RIR 
  - three members from each RIR 
  - 



ASO 
