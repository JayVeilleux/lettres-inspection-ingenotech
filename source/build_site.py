import base64,re
s=open('/home/claude/fosse/tool.src.html').read()
b=base64.b64encode(open('/home/claude/fosse/template.docx','rb').read()).decode()
s=s.replace('__TEMPLATE_B64__',b).replace('__FOOTER_B64__',base64.b64encode(open('/home/claude/fosse/footer_graphic.png','rb').read()).decode()).replace('__FOOTER_B64__',base64.b64encode(open('/home/claude/fosse/footer_graphic.png','rb').read()).decode())
i=s.index('</style>')+len('</style>')
head,body=s[:i],s[i:]
assert body.count('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js')==1
body=body.replace('https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js','./jszip.min.js').replace('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.2/jspdf.umd.min.js','./jspdf.umd.min.js')
assert 'cdnjs' not in body
sw="""<script>if('serviceWorker' in navigator){window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}))}</script>"""
out='''<!doctype html>
<html lang="fr-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b6aa8">
<link rel="manifest" href="./manifest.json">
<link rel="icon" href="./icon-192.png">
<link rel="apple-touch-icon" href="./apple-touch-icon.png">
<style>img{max-width:100%}</style>
'''+head+'\n</head>\n<body>\n'+body+'\n'+sw+'\n</body>\n</html>\n'
open('/home/claude/fosse/site/index.html','w').write(out)
