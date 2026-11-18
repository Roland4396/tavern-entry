"""Render only the two private origins. All other hosts/auth/SSE rules remain byte-for-byte."""
from pathlib import Path
import argparse
LAYOUT=Path(__file__).parent
ANCHOR='    resolver 127.0.0.11 valid=30s ipv6=off;\n'
TARGETS=(
 ('proxy_pass http://sillytavern:28000;', 'proxy_pass http://tavern_app_origin;',5),
 ('set $private_absolute_backend http://sillytavern:28000;', 'set $private_absolute_backend http://tavern_app_origin;',1),
 ('proxy_pass http://auth-gateway:28100','proxy_pass http://tavern_login_origin',4),
)
def render(text, *, revert=False):
    block=ANCHOR+'\n'+(LAYOUT/'origins.conf').read_text()
    old,new=(block,ANCHOR) if revert else (ANCHOR,block)
    if text.count(old)!=1 or (not revert and ('tavern_app_origin' in text or 'tavern_login_origin' in text)):
        raise ValueError('unexpected nginx origin definitions')
    out=text.replace(old,new)
    # Refuse to change other virtual hosts, mixed configurations or unreviewed references.
    start=out.index('        server_name tavern.example.invalid;')
    end=out.index('\n    }',start)
    body=out[start:end];other=out[:start]+out[end:]
    for a,b,n in TARGETS:
        if revert:a,b=b,a
        if body.count(a)!=n or a in other or b in body:raise ValueError('unexpected virtual-host targets: '+a)
        body=body.replace(a,b)
    return out[:start]+body+out[end:]
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('dest',type=Path);p.add_argument('--revert',action='store_true');a=p.parse_args()
    if a.dest.exists():p.error('destination must be a new candidate file')
    a.dest.write_text(render(a.source.read_text(),revert=a.revert))
