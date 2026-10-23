// Reads the typed text out of Anki's comparison block and checks it against accepted answers.
function typedFrom(el){
  if(!el) return null;
  if(el.tagName==='INPUT') return el.value;
  var arrow=el.querySelector('#typearrow');
  if(!arrow) return el.textContent;           // exact match: one line only
  var out='';
  for(var n=el.firstChild;n;n=n.nextSibling){
    if(n.nodeName==='BR') break;                // first line = what the user typed
    if(n.classList && n.classList.contains('typeMissed')) continue;
    out+=n.textContent;
  }
  return out;
}
function norm(s){
  return (s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase()
    .replace(/[’`]/g,"'").replace(/^\s*(?:(?:il|lo|la|i|gli|le|un|uno|una)\s+|(?:l|un|dell|nell|all|sull)'\s*)/,'').replace(/\s+/g,' ').trim();
}
function accepted(typed,main,variants){
  var t=norm(typed); if(!t) return false;
  return [main].concat(variants.split('|')).some(function(a){return norm(a)===t;});
}
module.exports={typedFrom,norm,accepted};
