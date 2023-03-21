## NYNOG March 2023
Recently I was selected to give a presentation at the New York Network Operators Group. 
This is an orgranization I have attended a number of events over the years. 
This was the first time I ever gave a technical talk 

The title of my chat was **Skills Development for a Changing Technical Landscape**. The aim of 
my talk was to go over a terse overview of my path from Network Engineer to one who 
makes uses of some tools to operate more effectively in a GitOps , Devops world. 

### Python 
The aim of my discussion was to visit that Python but scripting in general became better when I made it a habit. 
I was able to make Python relevant to myself but starting with modules and libraries that were relevant to Net Eng.
Modules like `ipaddress` and 'netutils' gave way for me to make some tooling like a subnet calculator , and more. 

I later moved on to creating iptool sets of my own to get basic details on either ipaddress or prefixes. 
Some basic logic would sort which 
- Check if Address or Network 
- Port knock on common service ports 
- Return DNS record 
- Return GEO IP Location 
- Basic Subnet Calculator 

All of the scripts are on my public git repo 

#### Python Libraries & Modules
The following libraries and modules helped me create these tools 
*requests* 
 - Make Curl like commands to grab data over HTTP  
*socket*  
 - Low level OS module to make system calls like ping 
*ipaddress* 
 - Great module , used this to create my own subnet calculator , ping sweeper and others 
*whois* 
 - whois but with python , look up AS 
*netutils*
 - POWERFUL , LOAD Network Library , I cant understate this one. 

#### Key Take Aways from Python
- Python Libraries & Modules
  - Both collections of code but with different limits. 
- Libraries are a collection of Modules & Packages 
- Modules are collection of functions 

- PEP - Python Enhancement Proposal 
  - Used to document features & standards . Similar to RFC

- PIP - Python Package Installer 
  - Easy to Install / Uninstall packages 
  - Solving Dependency issues 



### GIT 

