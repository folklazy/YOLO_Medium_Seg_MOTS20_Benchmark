"""Medium-only phase gates; never launches another tier or downloads weights."""
from pathlib import Path
import sys,subprocess,json,shutil,gzip,math,traceback
from validate import ROOT,EXP,MODELS,sha,write,now

def read(p):return json.loads(p.read_text())
def main(run):
 assert MODELS==['yolo26m-seg.pt','yolo11m-seg.pt','yolov8m-seg.pt']
 env=read(EXP/'manifests/environment.json');assert env['cuda_available']
 assert not read(EXP/'manifests/environment_comparison.json')['differences']
 reference=ROOT/'YOLO_Large_Seg_MOTS20_Benchmark'
 import ultralytics
 package=Path(ultralytics.__file__).parent
 framework=read(reference/'manifests/framework_source_hashes.json')
 assert all(sha(package/f)==h for f,h in framework.items()),'Framework drift'
 write(EXP/'manifests/framework_source_hashes.json',framework)
 audit={'status':'PASS','timestamp':now(),'dataset_compatibility':'PASS','environment_compatibility':'PASS','framework_compatibility':'PASS','reference_repository':reference.name,'same_frame_order_hashes_dimensions_gt_metadata':True,'reference_hashes':{str(f.relative_to(reference)):sha(f) for f in [reference/'manifests'/x for x in ['images.json','dataset_manifest.json','preflight_frames.json','timing_frames.json','visualization_frames.json','framework_source_hashes.json']]}}
 for n in ['images.json','preflight_frames.json','timing_frames.json','visualization_frames.json']:assert sha(reference/'manifests'/n)==sha(EXP/'manifests'/n)
 write(EXP/'manifests/shared_input_audit.json',audit)
 # Freeze preflight inputs without mutating shared resources.
 archive=EXP/'reports'/run/'preflight_inputs';archive.mkdir(parents=True,exist_ok=False)
 for path in [EXP/'EXPERIMENT_PROTOCOL.md',EXP/'configs/benchmark.yaml',*list((EXP/'src').rglob('*.py')),*list((EXP/'manifests').glob('*.json'))]:
  dst=archive/path.relative_to(EXP);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dst)
 def phase(script,*args):
  log=EXP/'logs'/run/(script.replace('.py','')+'-'+(args[0] if len(args)>1 else 'timing')+'.log')
  with log.open('w') as out:subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(EXP/'src'/script),*args],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT,check=True)
 phase('benchmark.py','preflight',run)
 decision=read(EXP/'manifests'/f'{run}_preflight.json');assert decision['status']=='PASS' and decision['selected_max_dets']==200
 # Validate saved preflight output before authorizing full inference; no extra inference.
 sample=read(EXP/'manifests/preflight_frames.json');checks=[]
 for cp in MODELS:
  base=EXP/'predictions'/run/'preflight'/cp.removesuffix('.pt');m=read(base/'metadata.json')
  assert m['status']=='PASS' and m['images_successful']==100 and m['images_failed']==0
  assert m['end2end'] is False and m['precision']=='fp32'
  count=0
  for f in sample:
   with gzip.open(base/'predictions'/f"{f['sequence']}_{f['frame']:06d}.json.gz",'rt') as stream:r=json.load(stream)
   assert r['input_shape']==[1,3,640,640] and r['post_nms_candidates']<1000
   for pred in r['predictions']:
    assert pred['class']==0 and math.isfinite(pred['confidence']) and all(math.isfinite(x) for x in pred['bbox_xyxy'])
    assert pred['rle']['size']==[r['height'],r['width']]
   count+=1
  checks.append({'model':cp,'frames':count,'finite_output':True,'native_masks':True,'status':'PASS'})
 write(EXP/'manifests'/f'{run}_preflight_output_checks.json',{'status':'PASS','checks':checks})
 print('PREFLIGHT + saved-output gates PASS: 3 models; AP maxDet 200. Starting full accuracy.',flush=True)
 phase('benchmark.py','full',run)
 print('FULL ACCURACY finished. Starting idle-gated timing.',flush=True)
 phase('repeat_clean_timing.py',run)
 import csv
 timing=list(csv.DictReader((EXP/'timing'/run/'clean_repetition/summary.csv').open()))
 assert len(timing)==3 and all(r['clean_rounds']=='3' and r['frames']=='300' for r in timing),'Incomplete clean timing: preserved records, stop for recovery'
 print('MEDIUM measurement phases complete; canonical reporting/consistency checks still required.',flush=True)
if __name__=='__main__':
 try:main(sys.argv[1])
 except BaseException as e:
  write(EXP/'logs'/sys.argv[1]/'orchestration_FAILURE.json',{'timestamp':now(),'error':repr(e),'traceback':traceback.format_exc()});raise
