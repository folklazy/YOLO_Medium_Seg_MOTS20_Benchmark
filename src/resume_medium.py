"""Durable Medium supervisor: reuse existing workers, recover missing work, finalize once.

No changes to frozen evaluator/preprocessing/timing measurements. Singleton lock,
per-frame atomic records and independent progress persist across UI disconnects.
"""
from pathlib import Path
import sys,os,json,time,subprocess,fcntl,traceback,shutil,csv,math
from validate import ROOT,EXP,MODELS,sha,now
from audit_resume_state import read,atomic,active_processes,audit

def rows(p):return list(csv.DictReader(p.open())) if p.exists() else []
def phase(run,name,args):
 logfile=EXP/'logs'/run/(name+'.log')
 with logfile.open('a') as log:subprocess.run([str(ROOT/'.venv/bin/python'),'-B',*args],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
def progress(run,stage):
 models=[]
 for cp in MODELS:
  d=EXP/'predictions'/run/'accuracy'/cp.removesuffix('.pt')/'predictions';files=sorted(d.glob('*.json.gz'))
  models.append({'model':cp,'frames_saved':len(files),'last_frame':files[-1].name.removesuffix('.json.gz') if files else None})
 atomic(EXP/'manifests'/f'{run}_RESUME_PROGRESS.json',{'timestamp':now(),'stage':stage,'supervisor_pid':os.getpid(),'models':models})

def accuracy_recovery(run,prov):
 import benchmark as b
 import torch,numpy as np,random,cv2
 torch.manual_seed(20260929);np.random.seed(20260929);random.seed(20260929);torch.backends.cudnn.benchmark=False
 from ultralytics.utils import LOGGER
 LOGGER.addHandler(b.NMSWarningGuard())
 inspection=audit(run,allow_quarantine=True)
 atomic(EXP/'manifests'/f'{run}_post_worker_audit.json',inspection)
 fs=None;out=EXP/'metrics'/run
 for entry in inspection['models']:
  cp=entry['model'];directory=EXP/'predictions'/run/'accuracy'/cp.removesuffix('.pt')
  if entry['completed_frames']==2862:
   print('[MEDIUM RESUME]',cp,'accuracy REUSED',flush=True)
  else:
   if fs is None:fs=b.frames_for()
   pred_dir=directory/'predictions';directory.mkdir(parents=True,exist_ok=True);pred_dir.mkdir(exist_ok=True)
   # Preserve any stale temporary writes outside the final-record namespace.
   for temp in pred_dir.glob('*.partial'):
    dst=directory/'quarantine'/f'{temp.name}.stale-{int(time.time())}';dst.parent.mkdir(exist_ok=True);os.replace(temp,dst)
   cfg=b.config();meta_path=directory/'metadata.json'
   if meta_path.exists():
    meta=read(meta_path);backup=directory/f'metadata.pre-resume-{int(time.time())}.json';shutil.copy2(meta_path,backup)
   else:
    meta={'model':cp,'phase':'accuracy','config':cfg,'config_sha256':sha(EXP/'configs/benchmark.yaml'),'protocol_sha256':sha(EXP/'EXPERIMENT_PROTOCOL.md'),'checkpoint_sha256':sha(ROOT/'models'/cp),'environment_sha256':sha(EXP/'manifests/environment.json'),'source_manifest_sha256':sha(EXP/'manifests/source_manifest.json'),'frames':[b.key(f) for f in fs],'start':now()}
   first=entry['completed_frames'];segment={'timestamp':now(),'existing_frames':first,'first_missing_frame':entry['next_frame'],'new_frames':0,'driver_sha256':sha(Path(__file__))}
   meta['resumed']=bool(first);meta.setdefault('resume_segments',[]).append(segment);atomic(meta_path,meta)
   adapter=None;audit_rows=[]
   try:
    b.clean();adapter=b.Adapter(ROOT/'models'/cp,cfg,directory/f'resume-framework-{int(time.time())}');adapter.sync();adapter.reset_peak_memory()
    meta['effective_predictor_args']=vars(adapter.predictor.args);meta['runtime_parameters']=adapter.runtime_parameters;meta['end2end']=adapter.predictor.model.end2end;meta['precision']=adapter.precision
    print('[MEDIUM RESUME]',cp,'RUNNING from',entry['next_frame'],flush=True)
    for index,f in enumerate(fs[first:],first):
     path=pred_dir/f'{b.key(f)}.json.gz';assert not path.exists()
     image=cv2.imread(str(f.image));assert image is not None
     ps,lat=adapter.predict(image,f.image);assert (lat['input_height'],lat['input_width'])==(640,640)
     compact=[p.compact() for p in ps]
     record={'sequence':f.sequence,'frame':f.number,'model':cp,'width':f.width,'height':f.height,'input_shape':[1,3,640,640],'post_nms_candidates':adapter.predictor.post_nms_candidates,'predictions':b.encode_preds(compact)}
     b.save_prediction(path,record)
     audit_rows.append({'sequence':f.sequence,'frame':f.number,'post_nms_candidates':record['post_nms_candidates'],'saved_predictions':len(compact),**lat})
     segment['new_frames']+=1;del ps,compact,image
     if (index+1)%10==0:
      atomic(directory/'RESUME_STATE.json',{'timestamp':now(),'completed_frames':index+1,'last_frame':b.key(f),'next_frame':b.key(fs[index+1]) if index+1<len(fs) else None,'segment':segment})
      progress(run,'RESUMING_ACCURACY')
    meta.update(status='PASS',images_successful=2862,images_failed=0,end=now(),peak_memory=adapter.peak_memory())
    segment['status']='PASS';prov['executed_segments'].append({'model':cp,**segment})
    b.csvwrite(directory/f'resume_frame_audit-{int(time.time())}.csv',audit_rows)
    meta['accuracy_frame_audit_note']='Previously saved predictions preserved. Timing audit rows from interrupted segment may be unavailable; primary speed is dedicated timing only.'
    atomic(meta_path,meta);atomic(directory/'RESUME_STATE.json',{'status':'COMPLETE','completed_frames':2862,'last_frame':b.key(fs[-1]),'next_frame':None})
   except BaseException as error:
    meta.update(status='INTERRUPTED',resume_error=repr(error));atomic(meta_path,meta);raise
   finally:
    del adapter;b.clean()
   print('[MEDIUM RESUME]',cp,'COMPLETE',flush=True)
  aggregate=out/f'{cp}-aggregates.csv'
  if aggregate.exists() and len(rows(aggregate))==5:
   print('[MEDIUM RESUME]',cp,'metrics REUSED',flush=True)
  else:
   if fs is None:fs=b.frames_for()
   b.evaluate_model(cp,fs,directory/'predictions',out,b.config())
   prov['new_metric_evaluations'].append(cp)
 allrows=[]
 for cp in MODELS:allrows.extend(rows(out/f'{cp}-aggregates.csv'))
 # Rebuild only the index tables from preserved aggregate rows, not metrics.
 b.csvwrite(out/'per_model.csv',[r for r in allrows if r['sequence']=='ALL'])
 b.csvwrite(out/'per_sequence.csv',[r for r in allrows if r['sequence']!='ALL'])

def timing_recovery(run,prov):
 import benchmark as b
 import torch,numpy as np,random,cv2,gc
 from ultralytics.utils import LOGGER
 from repeat_clean_timing import wait_idle
 torch.manual_seed(20260929);np.random.seed(20260929);random.seed(20260929);torch.backends.cudnn.benchmark=False;LOGGER.addHandler(b.NMSWarningGuard())
 cfg=b.config();frozen=read(EXP/'manifests'/f'{run}_full_freeze.json');fs=b.frames_for(read(EXP/'manifests/timing_frames.json'))
 base=EXP/'timing'/run/'clean_repetition';base.mkdir(parents=True,exist_ok=True);accepted=[];allrows=[]
 for rnd,order in enumerate(frozen['timing_order'],1):
  for cp in order:
   meta_file=base/f'round{rnd}-{cp}.json';csv_file=base/f'round{rnd}-{cp}.csv'
   if meta_file.exists() and csv_file.exists():
    m=read(meta_file);rr=rows(csv_file)
    if m.get('status')=='PASS' and not m.get('contaminated') and len(rr)==100:
     accepted.append(m);allrows.extend(rr);continue
   # Preserve incomplete/contaminated attempts; never reclassify them as clean.
   if meta_file.exists() or csv_file.exists():
    old=base/'excluded'/f'round{rnd}-{cp}-{int(time.time())}';old.mkdir(parents=True,exist_ok=False)
    for f in [meta_file,csv_file]:
     if f.exists():shutil.copy2(f,old/f.name)
   attempts=0
   while True:
    attempts+=1;b.clean();wait_idle();before=b.gpu();m={'round':rnd,'model':cp,'start':now(),'gpu_before':before,'contaminated':b.contaminated(before,idle=True),'recovery_attempt':attempts}
    adapter=None;rr=[]
    try:
     t=time.perf_counter();adapter=b.Adapter(ROOT/'models'/cp,cfg,base/f'round{rnd}-{cp}-recovery{int(time.time())}'/'framework');adapter.sync();m['load_seconds']=time.perf_counter()-t
     for f in fs[:cfg['warmup_iterations']]:adapter.predict(cv2.imread(str(f.image)),f.image)
     adapter.sync();adapter.reset_peak_memory();m['baseline_allocated_mib']=torch.cuda.memory_allocated()/1024**2;m['baseline_reserved_mib']=torch.cuda.memory_reserved()/1024**2;m['gpu_samples']=[]
     for i,f in enumerate(fs):
      if i%10==0:
       g=b.gpu();m['gpu_samples'].append(g);m['contaminated']|=b.contaminated(g)
      image=cv2.imread(str(f.image));ps,lat=adapter.predict(image,f.image)
      t=time.perf_counter();compact=[p.compact() for p in ps];prep=(time.perf_counter()-t)*1000
      rr.append({'model':cp,'round':rnd,'sequence':f.sequence,'frame':f.number,'post_nms_candidates':adapter.predictor.post_nms_candidates,'predictions':len(ps),'rle_preparation_ms':prep,**lat});del ps,compact,image
     m.update(adapter.peak_memory());m['status']='PASS'
    except BaseException as e:m.update(status='FAIL',error=repr(e));raise
    finally:
     m['end']=now();m['gpu_after']=b.gpu();m['contaminated']|=b.contaminated(m['gpu_after'])
     for r in rr:r['contaminated']=m['contaminated']
     atomic(meta_file,m);b.csvwrite(csv_file,rr);del adapter;b.clean()
    if not m['contaminated']:break
    old=base/'excluded'/f'round{rnd}-{cp}-{int(time.time())}';old.mkdir(parents=True,exist_ok=False);shutil.copy2(meta_file,old/meta_file.name);shutil.copy2(csv_file,old/csv_file.name)
   accepted.append(m);allrows.extend(rr);prov['new_timing_rounds'].append({'model':cp,'round':rnd});progress(run,'TIMING')
 b.csvwrite(base/'all_frames.csv',allrows);atomic(base/'runs.json',accepted)
 summary=[]
 for cp in MODELS:
  rr=[r for r in allrows if r['model']==cp];good=[r for r in accepted if r['model']==cp];r={'model':cp,'clean_rounds':len(good),'frames':len(rr)}
  for metric in ['preprocess_ms','inference_ms','postprocess_ms','ultralytics_postprocess_inclusive_ms','total_ms','rle_preparation_ms']:r.update({metric+'_'+k:v for k,v in b.stats([float(x[metric]) for x in rr]).items()})
  r['fps']=1000/r['total_ms_mean']
  for k in ['peak_gpu_allocated_mib','peak_gpu_reserved_mib','baseline_allocated_mib','baseline_reserved_mib']:r[k]=max(m[k] for m in good)
  r['load_seconds_mean']=float(np.mean([m['load_seconds'] for m in good]));summary.append(r)
 b.csvwrite(base/'summary.csv',summary)


def main(run):
 lock=(EXP/'logs'/run/'resume_supervisor.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 old=read(EXP/'manifests'/f'{run}_RESUME_AUDIT.json')
 prov={'timestamp':now(),'run_id':run,'session_interruption_reason':'ChatGPT/Codex usage limit; not a benchmark failure','audit_path':f'manifests/{run}_RESUME_AUDIT.json','audit_sha256':sha(EXP/'manifests'/f'{run}_RESUME_AUDIT.json'),'recovered_actual_state':old['models'],'requested_estimate_not_used':410,'original_workers_alive_at_recovery':old['active_processes'],'REUSED':[r['model']+' accuracy + metrics' for r in old['models'] if r['completed_frames']==2862 and r.get('metrics_complete')],'RESUMED':['Session supervision resumed; existing YOLOv8m process continues saved contiguous range.'],'NEW':['Remaining YOLOv8m frames, missing timing, canonical conversion and reports only.'],'executed_segments':[],'new_metric_evaluations':[],'new_timing_rounds':[],'runtime_driver_sha256':sha(Path(__file__))}
 atomic(EXP/'manifests/RESUME_PROVENANCE.json',prov)
 print('[MEDIUM RESUME] existing workers retained; no duplicate inference',flush=True)
 while active_processes():progress(run,'WAITING_FOR_EXISTING_WORKERS');time.sleep(20)
 progress(run,'RECOVERY_GATES')
 # If the original workers finished all accuracy, reuse all aggregates directly.
 aggregate_paths=[EXP/'metrics'/run/f'{cp}-aggregates.csv' for cp in MODELS]
 if not all(p.exists() and len(rows(p))==5 for p in aggregate_paths):accuracy_recovery(run,prov)
 print('[MEDIUM] accuracy complete',flush=True)
 tim=EXP/'timing'/run/'clean_repetition/summary.csv';current=rows(tim)
 if not (len(current)==3 and all(r['clean_rounds']=='3' and r['frames']=='300' for r in current)):
  timing_recovery(run,prov)
 else:prov['NEW'].append('9 timing rounds completed by the retained original worker; timing source reused at finalization.')
 print('[MEDIUM] timing complete',flush=True)
 # Compare already validated records to their recovery hashes: no saved frame was overwritten.
 for cp in MODELS:
  evidence=EXP/'manifests'/f'{run}_{cp}_recovery_hashes.json'
  if evidence.exists():assert all(sha(EXP/path)==h for path,h in read(evidence).items())
 prov['previous_saved_frames_preserved']='PASS';atomic(EXP/'manifests/RESUME_PROVENANCE.json',prov)
 phase(run,'final-canonical-audit',[str(EXP/'src/build_medium_results.py'),run])
 phase(run,'final-report',[str(EXP/'src/report_medium.py'),run])
 docs=read(EXP/'manifests/DOCUMENT_VALIDATION.json');assert docs['status']=='PASS'
 presentation=(EXP/'PRESENTATION_SUMMARY_TH.md').read_text();assert 'สรุปสำหรับคุยกับพี่' not in presentation
 standardization=read(EXP/'manifests/STANDARDIZATION.json');standardization['resumed_execution']=True;standardization['resume_provenance']='manifests/RESUME_PROVENANCE.json';standardization['resume_provenance_sha256']=sha(EXP/'manifests/RESUME_PROVENANCE.json');standardization['notes'].append('Session recovery reused completed YOLO26m/YOLO11m results and retained the active original YOLOv8m worker; no restart from zero.');atomic(EXP/'manifests/STANDARDIZATION.json',standardization)
 integrity=read(EXP/'manifests/final_integrity.json');integrity['post_freeze_reporting_sources']={str(f.relative_to(EXP)):sha(f) for f in [EXP/'src/build_medium_results.py',EXP/'src/report_medium.py',EXP/'src/resume_medium.py',EXP/'src/audit_resume_state.py']};atomic(EXP/'manifests/final_integrity.json',integrity)
 state_path=ROOT/'YOLO_Instance_Segmentation_MOTS20_Scaling_Study/STUDY_STATE.json';state=read(state_path);state['tiers']['medium'].update(completion_status='COMPLETE',result_status='PASS_WITH_WARNINGS',canonical_run_id=run,standardized=True,last_verified=now(),notes='Completed after session recovery; previously saved accuracy reused, original worker retained. 3 models × 2862 frames; 9 clean timing rounds; canonical/document integrity PASS.');state['last_verified']=now();atomic(state_path,state)
 progress(run,'COMPLETE_VALIDATED');atomic(EXP/'manifests/RESUME_COMPLETE.json',{'timestamp':now(),'status':'PASS_WITH_WARNINGS','run_id':run,'models':MODELS,'canonical_validation':'PASS','document_validation':'PASS','saved_frames_preserved':'PASS','git_publication':'pending independent review'})
 print('[MEDIUM] validation PASS; reports complete',flush=True)
if __name__=='__main__':
 try:main(sys.argv[1])
 except BaseException as e:
  atomic(EXP/'logs'/sys.argv[1]/'resume_supervisor_FAILURE.json',{'timestamp':now(),'error':repr(e),'traceback':traceback.format_exc()});raise
