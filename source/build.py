import base64,os
HERE=os.path.dirname(os.path.abspath(__file__))
def p(*a): return os.path.join(HERE,*a)
s=open(p('tool.src.html'),encoding='utf-8').read()
b=base64.b64encode(open(p('template.docx'),'rb').read()).decode()
footer_b64=base64.b64encode(open(p('footer_graphic.png'),'rb').read()).decode()
out_path=p('tool.html')
open(out_path,'w',encoding='utf-8').write(s.replace('__TEMPLATE_B64__',b).replace('__FOOTER_B64__',footer_b64))
print('wrote', out_path)
