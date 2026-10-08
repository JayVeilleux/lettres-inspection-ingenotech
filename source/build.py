import base64
s=open('/home/claude/fosse/tool.src.html').read()
b=base64.b64encode(open('/home/claude/fosse/template.docx','rb').read()).decode()
open('/home/claude/fosse/tool.html','w').write(s.replace('__TEMPLATE_B64__',b))
