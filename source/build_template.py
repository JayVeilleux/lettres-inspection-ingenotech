import re, os, shutil, zipfile
SP='/tmp/claude-0/-home-claude/1c7ad499-dfba-5774-ac52-aaa9ee66d7aa/scratchpad'
src=SP+'/un'
dst='/home/claude/fosse/tpl'
shutil.rmtree(dst,ignore_errors=True); shutil.copytree(src,dst)
x=open(dst+'/word/document.xml',encoding='utf8').read()
b0=x.index('<w:body>')+8; b1=x.index('</w:body>')
head,body,tail=x[:b0],x[b0:b1],x[b1:]
els=open(SP+'/els.txt',encoding='utf8').read().split('\n=====\n')
assert ''.join(els)==body, 'split mismatch'
E=[e.replace('<w:highlight w:val="yellow"/>','') for e in els]

def one_run(p,text):
    ppr=re.search(r'<w:pPr>.*?</w:pPr>',p).group(0)
    rpr=re.search(r'<w:r[ >](?:(?!</w:r>).)*?(<w:rPr>.*?</w:rPr>)',p,re.S).group(1)
    ptag=re.match(r'<w:p[^>]*>',p).group(0)
    parts=text.split('\t'); runs=''
    for i,t in enumerate(parts):
        if i>0: runs+='<w:r>'+rpr+'<w:tab/></w:r>'
        if t: runs+='<w:r>'+rpr+'<w:t xml:space="preserve">'+t+'</w:t></w:r>'
    return ptag+ppr+runs+'</w:p>'
def rep(p,old,new):
    assert p.count('>'+old+'<')==1, (old,p.count('>'+old+'<'))
    return p.replace('>'+old+'<','>'+new+'<')
def IF(name,*xs): return '<!--IF:%s-->'%name+''.join(xs)+'<!--ENDIF:%s-->'%name
blank=E[18]
for k in [25,31,41,44,47,52]:
    assert '<w:pStyle' not in E[k][:E[k].index('</w:pPr>')]
    E[k]=E[k].replace('<w:pPr>','<w:pPr><w:pStyle w:val="NormalWeb"/>',1)

E[0]=one_run(E[0],'Sherbrooke, le {{DATE_LETTRE}}')
E[3]=one_run(E[3],'{{DEST1}}')
dest2=one_run(E[3],'{{DEST2}}')
E[4]=one_run(E[4],'{{ADRESSE}}')
E[5]=one_run(E[5],'{{VILLE}} ({{PROVINCE}})  {{CP}}')
E[9]=one_run(E[9],'\t{{ADRESSE_TRAVAUX}}, {{VILLE_TRAVAUX}} (Qc)')
E[10]=one_run(E[10],'\tLot : {{LOT}} du Cadastre du Québec')
E[11]=one_run(E[11],'\tN/réf. : {{NREF}}')
p=E[13]
p=rep(p,'La présente fait suite aux travaux d’expertise réalisés les ','La présente fait suite aux travaux d’expertise réalisés ')
p=rep(p,'28 et 30 octobre 2024 par M. Philippe Drouin','{{DATES_EXPERTISE}} par {{TECHNICIEN}}')
E[13]=p
p=E[16]
p=rep(p,'une (1)','{{CHAMBRES}}')
p=rep(p,' chambre à coucher. Celle-ci se compose d’une fosse septique ',' à coucher. Celle-ci se compose d’une fosse septique ')
p=rep(p,'en béton','{{FOSSE_MAT}}')
p=rep(p,' présentant une capacité potentielle d’environ ',' présentant une capacité potentielle ')
p=rep(p,'3,4 m³','{{CAPACITE}}')
p=rep(p,'modifié.','{{EPURATEUR}}.')
p=rep(p,'relié','{{ANNEE}}')
p=p.replace('<w:t xml:space="preserve"> à l’année 1987.  / inconnu.</w:t>','<w:t></w:t>')
assert '1987' not in p
E[16]=p
E[95]=rep(E[95],'Annexe VI – Attestation de bon fonctionnement des installations septiques d’une résidence isolée','{{PJ_FORM}}')
E[37]=re.sub(r'<w:ind w:left="720"/>','',E[37],count=1)
# Conclusion headings -> "Conclusion"
h=rep(E[54],' fonctionnelle et non polluante','')
E[61]=rep(E[61],'Veuillez agréer nos salutations distinguées','Veuillez agréer nos salutations distinguées.')

# footer field cached result
f2=open(dst+'/word/footer2.xml',encoding='utf8').read()
m=re.findall(r'<w:t[^>]*>([^<]*)</w:t>',f2); print('footer texts',m)
f2=re.sub(r'(<w:t[^>]*>)ING-BON[^<]*(</w:t>)',r'\g<1>{{FICHIER}}\2',f2)
# ensure fields merged into one run
assert '{{FICHIER}}' in f2, 'footer token'
# remove other pieces of result text between separate and end if split
open(dst+'/word/footer2.xml','w',encoding='utf8').write(f2)

out=[]
out+= [E[0],E[1],E[2],E[3],IF('DEST2',dest2),E[4],E[5],E[6],E[7],E[8],E[9],E[10],E[11],blank]
out+= [E[13],E[14],E[16],E[17]]
out+= [IF('PLOMB_BON',E[21]),IF('PLOMB_MAUV',E[25])]
out+= [IF('NIV_BON',E[28]),IF('NIV_MAUV',E[31])]
out+= [E[32],IF('FLUO_FAIT',E[33]),IF('SAT_FAIT',E[34]),IF('FUM_FAIT',E[35])]
out+= [IF('ESSAIS_BONS',E[37],E[38]),IF('FLUO_MAUV',E[41]),IF('FUM_MAUV',E[44]),IF('SAT_MAUV',E[47])]
out+= [IF('DIST_BON',E[50]),IF('DIST_MAUV',E[52])]
out+= [E[53]]
out+= [IF('CONC_POS',h,E[55],E[56],IF('DIST_BON2',E[57]),E[58],E[59],E[60],E[61])]
out+= [IF('CONC_NEG',h,E[65],E[66],E[67],E[68],E[69],E[70],E[71])]
out+= E[72:89]
out+= [IF('PHOTOS1',E[89],'{{PHOTOS1}}'),E[91],E[92],'{{PHOTOS2}}',E[94],E[95],E[96]]
body2=''.join(out)
doc=head+body2+tail
open(dst+'/word/document.xml','w',encoding='utf8').write(doc)
# drop sample photos
rels=open(dst+'/word/_rels/document.xml.rels',encoding='utf8').read()
for rid in ['rId9','rId10','rId11','rId12','rId19','rId20','rId21','rId22']:
    mm=re.search(r'<Relationship Id="%s" [^>]*Target="([^"]+)"/>'%rid,rels)
    os.remove(dst+'/word/'+mm.group(1)); rels=rels.replace(mm.group(0),'')
    assert 'r:embed="%s"'%rid not in doc
open(dst+'/word/_rels/document.xml.rels','w',encoding='utf8').write(rels)
ct=open(dst+'/[Content_Types].xml',encoding='utf8').read(); print(re.findall(r'<Default [^>]*>',ct))
z=zipfile.ZipFile('/home/claude/fosse/template.docx','w',zipfile.ZIP_DEFLATED)
for r,d,fs in os.walk(dst):
    for f in fs:
        fp=os.path.join(r,f); z.write(fp,os.path.relpath(fp,dst))
z.close(); print(os.path.getsize('/home/claude/fosse/template.docx'))
