/* Fynzo advanced calculator features: comparisons, charts, schedules, favorites and exports. */
(function(){"use strict";
var MONEY=new Intl.NumberFormat("en-US",{style:"currency",currency:"USD",maximumFractionDigits:2});
function num(v){v=parseFloat(v);return Number.isFinite(v)?v:0;}
function inputs(){var out={};document.querySelectorAll("#fx [data-k]").forEach(function(el){out[el.dataset.k]=num(el.value);});return out;}
function page(){return location.pathname.split("/").pop()||"index.html";}
function title(){var h=document.querySelector("h1");return h?h.textContent.trim():page();}
function resultText(){var r=document.getElementById("res");return r?r.innerText.trim():"";}
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];});}
function calculation(file,v){var r,n,pay,total,principal,interest,future,contrib,tax,net,profit,roi;
 if(file==="mortgage-calculator.html"){principal=Math.max(v.price-v.down,0);r=v.rate/1200;n=v.term*12;pay=r?principal*r/(1-Math.pow(1+r,-n)):principal/n;total=pay*n;return{headline:pay,headlineLabel:"Monthly payment",parts:[["Principal",principal],["Interest",total-principal]],total:total};}
 if(file==="loan-calculator.html"){principal=v.amount;r=v.rate/1200;n=v.months;pay=r?principal*r/(1-Math.pow(1+r,-n)):principal/n;total=pay*n;return{headline:pay,headlineLabel:"Monthly payment",parts:[["Principal",principal],["Interest",total-principal]],total:total};}
 if(file==="compound-interest-calculator.html"){r=v.rate/1200;n=v.years*12;future=v.principal*Math.pow(1+r,n)+(r?v.monthly*(Math.pow(1+r,n)-1)/r:v.monthly*n);contrib=v.principal+v.monthly*n;return{headline:future,headlineLabel:"Future value",parts:[["Contributions",contrib],["Growth",Math.max(future-contrib,0)]],total:future};}
 if(file==="savings-goal-calculator.html"){r=v.rate/1200;n=v.months;var gap=Math.max(v.goal-v.have*Math.pow(1+r,n),0);pay=r?gap*r/(Math.pow(1+r,n)-1):gap/n;return{headline:pay,headlineLabel:"Monthly saving",parts:[["Already saved",v.have],["Still to build",Math.max(v.goal-v.have,0)]],total:v.goal};}
 if(file==="income-tax-calculator.html"){tax=v.income*v.rate/100;net=v.income-tax;return{headline:net,headlineLabel:"Net annual income",parts:[["Net income",net],["Estimated tax",tax]],total:v.income};}
 if(file==="roi-calculator.html"){profit=v.final-v.invest;roi=v.invest?profit/v.invest*100:0;return{headline:roi,headlineLabel:"ROI percentage",parts:[["Invested",v.invest],["Profit or loss",profit]],total:Math.max(v.final,v.invest)};}
 if(file==="hourly-to-salary-calculator.html"){total=v.hourly*v.hours*52;return{headline:total,headlineLabel:"Annual salary",parts:[["Monthly",total/12],["Weekly",v.hourly*v.hours]],total:total};}
 return null;}
function schedule(file,v){var principal,r,n;if(file==="mortgage-calculator.html"){principal=Math.max(v.price-v.down,0);r=v.rate/1200;n=Math.max(1,Math.round(v.term*12));}else if(file==="loan-calculator.html"){principal=v.amount;r=v.rate/1200;n=Math.max(1,Math.round(v.months));}else return[];
 var payment=r?principal*r/(1-Math.pow(1+r,-n)):principal/n,balance=principal,rows=[],yp=0,yi=0,year=1;
 for(var m=1;m<=n;m++){var i=balance*r,pr=Math.min(payment-i,balance);if(!r)pr=Math.min(payment,balance);balance=Math.max(balance-pr,0);yp+=pr;yi+=i;if(m%12===0||m===n){rows.push({year:year++,principal:yp,interest:yi,balance:balance});yp=0;yi=0;}}
 return rows;}
function drawChart(){var container=document.querySelector(".result-chart");if(!container)return;var calc=calculation(page(),inputs());if(!calc){var rows=[].slice.call(document.querySelectorAll("#res .rrow")).slice(0,3);container.innerHTML=rows.map(function(row,i){return'<div class="chart-row"><span>'+esc(row.children[0].textContent)+'</span><i style="width:'+Math.max(20,100-i*22)+'%"></i><b>'+esc(row.children[1].textContent)+'</b></div>';}).join("");return;}
 var vals=calc.parts.map(function(x){return Math.abs(x[1]);}),max=Math.max.apply(Math,vals.concat([1]));container.innerHTML=calc.parts.map(function(x,i){var color=i%2?"var(--gold)":"var(--green)";return'<div class="chart-row"><span>'+esc(x[0])+'</span><i style="width:'+Math.max(3,Math.abs(x[1])/max*100)+'%;background:'+color+'"></i><b>'+MONEY.format(x[1])+'</b></div>';}).join("");}
function setupObserver(){var r=document.getElementById("res");if(!r)return;new MutationObserver(function(){drawChart();refreshAdvanced();}).observe(r,{childList:true,subtree:true,characterData:true});drawChart();}
var scenarios={};
function scenarioHtml(letter,data){if(!data)return"<strong>Scenario "+letter+"</strong><p>Not saved yet.</p>";var fields=Object.keys(data.values).map(function(k){return'<span>'+esc(k)+': '+esc(data.values[k])+'</span>';}).join("");return'<strong>Scenario '+letter+'</strong><em>'+esc(data.calc.headlineLabel)+': '+(page()==="roi-calculator.html"?data.calc.headline.toFixed(2)+"%":MONEY.format(data.calc.headline))+'</em><div>'+fields+'</div>';}
function setupCompare(){document.querySelectorAll("[data-save-scenario]").forEach(function(btn){btn.addEventListener("click",function(){var letter=btn.dataset.saveScenario,v=inputs(),calc=calculation(page(),v);if(!calc)return;scenarios[letter]={values:v,calc:calc};var panel=document.querySelector('[data-scenario-panel="'+letter+'"]');panel.innerHTML=scenarioHtml(letter,scenarios[letter]);var out=document.querySelector(".scenario-comparison");if(scenarios.A&&scenarios.B){var d=scenarios.B.calc.headline-scenarios.A.calc.headline;out.textContent="Scenario B is "+(d>=0?"higher":"lower")+" by "+(page()==="roi-calculator.html"?Math.abs(d).toFixed(2)+" percentage points":MONEY.format(Math.abs(d)))+".";}});});}
function fillSchedule(){var rows=schedule(page(),inputs()),body=document.querySelector(".amort-table tbody");if(!body)return;body.innerHTML=rows.map(function(x){return"<tr><td>"+x.year+"</td><td>"+MONEY.format(x.principal)+"</td><td>"+MONEY.format(x.interest)+"</td><td>"+MONEY.format(x.balance)+"</td></tr>";}).join("");}
function setupSchedule(){var btn=document.querySelector(".toggle-schedule"),wrap=document.querySelector(".amort-wrap");if(!btn||!wrap)return;btn.addEventListener("click",function(){wrap.hidden=!wrap.hidden;btn.textContent=wrap.hidden?"Show schedule":"Hide schedule";if(!wrap.hidden)fillSchedule();});}
function refreshAdvanced(){if(document.querySelector(".amort-wrap:not([hidden])"))fillSchedule();}
function csvCell(v){return'"'+String(v).replace(/"/g,'""')+'"';}
function setupExport(){var btn=document.querySelector(".export-csv");if(!btn)return;btn.addEventListener("click",function(){var lines=[["Fynzo calculation",title()],["Page",location.href.split("?")[0]],["Exported",new Date().toISOString()],["Inputs",""]];var v=inputs();Object.keys(v).forEach(function(k){lines.push([k,v[k]]);});lines.push(["Result",resultText()]);var rows=schedule(page(),v);if(rows.length){lines.push([],['Amortization schedule'],['Year','Principal','Interest','Balance']);rows.forEach(function(x){lines.push([x.year,x.principal.toFixed(2),x.interest.toFixed(2),x.balance.toFixed(2)]);});}var csv=lines.map(function(r){return r.map(csvCell).join(",");}).join("\r\n");var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));a.download=page().replace(".html","")+"-result.csv";a.click();setTimeout(function(){URL.revokeObjectURL(a.href);},1000);});}
function getList(key){try{return JSON.parse(localStorage.getItem(key)||"[]");}catch(e){return[];}}
function setList(key,value){localStorage.setItem(key,JSON.stringify(value));}
function addRecent(){if(!document.querySelector("#fx"))return;var item={title:title(),url:page()},list=getList("fynzo-recent").filter(function(x){return x.url!==item.url;});list.unshift(item);setList("fynzo-recent",list.slice(0,5));}
function setupFavorite(){var btn=document.querySelector(".favorite-tool-btn");if(!btn)return;var item={title:btn.dataset.title,url:btn.dataset.url};function render(){var saved=getList("fynzo-favorites"),on=saved.some(function(x){return x.url===item.url;});btn.textContent=on?"★ Saved":"☆ Save this calculator";btn.setAttribute("aria-pressed",on?"true":"false");}btn.addEventListener("click",function(){var saved=getList("fynzo-favorites"),i=saved.findIndex(function(x){return x.url===item.url;});if(i>=0)saved.splice(i,1);else saved.unshift(item);setList("fynzo-favorites",saved.slice(0,12));render();});render();}
function renderList(id,list){var box=document.getElementById(id);if(!box)return;box.innerHTML=list.length?list.map(function(x){return'<a href="'+x.url+'"><strong>'+esc(x.title)+'</strong><span>Open calculator</span></a>';}).join(""):'<span class="empty-state">Nothing here yet.</span>';}
function setupPersonal(){var favorites=getList("fynzo-favorites"),recent=getList("fynzo-recent"),section=document.getElementById("personal-tools");renderList("favoriteTools",favorites);renderList("recentTools",recent);if(section)section.classList.toggle("is-empty",favorites.length===0&&recent.length===0);var clear=document.getElementById("clearRecent");if(clear)clear.addEventListener("click",function(){localStorage.removeItem("fynzo-recent");renderList("recentTools",[]);if(section)section.classList.toggle("is-empty",getList("fynzo-favorites").length===0);});}
document.addEventListener("DOMContentLoaded",function(){addRecent();setupFavorite();setupPersonal();setupObserver();setupCompare();setupSchedule();setupExport();document.querySelectorAll("#fx [data-k]").forEach(function(el){el.addEventListener("input",function(){drawChart();refreshAdvanced();});});});
})();

/* Focused mortgage/loan comparisons and personalized next steps. */
(function(){"use strict";
function field(key){return document.querySelector('#fx [data-k="'+key+'"]');}
function trigger(el){if(!el)return;el.dispatchEvent(new Event("input",{bubbles:true}));}
function currentFile(){return location.pathname.split("/").pop()||"index.html";}
function setupQuickCompare(){
  document.querySelectorAll(".quick-compare-actions button").forEach(function(btn){
    btn.addEventListener("click",function(){
      var file=currentFile(),action=btn.getAttribute("data-quick"),rate=field("rate"),term=file==="mortgage-calculator.html"?field("term"):field("months");
      if(action==="rate-down"&&rate) rate.value=Math.max(0,(parseFloat(rate.value)||0)-0.5).toFixed(2);
      if(action==="rate-up"&&rate) rate.value=((parseFloat(rate.value)||0)+0.5).toFixed(2);
      if(action==="term-short"&&term){var step=file==="mortgage-calculator.html"?5:12;term.value=Math.max(step,(parseFloat(term.value)||step)-step);}
      if(action==="term-long"&&term){var add=file==="mortgage-calculator.html"?5:12;term.value=(parseFloat(term.value)||0)+add;}
      trigger(rate);trigger(term);
      var saveB=document.querySelector('[data-save-scenario="B"]');
      if(saveB) window.setTimeout(function(){saveB.click();},30);
    });
  });
}
function personalizeNextSteps(){
  var box=document.querySelector('[data-smart-next="true"]');
  if(!box)return;
  var file=currentFile(),result=document.querySelector("#res .rbig"),value=result?result.textContent.trim():"this result";
  box.querySelectorAll("a[data-reason]").forEach(function(link){
    var reason=link.getAttribute("data-reason");
    link.setAttribute("title",reason);
    if(!link.querySelector("small")){var small=document.createElement("small");small.textContent=reason;link.appendChild(small);}
  });
  box.setAttribute("aria-label","Recommended next tools based on "+value+" from "+file);
}
document.addEventListener("DOMContentLoaded",function(){setupQuickCompare();personalizeNextSteps();var result=document.getElementById("res");if(result)new MutationObserver(personalizeNextSteps).observe(result,{childList:true,subtree:true,characterData:true});});
})();
