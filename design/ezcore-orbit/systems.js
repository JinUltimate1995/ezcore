// Core management is a local UI simulation, never a native package operation.
let coreScope='all', visibleCores=[], previewCores=cores.filter(c=>c.id!=='scummvm').map(c=>c.id);
try {const saved=JSON.parse(localStorage.getItem('ezcore-preview-cores'));if(Array.isArray(saved))previewCores=saved.filter(id=>cores.some(c=>c.id===id));}catch(e){}
function coreEnabled(id){return previewCores.includes(id)}
function persistCores(){try{localStorage.setItem('ezcore-preview-cores',JSON.stringify(previewCores))}catch(e){toast('This browser cannot save preview preferences.')}}
function selectCore(id){state.core=id;renderCoreDock();positionCoreCards()}
function renderSystems(){
 visibleCores=cores.filter(c=>coreScope==='all'||(coreScope==='added'?coreEnabled(c.id):!coreEnabled(c.id)));
 if(!visibleCores.some(c=>c.id===state.core)&&visibleCores.length)state.core=visibleCores[0].id;
 $('#core-summary').textContent=`${previewCores.length} added · ${cores.length-previewCores.length} available`;
 document.querySelectorAll('[data-core-scope]').forEach(b=>{b.classList.toggle('active',b.dataset.coreScope===coreScope);b.setAttribute('aria-pressed',b.dataset.coreScope===coreScope);b.onclick=()=>{coreScope=b.dataset.coreScope;renderSystems()}});
 $('#core-flow-inner').innerHTML=visibleCores.map((c,i)=>`<button class="core-card" data-core="${c.id}" aria-label="${c.name}, ${c.id}" aria-pressed="false"><div class="core-card-top"><span>${c.short}</span><span class="core-state ${coreEnabled(c.id)?'added':''}">${coreEnabled(c.id)?'ADDED':'AVAILABLE'}</span></div><div class="hardware-stage">${hardwareArt(c.id)}</div><div class="core-card-caption"><strong>${c.name}</strong><span>${c.id}</span></div></button>`).join('');
 document.querySelectorAll('.core-card').forEach(b=>b.onclick=()=>selectCore(b.dataset.core));
 $('#core-browser').hidden=!visibleCores.length;$('#cores-empty').hidden=!!visibleCores.length;
 $('#system-feature').hidden=!visibleCores.length;
 renderCoreDock();positionCoreCards();
}
function positionCoreCards(){
 const stage=$('#core-flow');if(!stage||state.page!=='systems')return;
 const w=stage.clientWidth,index=visibleCores.findIndex(c=>c.id===state.core);
 const card=stage.querySelector('.core-card');if(!card)return;
 const step=Math.min(card.offsetWidth*.91,w*.43);
 stage.querySelectorAll('.core-card').forEach((e,i)=>{const d=i-index,a=Math.abs(d);e.style.transform=`translate(-50%,-50%) translateX(${d*step}px) translateZ(${a? -80-(a-1)*50:10}px) rotateY(${d===0?0:d>0?-24:24}deg)`;e.style.opacity=a>3?'0':a===0?'1':String(Math.max(.2,.68-a*.13));e.style.zIndex=20-a;e.style.pointerEvents=a>3?'none':'auto';e.tabIndex=a>3?-1:0;e.classList.toggle('selected',!d);e.setAttribute('aria-pressed',String(!d))});
 $('#core-position').textContent=`${String(index+1).padStart(2,'0')} / ${String(visibleCores.length).padStart(2,'0')}`;
 $('#core-prev').disabled=index<=0;$('#core-next').disabled=index>=visibleCores.length-1;
}
function renderCoreDock(){
 const c=visibleCores.find(c=>c.id===state.core);if(!c)return;
 const added=coreEnabled(c.id),count=games.filter(g=>g.core===c.id).length;
 $('#system-feature').innerHTML=`<div class="core-dock-copy"><div class="core-dock-meta"><span>${c.id}</span><span>${c.type} · ${c.era}</span></div><h2>${c.name}</h2><p>${c.about.split('. ')[0]}. <span>${count} sample ${count===1?'game':'games'}</span></p></div><div class="core-dock-actions"><button class="primary" id="browse-core" ${added?'':'disabled'}>${icon('library')} Browse games</button><button class="secondary ${added?'remove-core':''}" id="core-toggle">${icon(added?'close':'plus')}${added?'Remove core':'Add core'}</button></div><p class="core-preview-note">${icon('info')}Preview only · Core changes stay in this browser. Games & saves are kept.</p>`;
 $('#browse-core').onclick=()=>{state.query='';$('#search').value='';setFilter('core:'+c.id)};
 $('#core-toggle').onclick=()=>added?confirmRemoveCore(c):addPreviewCore(c);
}
function addPreviewCore(c){if(!coreEnabled(c.id))previewCores.push(c.id);persistCores();renderSystems();toast(`${c.id} added to preview — no package downloaded`)}
function confirmRemoveCore(c){
 openOverlay(`<section class="dialog core-confirm" role="dialog" aria-modal="true" aria-labelledby="remove-core-title"><button class="close" aria-label="Close remove core confirmation">${icon('close')}</button><p class="eyebrow">CORE MANAGEMENT / PREVIEW</p><h2 id="remove-core-title">Remove ${c.id}?</h2><p>This removes ${c.name} from your added-core preview. Your games and saves stay untouched. You can add this core again at any time.</p><div class="core-confirm-actions"><button class="secondary" id="cancel-remove-core">Keep core</button><button class="primary" id="confirm-remove-core">Remove core</button></div></section>`);
 $('#cancel-remove-core').onclick=closeOverlay;
 $('#confirm-remove-core').onclick=()=>{previewCores=previewCores.filter(id=>id!==c.id);persistCores();closeOverlay();renderSystems();$('#core-toggle')?.focus();toast(`${c.id} removed from preview · games & saves kept`)};
}
function moveCore(n){if(state.page!=='systems'||!visibleCores.length)return;const i=visibleCores.findIndex(c=>c.id===state.core);selectCore(visibleCores[Math.max(0,Math.min(visibleCores.length-1,i+n))].id)}
icons.plus='<path d="M12 5v14M5 12h14"/>';
$('#core-prev').onclick=()=>moveCore(-1);$('#core-next').onclick=()=>moveCore(1);
let coreStart=null,coreWheelAt=0;
$('#core-flow').addEventListener('pointerdown',e=>{coreStart={x:e.clientX,y:e.clientY}});
$('#core-flow').addEventListener('pointercancel',()=>coreStart=null);
$('#core-flow').addEventListener('pointerup',e=>{if(!coreStart)return;const dx=e.clientX-coreStart.x,dy=e.clientY-coreStart.y;coreStart=null;if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)){moveCore(dx<0?1:-1);$('#core-flow').addEventListener('click',e=>{e.stopPropagation();e.preventDefault()},{capture:true,once:true})}});
$('#core-flow').addEventListener('wheel',e=>{if(Math.abs(e.deltaX)>Math.abs(e.deltaY)&&Math.abs(e.deltaX)>8){e.preventDefault();if(Date.now()-coreWheelAt>220){moveCore(e.deltaX>0?1:-1);coreWheelAt=Date.now()}}},{passive:false});
new ResizeObserver(positionCoreCards).observe($('#core-flow'));
