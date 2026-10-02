"""Validate durable per-frame records without starting a model or touching active output."""
from pathlib import Path
import sys,json,gzip,math,os,time,subprocess,csv
from validate import ROOT,EXP,MODELS,sha,now

def read(p):return json.loads(p.read_text())
def atomic(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);temp=p.with_name(p.name+f'.{os.getpid()}.tmp')
 with temp.open('w') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())
 os.replace(temp,p)
def active_processes():
 output=subprocess.check_output(['ps','-eo','pid,ppid,args'],text=True)
 result=[]
 for line in output.splitlines()[1:]:
  parts=line.strip().split(None,2)
  if len(parts)!=3:continue
  pid,ppid,args=parts
  if int(pid)==os.getpid():continue
  if str(EXP) in args or EXP.name+'/src/' in args:
   if ('python' in args and any('/'+n in args for n in ['benchmark.py','run_medium.py','repeat_clean_timing.py'])) and not args.startswith(('/bin/bash','bash ')):
    result.append({'pid':int(pid),'ppid':int(ppid),'args':args})
 return result

def audit(run,allow_quarantine=False):
 from pycocotools import mask as cm
 import yaml
 frozen=read(EXP/'manifests'/f'{run}_full_freeze.json');cfg=yaml.safe_load((EXP/'configs/benchmark.yaml').read_text())
 assert sha(EXP/'configs/benchmark.yaml')==frozen['config_sha256']
 assert sha(EXP/'EXPERIMENT_PROTOCOL.md')==frozen['protocol_sha256']
 assert all(sha(EXP/f)==h for f,h in frozen['sources'].items())
 checkpoints={r['filename']:r for r in read(EXP/'manifests/checkpoint_manifest.json')}
 images=read(EXP/'manifests/images.json');keys=[f"{r['sequence']}_{r['frame']:06d}" for r in images];expected=set(keys)
 live=active_processes();models=[];errors=[]
 for cp in MODELS:
  directory=EXP/'predictions'/run/'accuracy'/cp.removesuffix('.pt');pred=directory/'predictions'
  if not directory.exists():models.append({'model':cp,'completed_frames':0,'last_frame':None,'next_frame':keys[0],'status':'NOT_STARTED'});continue
  metadata=read(directory/'metadata.json')
  assert metadata['model']==cp and metadata['phase']=='accuracy' and metadata['frames']==keys
  assert metadata['config']==cfg and metadata['config_sha256']==frozen['config_sha256'] and metadata['protocol_sha256']==frozen['protocol_sha256']
  assert metadata['checkpoint_sha256']==sha(ROOT/'models'/cp)==checkpoints[cp]['sha256']
  snapshot=sorted(pred.glob('*.json.gz'));filenames=[f.name.removesuffix('.json.gz') for f in snapshot]
  assert len(set(filenames))==len(filenames) and set(filenames)<=expected
  assert filenames==keys[:len(filenames)],'Noncontiguous saved frame range'
  records=set();hashes={};corrupt=[]
  for idx,path in enumerate(snapshot):
   im=images[idx];key=keys[idx]
   try:
    with gzip.open(path,'rt') as stream:r=json.load(stream)
    assert r['model']==cp and r['input_shape']==[1,3,640,640]
    assert (r['sequence'],r['frame'])==(im['sequence'],im['frame'])
    assert (r['width'],r['height'])==(im['width'],im['height']) and r['post_nms_candidates']<1000
    assert key not in records;records.add(key)
    rles=[]
    for p in r['predictions']:
     assert p['class']==0 and math.isfinite(p['confidence']) and p['confidence']>.001
     assert all(math.isfinite(x) for x in p['bbox_xyxy']) and p['rle']['size']==[im['height'],im['width']]
     rles.append({'size':p['rle']['size'],'counts':p['rle']['counts'].encode('ascii')})
    if rles:
     areas=cm.area(rles);assert all(int(a)>0 and int(a)<=im['width']*im['height'] for a in areas)
    hashes[str(path.relative_to(EXP))]=sha(path)
   except BaseException as e:corrupt.append({'path':str(path.relative_to(EXP)),'error':repr(e),'index':idx})
  if corrupt:
   assert not live,'Never quarantine active output'
   assert allow_quarantine and len(corrupt)==1 and corrupt[0]['index']==len(snapshot)-1,'Only incomplete terminal record may be quarantined'
   path=EXP/corrupt[0]['path'];quarantine=directory/'quarantine'/f'{path.name}.incomplete-{int(time.time())}';quarantine.parent.mkdir(exist_ok=True);os.replace(path,quarantine)
   snapshot=snapshot[:-1];filenames=filenames[:-1]
  n=len(snapshot)
  aggregate=EXP/'metrics'/run/f'{cp}-aggregates.csv'
  metric_complete=False
  if aggregate.exists():
   rr=list(csv.DictReader(aggregate.open()));metric_complete=len(rr)==5 and any(r['sequence']=='ALL' and r['frames']=='2862' for r in rr)
  t=EXP/'timing'/run/'clean_repetition/summary.csv';timing_complete=False
  if t.exists():timing_complete=any(r['model']==cp and r['clean_rounds']=='3' and r['frames']=='300' for r in csv.DictReader(t.open()))
  models.append({'model':cp,'completed_frames':n,'last_frame':filenames[-1] if n else None,'next_frame':keys[n] if n<len(keys) else None,'metadata_status':metadata.get('status','RUNNING_OR_INTERRUPTED'),'metrics_complete':metric_complete,'timing_complete':timing_complete,'contiguous_order':'PASS','unique_ids':'PASS','readable_rle':'PASS','frozen_config_protocol_checkpoint':'PASS','atomic_frame_format':True,'temporary_files':[f.name for f in pred.glob('*.partial')],'quarantined_records':corrupt})
  atomic(EXP/'manifests'/f'{run}_{cp}_recovery_hashes.json',hashes)
 result={'timestamp':now(),'run_id':run,'status':'PASS','active_processes':live,'models':models,'policy':'Per-frame atomic gzip records are authoritative. Snapshot reflects start of inspection, active process may have advanced. No active outputs rewritten.'}
 return result
if __name__=='__main__':
 run=sys.argv[1];result=audit(run,allow_quarantine='--quarantine-terminal-corrupt' in sys.argv)
 atomic(EXP/'manifests'/f'{run}_RESUME_AUDIT.json',result)
 for r in result['models']:print('[MEDIUM RESUME]',r['model'],'saved:',r['completed_frames'],'last:',r['last_frame'],'metrics:',r.get('metrics_complete',False),'timing:',r.get('timing_complete',False))
 print('[MEDIUM RESUME] active existing processes:',len(result['active_processes']))
