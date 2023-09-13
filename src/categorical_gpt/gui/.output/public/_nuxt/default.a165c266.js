import x from"./Icon.fdb3aa7f.js";import{a as h,b as w}from"./wizzard.fa111ad8.js";import{d as $,a as S,k as r,l as a,F as y,G as k,m as e,B as t,L as p,t as m,v as b,D as _,q as d,N as z}from"./entry.a72026d0.js";import"./config.f6aefa06.js";const C={class:"flex items-center"},L={class:"flex items-center"},N={class:"mr-2 text-center h-16 w-28 lg:w-32"},B=["onClick"],D={key:0},V={key:1,class:"loading loading-spinner loading-xs"},W=e("br",null,null,-1),j={key:0},F=["value"],P=e("br",null,null,-1),R=$({__name:"WizzardStepper",setup(g){const n=h();S();const s=c=>n.currentStep.number==c.number;return(c,u)=>(r(),a("div",C,[(r(!0),a(y,null,k(t(n).steps,(o,i)=>(r(),a("div",L,[e("div",N,[e("button",{onClick:l=>t(n).loadStep(o),class:p(["btn btn-circle btn-sm",{"btn-primary":t(n).hasStepLoaded[o.number],"btn-outline":!s(o)}])},[t(n).isStepLoading[o.number]?(r(),a("span",V)):(r(),a("span",D,m(o.number-1),1))],10,B),b(),W,e("span",{class:p(["text-sm",{"font-bold":t(n).currentStep.number==o.number}])},m(o.name),3)]),i<t(n).steps.length-1?(r(),a("div",j,[e("progress",{class:"progress progress-primary w-12 lg:w-16",value:t(n).stepProgress[o.number+1],max:"100"},null,8,F),P,b("   ")])):_("",!0)]))),256))]))}}),q=["data-theme"],E={class:"flex-grow content-center"},G={class:"flex justify-between items-center p-4 pb-8 bg-base-100 shadow-md relative"},I={class:"w-32"},T=["disabled"],A={class:"flex-grow"},H={class:"flex justify-center"},J={class:"w-32 text-right"},K=["disabled"],M={class:"p-4"},O=e("div",null," © Copyright 2023 ",-1),Z={__name:"default",setup(g){const n=w(),s=h();S();const c=()=>s.isLoading||!s.isStepReady(s.currentStep),u=()=>s.isLoading;return(o,i)=>{const l=x,v=R;return r(),a("div",{class:"flex flex-col min-h-screen bg-base-300","data-theme":t(n).theme},[e("div",E,[e("div",G,[e("div",I,[t(s).prevStep?(r(),a("button",{key:0,onClick:i[0]||(i[0]=f=>t(s).loadStep(t(s).prevStep)),class:"btn btn-primary",disabled:u()},[d(l,{name:"ic:baseline-arrow-back-ios"})],8,T)):_("",!0)]),e("div",A,[e("div",H,[d(v)])]),e("div",J,[t(s).nextStep?(r(),a("button",{key:0,onClick:i[1]||(i[1]=f=>t(s).loadStep(t(s).nextStep)),disabled:c(),class:"btn btn-primary"},[d(l,{name:"ic:baseline-arrow-forward-ios"})],8,K)):_("",!0)])]),e("div",M,[z(o.$slots,"default")])]),O],8,q)}}};export{Z as default};
