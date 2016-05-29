# -*- coding: utf-8 -*-
import re,json
import MeCab

### Constants                                                                                                                                                     
MECAB_MODE = 'mecabrc'
PARSE_TEXT_ENCODING = 'utf-8'
pre_rdf  = "@prefix rdf:  	<http://www.w3.org/1999/02/22-rdf-syntax-ns#>."
pre_rdfs = "@prefix rdfs: 	<http://www.w3.org/2000/01/rdf-schema#> . "
pre_ont  = "@prefix ont:  	<http://www.daml.org/2001/03/daml-ont#> ."
pre_sake = "@prefix sake: 	<http://www.ohsuga.is.uec.ac.jp/sake#> ."
pre_sake_property = "@prefix sake_property: 	<http://www.ohsuga.is.uec.ac.jp/sake/property#> ."
pre_sake_bre = "@prefix sake_bre: 	<http://www.ohsuga.is.uec.ac.jp/sake/brewery#> ."
pre_dbp = "@prefix dbpedia-ja: <http://ja.dbpedia.org/resource#> ."
uri_subject  = "<http://www.ohsuga.is.uec.ac.jp/sake/"
uri_subject_bre  = "<http://www.ohsuga.is.uec.ac.jp/sake/brewery/"
uri_property = "<http://www.ohsuga.is.uec.ac.jp/sake/property/"
sake_bre_list = []

def convert(output,min_id,max_id,path):
	f = open(path, 'r')
	jsonData = json.load(f)
	#print(json.dumps(jsonData,ensure_ascii=False, sort_keys = True, indent = 4))
	f.close()

	for i in range(min_id,max_id):
		sub1 = uri_subject + str(i)
		pro_list = list(jsonData[str(i)])
		pro_list.sort()
		count = 0
		output1 = ''
		sub1 = uri_subject +jsonData[str(i)]['名前'].replace('　','').replace(' ','').replace('%','').replace(' ','').replace('∴','').replace('(','').replace(')','') +">"
		output1 = sub1 + '\t'
		output1 += "a" + '\t'
		output1 += '<http://ja.dbpedia.org/resource/日本酒>  ;\n'
		count += 1
		for pro in pro_list:
			obj = jsonData[str(i)][str(pro)].replace(' ','').replace('＜掛米＞','').replace('＜麹米＞','').replace('(%)','').replace('(','').replace(')','')
			if obj == "":
				continue
			if count == 0:
				sub1 = uri_subject +jsonData[str(i)]['名前'].replace('　','').replace(' ','').replace('%','').replace(' ','').replace('∴','').replace('(','').replace(')','')
				output1 = sub1 + '\t'
				output1 += uri_property + pro + '>\t'
				output1 += '\"' +obj + '\"'
				count += 1
			else:
				if pro =='名前':
					output1 += '\t' + 'rdfs:label' + '\t' 
					output1 += '\"' + obj + '\"@ja'
				#	pat = re.compile(sub1)
				#	output1 = pat.sub(uri_subject+obj.replace('　','').replace(' ','').replace('%','').replace(' ','').replace('∴',''),output1)
				else:
					output1 += '\t' + uri_property + pro + '>\t'
					if pro =='蔵元':
						if obj in sake_bre_list:
							output1 += uri_subject_bre+obj+'_'+jsonData[str(i)]['都道府県']+">"
						else:
							output1 += '\"\"'
					elif pro =='都道府県':
						output1 += '<http://ja.dbpedia.org/resource/'+obj+">"
					else:
						output1 += '\"' + obj + '\"'
			
			#if pro == pro_list[-1]:
			#	output1 += ' . \n'	
			#else:
			#	output1 += ' ; \n'
			output1 += ' ; \n'
		a = output1.rfind(';')
		output2 = list(output1)
		output2[a] ='.'
		output1 = "".join(output2)
		
		output += output1

	return output

def make_list_bre(min_id,max_id,path):
	f = open(path, 'r')
	jsonData = json.load(f)
	f.close()
	for i in range(min_id,max_id):
		pro_list = list(jsonData[str(i)])
		for pro in pro_list:
			obj = jsonData[str(i)][str(pro)]
			if pro == '蔵元名':
				brewery = obj.replace('　','').replace(' ','')
				sake_bre_list.append(brewery)
	print('酒造リスト作成完了')
	return sake_bre_list


def write(output):
	#書き込み
	#wf = open('../../sake_data/n3/enoteka_wine_red.n3', 'w') # 書き込みモードで開く
	wf = open('../../sake_data/n3/sake.n3', 'w') # 書き込みモードで開く
	wf.write(output) # 引数の文字列をファイルに書き込む
	wf.close() # ファイルを閉じる

if __name__ == "__main__":
	output = pre_rdf+"\n"+pre_rdfs+"\n"+pre_ont+"\n"+pre_sake+"\n"+pre_sake_property+"\n"+pre_dbp+"\n"+pre_sake_bre+"\n\n"
	#output = convert(output,1,1938,'../../sake_data/json/sake_sen_bre.json')
	make_list_bre(1,1938,'../../sake_data/json/sake_sen_bre.json')
	output = convert(output,1,678,'../../sake_data/json/sake_sen.json')
	write(output)
	#convert('../../sake_data/json/enoteka_wine_red2.json')