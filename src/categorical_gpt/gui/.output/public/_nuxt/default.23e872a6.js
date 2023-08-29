import J from"./Icon.569dfb32.js";import{a as k,b as C}from"./wizzard.3c4dee2d.js";import{d as O,a as z,k as d,l as u,F as V,G as H,m as e,B as t,L as M,t as b,v as N,D as y,r as v,c as L,I as h,o as B,z as x,A as f,C as S,q as g,N as D,E as j}from"./entry.193f47eb.js";import"./config.270a4c2e.js";const U={class:"flex items-center"},A={class:"flex items-center"},E={class:"mr-2 text-center h-16 w-28 lg:w-32"},I=["onClick"],R={key:0},W={key:1,class:"loading loading-spinner loading-xs"},F=e("br",null,null,-1),T={key:0},q=["value"],G=e("br",null,null,-1),K=O({__name:"WizzardStepper",setup(P){const r=k();z();const a=n=>r.currentStep.number==n.number;return(n,m)=>(d(),u("div",U,[(d(!0),u(V,null,H(t(r).steps,(o,c)=>(d(),u("div",A,[e("div",E,[e("button",{onClick:s=>t(r).loadStep(o),class:M(["btn btn-circle btn-sm",{"btn-primary":t(r).hasStepLoaded[o.number],"btn-outline":!a(o)}])},[t(r).isStepLoading[o.number]?(d(),u("span",W)):(d(),u("span",R,b(o.number-1),1))],10,I),N(),F,e("span",{class:M(["text-sm",{"font-bold":t(r).currentStep.number==o.number}])},b(o.name),3)]),c<t(r).steps.length-1?(d(),u("div",T,[e("progress",{class:"progress progress-primary w-12 lg:w-16",value:t(r).stepProgress[o.number+1],max:"100"},null,8,q),G,N("   ")])):y("",!0)]))),256))]))}}),Q={class:"modal modal-open"},X={class:"card w-96 bg-base-100 shadow-xl p-4"},Y=e("h3",{class:"font-bold text-3xl mb-4"},"Settings",-1),Z=e("div",{class:"font-bold text-xl"},"Model",-1),ee={class:"text-xs text-error"},te={class:"text-xs text-warning"},se=e("div",{class:"divider divider-vertical"},null,-1),ae=e("div",{class:"font-bold text-xl"},"Model parameters",-1),oe={class:"flex flex-col gap-2"},le={class:"w-full"},re=e("div",{class:"font-bold"},"Characteristic",-1),ne={class:"text-xs text-error"},ie={class:"w-full"},de=e("div",{class:"font-bold"},"Heuristic",-1),ce={class:"text-xs text-error"},ue={class:"w-full"},me=e("div",{class:"font-bold"},"Apply heuristic",-1),_e={class:"text-xs text-error"},pe={class:"flex justify-between mt-4"},ve=["disabled"],be=O({__name:"Settings",emits:["close"],setup(P,{emit:r}){const a=C(),n=v(""),m=v(""),o=v(""),c=v(""),s=v({characteristicModelParameters:"",heuristicModelParameters:"",applyHeuristicModelParameters:"",model:""}),p=v({model:""}),$=L(()=>!Object.values(s.value).every(l=>l===""));h(()=>n.value,l=>{try{s.value.characteristicModelParameters="",JSON.parse(l)}catch{s.value.characteristicModelParameters="No valid JSON"}}),h(()=>m.value,l=>{try{s.value.heuristicModelParameters="",JSON.parse(l)}catch{s.value.heuristicModelParameters="No valid JSON"}}),h(()=>o.value,l=>{try{s.value.applyHeuristicModelParameters="",JSON.parse(l)}catch{s.value.applyHeuristicModelParameters="No valid JSON"}}),h(()=>c.value,l=>{l===""?s.value.model="Model name is empty":a.availableModels.includes(l)?(s.value.model="",p.value.model=""):p.value.model="Make sure that the API maps this model to a driver."});const w=()=>{a.modelParams.characteristic=JSON.parse(n.value),a.modelParams.heuristic=JSON.parse(m.value),a.modelParams.apply_heuristic=JSON.parse(o.value),a.model=c.value,r("close")};return B(()=>{c.value=a.model,n.value=JSON.stringify(a.modelParams.characteristic,null,0),m.value=JSON.stringify(a.modelParams.heuristic,null,0),o.value=JSON.stringify(a.modelParams.apply_heuristic,null,0)}),(l,i)=>(d(),u("div",Q,[e("div",X,[Y,Z,x(e("input",{class:"input input-bordered w-full mb-1",placeholder:"Model name","onUpdate:modelValue":i[0]||(i[0]=_=>S(c)?c.value=_:null)},null,512),[[f,t(c)]]),e("div",ee,b(t(s).model),1),e("div",te,b(t(p).model),1),se,ae,e("div",oe,[e("div",le,[re,x(e("textarea",{class:"textarea textarea-bordered w-full","onUpdate:modelValue":i[1]||(i[1]=_=>S(n)?n.value=_:null)},null,512),[[f,t(n)]]),e("div",ne,b(t(s).characteristicModelParameters),1)]),e("div",ie,[de,x(e("textarea",{class:"textarea textarea-bordered w-full","onUpdate:modelValue":i[2]||(i[2]=_=>S(m)?m.value=_:null)},null,512),[[f,t(m)]]),e("div",ce,b(t(s).heuristicModelParameters),1)]),e("div",ue,[me,x(e("textarea",{class:"textarea textarea-bordered w-full","onUpdate:modelValue":i[3]||(i[3]=_=>S(o)?o.value=_:null)},null,512),[[f,t(o)]]),e("div",_e,b(t(s).applyHeuristicModelParameters),1)])]),e("div",pe,[e("button",{class:"btn",onClick:i[4]||(i[4]=_=>r("close"))},"Close"),e("button",{class:"btn btn-success",onClick:w,disabled:t($)},"Save",8,ve)])])]))}}),he=["data-theme"],xe={class:"flex-grow content-center"},fe={class:"flex justify-between items-center p-4 pb-8 bg-base-100 shadow-md relative"},Se={class:"absolute right-1 top-1"},ge={class:"w-32"},ye=["disabled"],$e={class:"flex-grow"},we={class:"flex justify-center"},Pe={class:"w-32"},Me=["disabled"],Ne={class:"p-4"},ke=e("div",null," © Copyright 2023 ",-1),Ve={__name:"default",setup(P){const r=C(),a=k();z();const n=v(!1),m=()=>a.isLoading||!a.isStepReady(a.currentStep),o=()=>a.isLoading;return(c,s)=>{const p=J,$=K,w=be;return d(),u("div",{class:"flex flex-col min-h-screen bg-base-300","data-theme":t(r).theme},[e("div",xe,[e("div",fe,[e("div",Se,[e("button",{class:"btn btn-xs btn-circle btn-ghost text-lg",onClick:s[0]||(s[0]=l=>n.value=!0)},[g(p,{name:"codicon:settings-gear"})])]),e("div",ge,[t(a).prevStep?(d(),u("button",{key:0,onClick:s[1]||(s[1]=l=>t(a).loadStep(t(a).prevStep)),class:"btn btn-primary",disabled:o()},[g(p,{name:"ic:baseline-arrow-back-ios"})],8,ye)):y("",!0)]),e("div",$e,[e("div",we,[g($)])]),e("div",Pe,[t(a).nextStep?(d(),u("button",{key:0,onClick:s[2]||(s[2]=l=>t(a).loadStep(t(a).nextStep)),disabled:m(),class:"btn btn-primary"},[g(p,{name:"ic:baseline-arrow-forward-ios"})],8,Me)):y("",!0)])]),e("div",Ne,[D(c.$slots,"default")]),t(n)?(d(),j(w,{key:0,onClose:s[3]||(s[3]=l=>n.value=!1)})):y("",!0)]),ke],8,he)}}};export{Ve as default};
