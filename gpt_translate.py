# coding=utf-8
from openai import OpenAI
import json
import os


os.environ["OPENAI_API_KEY"]='YOUR_KEY'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_facts(input_sentence_list, src="English", tgt="Japanese"):
    results = []

    for sent in input_sentence_list:
        prompt = f"Translate the following text from {src} into {tgt}: {sent}"
        print("prompt: ",prompt)
        response =client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            #stream=True
        )
        #print(response)
        chain_of_facts = response.choices[0].message.content #['message']['content']
        results.append(chain_of_facts.strip())
    return results

def generate_facts_cod(input_sentence_list,cods, src="English", tgt="Japanese"):
    results = []
    for sent,cod in zip(input_sentence_list,cods):
        dict_infor = ""
        #print(cod)
        for cd in cod:
            dict_infor+=" means ".join(cd[:])
            dict_infor+="\n"
        #print(dict_infor)
        dict_infor+="\n"
        prompt = f"{dict_infor}Translate the following text from {src} into {tgt}: {sent}"
        #print(f"cod prompt: {prompt}")
        response =client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            #stream=True
        )
        #print(response)
        chain_of_facts = response.choices[0].message.content #['message']['content']
        results.append(chain_of_facts.strip())
    #print(results)
    return results

def generate_facts_bicod(input_sentence_list,cods, src="English", tgt="Japanese"):
    results = []

    for sent,cod in zip(input_sentence_list,cods):
        dict_infor = ""
        #print(cod)
        for cd in cod:
            dict_infor+=" means ".join(cd[:2])
            dict_infor+="\n"
        #print(dict_infor)
        dict_infor+="\n"
        prompt = f"{dict_infor}Translate the following text from {src} into {tgt}: {sent}"
        #print(f"bi-cod prompt: {prompt}")
        response =client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            #stream=True
        )
        #print(response)
        chain_of_facts = response.choices[0].message.content #['message']['content']
        results.append(chain_of_facts.strip())
    #print(results)
    return results




source_sentences = ["sent1","sent2"]


### lang can be something like: Kikongo with Latin script,Kikongo with Latin script,...
languages = ["lang1","lang2","lang3"]
### abbr is the abbrevation of languages, can be something like: kon_Latn, ckb_Arab
abbr = ["abbr1","abbr2","abbr3"]

target_sentences_lang1 = ["sent1","sent2"]
target_sentences_lang2 = ["sent1","sent2"]
target_sentences_lang3 = ["sent1","sent2"]

total_target_sentences = [target_sentences_lang1, target_sentences_lang2, target_sentences_lang3]

#cod for language kon_Latn, for each sentence we have a two dimension list,[[],[],[],...] each item in the list is a keywords with its translaition in other languages.
#cods1 = [[["sent_1_word_1_original", "sent_1_word_1_trans1","sent_1_word_1_trans2",....],["sent_1_word_2_original", "sent_1_word_2_trans1","sent_1_word_2_trans2",...],...],[]]
cods1 = []
#cod for language ckb_Arab
cods2 = []

total_cods = [cods1, cods2]

total_res = []

total_target = []
for idx, (lang, xs) in enumerate(zip(languages,abbr)):
    print(idx, lang, xs)
    cur_res = []
    cod_res = generate_facts_cod(source_sentences,total_cods[idx], src="English", tgt=lang)
    bi_cod_res = generate_facts_bicod(source_sentences,total_cods[idx], src="English", tgt=lang)
    ori = generate_facts(source_sentences, src="English", tgt=lang)
    cur_res.append(cod_res)
    cur_res.append(bi_cod_res)
    cur_res.append(ori)
    print(cur_res)
    total_res.append(cur_res)
print(total_res)
