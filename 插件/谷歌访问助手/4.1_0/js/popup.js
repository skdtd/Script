$(document).ready(function(){var e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",r=null;if(void 0!==window.localStorage.p__conflict&&(r=JSON.parse(function(r){var t,n,o,c,i,a,s="",h=0;if(void 0!==r&&null!==r){for(r=r.replace(/[^A-Za-z0-9\+\/\=]/g,"");h<r.length;)t=e.indexOf(r.charAt(h++))<<2|(c=e.indexOf(r.charAt(h++)))>>4,n=(15&c)<<4|(i=e.indexOf(r.charAt(h++)))>>2,o=(3&i)<<6|(a=e.indexOf(r.charAt(h++))),s+=String.fromCharCode(t),64!=i&&(s+=String.fromCharCode(n)),64!=a&&(s+=String.fromCharCode(o));s=function(e){var r,t,n,o,c,i;for(r="",n=e.length,t=0;t<n;)switch((o=e.charCodeAt(t++))>>4){case 0:case 1:case 2:case 3:case 4:case 5:case 6:case 7:r+=e.charAt(t-1);break;case 12:case 13:c=e.charCodeAt(t++),r+=String.fromCharCode((31&o)<<6|63&c);break;case 14:c=e.charCodeAt(t++),i=e.charCodeAt(t++),r+=String.fromCharCode((15&o)<<12|(63&c)<<6|(63&i)<<0)}return r}(s)}return s}(window.localStorage.p__conflict))),r){if($("#pop_content").hide(),$("#pop_conflict").show(),r&&r.length>0){var t="";for(var n in r)t+='<li id="'+r[n].id+'" class="list-group-item"><img src="'+r[n].icons[0].url+'" width="16"> '+r[n].name+"</li>";$("#pop_conflict #header ul").html(t)}$("#openExtensions").click(function(){chrome.tabs.create({url:"chrome://extensions/"})}),$("#disableExtensions").click(function(){for(var e in r)chrome.management.setEnabled(r[e].id,!1,function(){});window.location.reload()})}else $("#pop_content").show(),$("#pop_conflict").hide(),$("#banben").text(chrome.runtime.getManifest().version),$("#refresh").click(function(){$("#status").css("display",""),$("#refresh").css("color","gray"),$("#refresh span").css("color","gray"),$("#refresh").css("pointer-events","none"),setTimeout(function(){chrome.tabs.create({url:"http://www.iwikimedia.com/ppgg/serverreport.html"})},500)}),chrome.proxy.settings.get({incognito:!1},function(e){for(var r=JSON.stringify(e).match(/https.+\d;/)[0].split(/\.|:/),t="",n=0;n<r.length;n++){var o=r[n].length-1;r[n].length-2>=0&&(o=r[n].length-2),t+=r[n].charAt(o)}$("#servername").text(t)})});