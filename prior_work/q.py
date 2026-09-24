import json,sys,urllib.request,urllib.parse
def q(t,query,p=1):
    u="https://www.deadseascrolls.org.il/api/search?"+urllib.parse.urlencode({'t':t,'q':query,'p':p})
    r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r,timeout=40))
if __name__=='__main__':
    for t,query in [('manuscript',"'Qumran'"),('manuscript',"composition_type_en:'Unidentified Texts'"),('manuscript',"'Unidentified'"),('image',"'Unidentified'")]:
        d=q(t,query); print(t,'|',query,'->',d['length'],'pages',d['totalpages'])
        if d['results']: print(json.dumps(d['results'][0],ensure_ascii=False)[:900])
        print('groups:',json.dumps(d.get('groups'),ensure_ascii=False)[:400]); print()
