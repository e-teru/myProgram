# -*- coding: utf-8 -*-
import re,json
import MeCab

http://www.ohsuga.is.uec.ac.jp/openrdf-sesame/repositories/DBpedia-ja?query=PREFIX+dbpedia-ja%3A+%3Chttp%3A%2F%2Fja.dbpedia.org%2Fresource%2F%3E+PREFIX+rdfs%3A%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E+SELECT+%3Fsake_name+WHERE+%7BGraph+%3Chttp%3A%2F%2Fwww.ohsuga.is.uec.ac.jp%2Fsake%3E%7B%3Fsake+a+%3Chttp%3A%2F%2Fja.dbpedia.org%2Fresource%2F%5Cu65E5%5Cu672C%5Cu9152%3E+%3Brdfs%3Alabel+%3Fsake_name+.+%7D%7D&Accept=application/sparql-results%2bjson

### Constants                                                                                                                                                     
MECAB_MODE = 'mecabrc'
PARSE_TEXT_ENCODING = 'utf-8'
pre_rdf  = "@prefix rdf:  	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>."
pre_rdfs = "@prefix rdfs: 	<http://www.w3.org/2000/01/rdf-schema#> . "
pre_ont  = "@prefix ont:  	<http://www.daml.org/2001/03/daml-ont#> ."
pre_sake_property = "@prefix sake_property: 	<http://www.ohsuga.is.uec.ac.jp/sake/property#> ."
pre_dbp = "@prefix dbp-ja: <http://ja.dbpedia.org/resource#> ."
pre_sake_bre = "@prefix sake_bre: 	<http://www.ohsuga.is.uec.ac.jp/sake/brewery#> ."
uri_subject_bre = "<http://www.ohsuga.is.uec.ac.jp/sake/brewery/"
uri_property = "<http://www.ohsuga.is.uec.ac.jp/sake/property/"
place1=''

def convert(output,min_id,max_id,path):
	f = open(path, 'r')
	jsonData = json.load(f)
	#print(json.dumps(jsonData,ensure_ascii=False, sort_keys = True, indent = 4))
	f.close()

	for i in range(min_id,max_id):
		sub1 = uri_subject_bre + str(i) + ">"
		pro_list = list(jsonData[str(i)])
		pro_list.sort()
		count = 0
		output1 = ''
		if jsonData[str(i)]['蔵元名'] == "狩場酒造場‎":
			continue
		if "不明" in jsonData[str(i)]['蔵元名']:
			continue
		for pro in pro_list:
			obj = jsonData[str(i)][str(pro)].replace(' ','').replace('＜掛米＞','').replace('＜麹米＞','').replace('(%)','').replace('　','').replace(' ','')
			if obj == "":
				continue
			if count == 0:
				output1 = sub1 + '>\t'
				output1 += uri_property + pro + '>\t'
				output1 += '\"' +obj + '\"'
				count += 1
			else:
				if pro == '蔵元名':
					output1 += '\t' + 'rdfs:label' + '\t'

					pat = re.compile(sub1)
					brewery = obj.replace('　','').replace(' ','').replace(' ','').replace('※','').replace('?','')+'_'+place1.replace('<http://ja.dbpedia.org/resource/','').replace('>','')
					output1 = pat.sub(uri_subject_bre+brewery,output1)
				else:
					output1 += '\t' + uri_property + pro + '>\t'
				output1 += '\"' + obj + '\"'
				
			
			if pro == pro_list[-1]:
				output1 += ' .\n'	
			else:
				output1 += ' ;\n'

			if pro == '住所':
				place1,place2,place3,place4 = parse(obj)
				place1_wiki = parse_wiki(place1)
				place2_wiki = parse_wiki(place2)
				place3_wiki = parse_wiki(place3)
				if(len(place1_wiki)==1):
					place1 = '<http://ja.dbpedia.org/resource/' + place1_wiki[0] + ">"
					output1 += '\t' + uri_property + 'place1>' + '\t' + place1 + ' ;\n'
				else:
					output1 += '\t' + uri_property + 'place1>' + '\t"' + place1 + '\" ;\n'
				if(len(place2_wiki)==1):
					place2 = '<http://ja.dbpedia.org/resource/' + place2_wiki[0] + ">"
					output1 += '\t' + uri_property + 'place2>' + '\t' + place2 + ' ;\n'
				else:
					output1 += '\t' + uri_property + 'place2>' + '\t"' + place2 + '\" ;\n'
				if(len(place3_wiki)==1):
					place3 = '<http://ja.dbpedia.org/resource/' + place3_wiki[0] + ">"
					output1 += '\t' + uri_property + 'place3>' + '\t' + place3 + ' ;\n'
				else:
					output1 += '\t' + uri_property + 'place3>' + '\t"' + place3 + '\" ;\n'
				
				
				if place4 != '':
					place4_wiki = parse_wiki(place4)
					if(len(place4_wiki)==1):
						place4 = '<http://ja.dbpedia.org/resource/' + place4_wiki[0] + ">"
						output1 += '\t' + uri_property + 'place4>' + '\t' + place4 + ';\n'
					else:
						output1 += '\t' + uri_property + 'place4>' + '\t"' + place4 + '";\n'
		output += output1

	return output

def parse(address):
	start = 0
	end = 6
	target = 0
	place3 = ''
	place4 = ''
	#print(address)
	place1,start,end = parse_place1(address,start,end)
	#print(place1)
	place2,start,end = parse_place2(address,start,end)
	#print(place2)
	if place2 == '':
		place2,start,end = parse_place3(address,start,end)
		place3 = address[start:len(address)]
	else:
		place3,start,end = parse_place3(address,start,end)
		if place3 == '':
			place3 = address[start:len(address)]
		else:
			place4 = address[start:len(address)]

	
	return place1,place2,place3,place4
	
def parse_place1(address,start,end):
	place1 = ""
	target = 0
	if address.find('府',start,end) != -1:
		target = address.find('府',start,end)+1
	elif address.find('道',start,end) != -1:
		target = address.find('道',start,end)+1
	elif address.find('県',start,end) != -1:
		target = address.find('県',start,end)+1
	elif address.find('都',start,end) != -1:
		target = address.find('都',start,end)+1

	place1 = address[start:target]
	end += (target-start) 
	start = target
	return place1,start,end

def parse_place2(address,start,end):
	place2 = ""
	target = 0
	if address.find('郡',start,end) != -1 and address.find('郡山',start,end) == -1:
		target = address.find('郡',start,end)+1
	elif address.find('市',start,end) != -1:
		target = address.find('市',start,end)+1
	elif address.find('村',start,end) != -1:
		target = address.find('村',start,end)+1
	elif address.find('島',start,end) != -1:
		target = address.find('島',start,end)+1
	elif address.find('町',start,end) != -1:
		target = address.find('町',start,end)+1

	else:
		return place2,start,end

	place2 = address[start:target]
	end += (target-start) 
	start = target
	return place2,start,end


def parse_place3(address,start,end):
	place3 = ""
	target = 0
	if address.find('市',start,end) != -1:
		target = address.find('市',start,end)+1
	elif address.find('区',start,end) != -1:
		target = address.find('区',start,end)+1
	elif address.find('町',start,end) != -1:
		target = address.find('町',start,end)+1
	elif address.find('村',start,end) != -1:
		target = address.find('村',start,end)+1
	else:
		return place3,start,end
	place3 = address[start:target]
	end += (target-start) 
	start = target
	return place3,start,end

def parse_wiki(text):
	_id = 0
	wiki_name = []
	tagger = MeCab.Tagger(MECAB_MODE)
	result = tagger.parse(text)
	result1 = result.split('\n')
	for r in result1:
		result2 = r.split(',')
		name_type = result2[0].split('\t')
		name = name_type[0]
		
		if len(name_type) >1:
			type = name_type[1]
		if result2[len(result2)-1] == 'wikipedia':
			#print(name+"：" +type+"：" + result2[len(result2)-1])
			if name not in wiki_name:
				wiki_name.insert(_id,name)
				_id += 1
	return wiki_name

def write(output):
	#書き込み
	#wf = open('../../sake_data/n3/enoteka_wine_red.n3', 'w') # 書き込みモードで開く
	wf = open('../../sake_data/n3/sake_bre.n3', 'w') # 書き込みモードで開く
	wf.write(output) # 引数の文字列をファイルに書き込む
	wf.close() # ファイルを閉じる

if __name__ == "__main__":
	output = pre_rdf+"\n"+pre_rdfs+"\n"+pre_ont+"\n"+pre_sake_property+"\n"+pre_dbp+"\n"+pre_sake_bre+"\n\n"
	output = convert(output,1,1938,'../../sake_data/json/sake_sen_bre.json')
	write(output)
	#convert('../../sake_data/json/enoteka_wine_red2.json')
