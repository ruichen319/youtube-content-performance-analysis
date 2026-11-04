from html import escape
from pathlib import Path
import math

COLORS = ['#2563eb', '#db6b27', '#12826a', '#8b5cf6']

def text(x, y, value, size=14, anchor='start', color='#334155', weight='normal'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{escape(str(value))}</text>'

def frame(title, subtitle, height=540):
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="'+str(height)+'" viewBox="0 0 1100 '+str(height)+'">', '<rect width="1100" height="'+str(height)+'" fill="white"/>', text(36, 41, title, 23, weight='bold'), text(36, 69, subtitle, 13)]

def save(path, parts):
    Path(path).write_text(''.join(parts)+ '</svg>')

def line_panels(path, series, title, subtitle):
    # Independent y scales: these groups contain unequal numbers of eligible seasons.
    parts=frame(title, subtitle, 650)
    panels=list(series.items())
    for k,(name,values) in enumerate(panels):
        left=92; right=1060; top=125+k*235; bottom=top+160
        xmin,xmax=min(x for x,y in values),max(x for x,y in values)
        ymax=max(y for x,y in values) or 1
        def xx(v):return left+(v-xmin)/(xmax-xmin)*(right-left)
        def yy(v):return bottom-v/ymax*(bottom-top)
        parts.append(text(left,top-15,name,16,weight='bold'))
        for f in [0,.25,.5,.75,1]:
            y=bottom-f*(bottom-top)
            parts.append(f'<line x1="{left}" y1="{y}" x2="{right}" y2="{y}" stroke="#e2e8f0"/>')
            parts.append(text(left-12,y+4,f'{ymax*f:g}',12,'end'))
        parts.append(f'<line x1="{xx(0)}" y1="{top}" x2="{xx(0)}" y2="{bottom}" stroke="#64748b" stroke-dasharray="5 5"/>')
        for x in [-12,-8,-4,0,4,8,11]:
            parts.append(text(xx(x),bottom+22,x,12,'middle'))
        pts=' '.join(f'{xx(x):.1f},{yy(y):.1f}' for x,y in values)
        parts.append(f'<polyline points="{pts}" fill="none" stroke="{COLORS[k]}" stroke-width="3"/>')
        for x,y in values:parts.append(f'<circle cx="{xx(x):.1f}" cy="{yy(y):.1f}" r="3.2" fill="{COLORS[k]}"/>')
    parts.append(text(576,599,'Report week relative to first-batch launch (Week 0)',14,'middle'))
    parts.append(text(36,632,'Counts of listed event-season pairs; separate y scales. Chart absence does not mean zero viewing.',12))
    save(path,parts)

def bars(path, rows, title, subtitle, value_label='Value', percent=False):
    # rows = (label, value, color). Values share one zero-based linear scale.
    rows=list(rows); h=max(370,190+len(rows)*49)
    parts=frame(title,subtitle,h)
    left=360; right=1008; top=111
    maximum=max((v for _,v,_ in rows),default=1) or 1
    maximum*=1.16
    for f in [0,.25,.5,.75,1]:
        x=left+f*(right-left)
        parts.append(f'<line x1="{x}" y1="{top-8}" x2="{x}" y2="{top+len(rows)*49}" stroke="#e2e8f0"/>')
        v=maximum*f
        label=f'{v:.1%}' if percent else f'{v/1e6:.1f}M' if maximum>=1e6 else f'{v:,.1f}'
        parts.append(text(x,top+len(rows)*49+23,label,12,'middle'))
    for i,(label,value,color) in enumerate(rows):
        y=top+i*49
        parts.append(text(left-14,y+22,label,13,'end'))
        width=value/maximum*(right-left)
        parts.append(f'<rect x="{left}" y="{y}" width="{width:.1f}" height="31" rx="3" fill="{color}"/>')
        label=f'{value:.2%}' if percent else f'{value:,.1f}' if value<100 else f'{value:,.0f}'
        parts.append(text(left+width+8,y+22,label,12))
    parts.append(text((left+right)/2,top+len(rows)*49+49,value_label,13,'middle'))
    save(path,parts)
