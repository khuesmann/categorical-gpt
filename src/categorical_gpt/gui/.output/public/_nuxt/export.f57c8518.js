import p from"./Icon.fdb3aa7f.js";import{d as l,c as f,k as d,l as _,m as t,t as m,B as n,q as a,o as v}from"./entry.a72026d0.js";import{a as x,u as b}from"./wizzard.fa111ad8.js";import"./config.f6aefa06.js";const h={class:"textarea w-full h-64",disabled:""},j={class:"text-right"},g=l({__name:"ClipboardTextarea",props:{text:{type:String,default:""},json:{type:Object,default:null}},setup(i){const o=i,s=f(()=>o.json?JSON.stringify(o.json):o.text),c=r=>{navigator.clipboard.writeText(r)};return(r,e)=>{const u=p;return d(),_("div",null,[t("textarea",h,m(n(s)),1),t("div",j,[t("a",{class:"btn btn-xs",onClick:e[0]||(e[0]=O=>c(n(s)))},[a(u,{name:"ic:outline-content-copy"})])])])}}}),S={class:"flex gap-4"},y={class:"flex-1"},z=t("div",{class:"font-bold mb-2"},"Feature vectors",-1),C=t("div",{class:"font-bold mb-2"},"Feature dictionary",-1),k=t("div",{class:"divider divider-horizontal"},null,-1),B={class:"flex-1"},T=t("div",{class:"font-bold mb-2"},"Color-coding",-1),$=t("div",{class:"divider divider-horizontal"},null,-1),w={class:"flex-1"},N=t("div",{class:"font-bold mb-2"},"Ordering",-1),E=l({__name:"export",setup(i){const o=x(),s=b();return v(()=>{o.hasStepLoaded[o.steps[4].number]||o.loadStep(o.steps[4])}),(c,r)=>{const e=g;return d(),_("div",S,[t("div",y,[z,a(e,{json:n(s).results.feature_vectors},null,8,["json"]),C,a(e,{json:n(s).results.feature_vectors_dict},null,8,["json"])]),k,t("div",B,[T,a(e,{json:n(s).results.color_coding},null,8,["json"])]),$,t("div",w,[N,a(e,{json:n(s).results.ordering},null,8,["json"])])])}}});export{E as default};