import base64
s=open('tool.src.html').read()
b=base64.b64encode(open('template.docx','rb').read()).decode()
open('tool.html','w').write(s.replace('__TEMPLATE_B64__',b).replace('__FOOTER_B64__',base64.b64encode(open('footer_graphic.png','rb').read()).decode()))
