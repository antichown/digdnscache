# -*- coding: utf-8 -*-
from socket import gethostbyname
import sys,os,re, commands

def tumislem(domain):
	try:
		print "Dns Bilgisi"
		print "-------------------------"
		nsbul   = commands.getoutput("dig " + domain+" NS")
		nspattern = re.compile(domain +".\s+\d+\s+IN\s+NS\s+(.*?).\n")
		nsmatch = re.findall(nspattern,nsbul)
		for nscikler in nsmatch:
			print "NS Adres="+nscikler
		nameserver1=nsmatch[0]
		if nameserver1:
			print "işlem yapilacak NS1 Adres:", nameserver1
	except:
		print "hata oluştu, işlem durduruldu"
		exit()

	try:
		print "MX Bilgisi"
		print "-------------------------"
		mxbul   = commands.getoutput("dig " + domain+" MX")
		mxpattern = re.compile(domain +".\s+\d+\s+IN\s+MX\s+(.*?).\n")
		mxmatch = re.findall(mxpattern,mxbul)
		for mxcikler in mxmatch:
			print "MX Adres="+mxcikler
	except:
		print "mx ile oluştu, işlem durduruldu"
	
	print "Recurse Bilgisi"
	print "-------------------------"
	recurseresp = commands.getoutput("dig @" + nameserver1 + " +norecurse")
	answerpattern = re.compile(r",\s+ANSWER:\s+(\d+),")
	answermatch = re.search(answerpattern, recurseresp)
	is_recurse = True if answermatch.group(1) == 1 else False
	print "Recurse  :", is_recurse

	print "Remote Recurse Bilgisi"
	print "-------------------------"
	recurseresp = commands.getoutput("dig @" + nameserver1 + " www.google.com +norecurse")
	answerpattern = re.compile(r",\s+ANSWER:\s+(\d+),")
	answermatch = re.search(answerpattern, recurseresp)
	is_recurse = True if answermatch.group(1) == 1 else False
	print "Remote Recurse Test  :", is_recurse

	#POOR mu

	poorresp = commands.getoutput("dig @" + nameserver1 + " +short porttest.dns-oarc.net TXT")
	is_poor = True if "POOR" in poorresp else False
	print "porttest.dns-oarc.net :", is_poor

	#Zone transfer
	print "Zone transfer Bilgisi"
	print "-------------------------"
	zoneresp = commands.getoutput("dig @" + nameserver1 + " " + domain + " AXFR")
	is_transferable = False if ("failed" in zoneresp) or ("error" in zoneresp) else True
	print "AXFR Transfer :", is_transferable

	#reverse zone

	hostip    = gethostbyname(domain)
	tershostip = hostip[::-1]
	rzoneresp = commands.getoutput("dig @" + nameserver1 + " " + tershostip + ".in-addr.arpa AXFR")
	is_rtransferable = False if ("failed" in rzoneresp) or ("error" in rzoneresp) else True
	print tershostip + ".in-addr.arpa AXFR :", is_rtransferable

	#bind surum
	print "Bind Bilgisi"
	print "-------------------------"
	bsurumresp = commands.getoutput("dig @" + nameserver1 + " version.bind txt chaos")
	bsurumpattern = re.compile(r'version.bind.\s+\d+\s+CH\s+TXT\s+"(.*?)"')
	bsurummatch = re.search(bsurumpattern, bsurumresp)
	bindsurum   = bsurummatch.group(1) if bsurummatch else "Bulamadim"
	print "bind version :", bindsurum

	#hostname
	print "Hostname Bilgisi"
	print "-------------------------"
	hnameresp = commands.getoutput("dig @" + nameserver1 + " hostname.bind txt chaos")
	hnamepattern = re.compile(r'hostname.bind.\s+\d+\s+CH\s+TXT\s+"(.*?)"')
	hnamematch  = re.search(hnamepattern, hnameresp)
	hname = hnamematch.group(1) if hnamematch else "Bulamadim"
	print "Hostname :", hname

	#txt bilgiler
	print "TXT Bilgisi"
	print "-------------------------"
	tresp = commands.getoutput("dig " + domain + " TXT")
	tpattern = re.compile(domain + '.\s+\d+\s+IN\s+TXT\s+"(.*?)=(.*?)"\n')
	tbul    = re.findall(tpattern, tresp)
	print "TXT records ", domain
	if tbul:
	    for k, v in tbul:
		print k, "=", v
	else:
	    print "Bulamadim"
	#WKS


	wresp = commands.getoutput("dig @" +nameserver1 + " " + domain + " WKS")
	wpattern = re.compile(domain + '\sIN\s+WKS\s+"(.*?)"\n')
	wbul = re.findall(wpattern, wresp)
	print "WKS for ", domain
	if wbul:
	    for w in wbul:
		print w
	else:
	    print "Bulamadim"      
	#HINFO
	print "Hinfo Bilgisi"
	print "-------------------------"
	hresp = commands.getoutput("dig @" +nameserver1 + " " + domain + " HINFO")
	hpattern = re.compile(domain + '\sIN\s+HINFO\s+(.*?)\n')
	hbul = re.findall(hpattern, hresp)
	print "HINFO for ", domain
	if hbul:
	    for h in hbul:
		print h
	else:
	    print "Bulamadim"


	print "Hinfo2 Bilgisi"
	print "-------------------------"
	h2resp = commands.getoutput("dig "+ domain + " HINFO")
	h2pattern = re.compile('\sIN\s+HINFO\s+(.*?)\n')
	h2bul = re.findall(h2pattern, h2resp)
	print "HINFO2 for ", domain
	if h2bul:
	    for h2 in h2bul:
		print h2
	else:
	    print "Bulamadim"

	print "SOA Bilgisi"
	print "-------------------------"
	hsresp = commands.getoutput("dig @" +nameserver1 + " " + domain + " SOA")
	hspattern = re.compile('\sIN\s+SOA\s+(.*?)\n')
	hsbul = re.findall(hspattern, hsresp)
	print "SOA for ", domain
	if hsbul:
	    for hs in hsbul:
		print hs
	else:
	    print "Bulamadim"

def main():
	if (sys.platform == 'linux-i386' or sys.platform == 'linux2' or sys.platform == 'darwin'):
		os.system("clear")
	else:
		print "yaşın kucuk bu yazilimi kullanamazsin"
		sys.exit(1)
	if len(sys.argv) != 2:
    		print "Kullanim : ./dnscache.py host.com"
    		sys.exit(1)
	else:
		print "#########################"
		print u"Dig Yardimcisi [@0x94 twitter]"
		print "#########################"
 		tumislem(sys.argv[1])

main()



