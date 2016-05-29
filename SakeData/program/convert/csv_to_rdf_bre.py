# -*- coding: utf-8 -*-

count = 0
pre_rdf  = "@prefix rdf:  	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>."
pre_rdfs = "@prefix rdfs: 	<http://www.w3.org/2000/01/rdf-schema#> . "
pre_ont  = "@prefix ont:  	<http://www.daml.org/2001/03/daml-ont#> ."
pre_sake_bre = "@prefix sake_bre: 	<http://www.ohsuga.is.uec.ac.jp/sake/bre#> ."
pre_sake_property = "@prefix sake_property: 	<http://www.ohsuga.is.uec.ac.jp/sake/property#> ."
str = pre_rdf+"\n"+pre_rdfs+"\n"+pre_ont+"\n"+pre_sake_bre+"\n" +pre_sake_property+"\n"
property={}
ohsuga_domain = "http://www.ohsuga.is.uec.ac.jp"
uri_subject   = "sake_bre"
uri_property  = "sake_property"
f = open('../../sake_data/csv/sake_sen_bre.csv', 'r')
for line in f:
	line = line.strip()
	items = line.split(',')
	if count==0:
		for i in range(0,len(items)):
			if items[i].replace('"','')=='蔵元名':
				property[i]='http://www.w3.org/2000/01/rdf-schema#label'
			else:
				property[i]=uri_property+items[i].replace('"','')
		count+= 1
	else:
		str += uri_subject+items[0].replace('"','')+"\t"
		str += property[1]+"\t"
		str += items[1] +" ; \n"
		for i in range(2,len(items)):
			str += "\t"
			str += property[i]+"\t"
			if i == len(items)-1:
				str += items[i] + " . \n"
			else:	
				str += items[i] + " ; \n"
f.close()

#書き込み
wf = open('../../sake_data/n3/sake_bre.n3', 'w') # 書き込みモードで開く
wf.write(str) # 引数の文字列をファイルに書き込む
wf.close() # ファイルを閉じる