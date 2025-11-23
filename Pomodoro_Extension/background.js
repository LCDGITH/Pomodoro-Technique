
    const SERVER='http://127.0.0.1:5000/update_url';
    async function s(){try{const t=await chrome.tabs.query({active:true,currentWindow:true});
    if(t&&t[0]&&t[0].url&&!t[0].url.startsWith('chrome')&&!t[0].url.startsWith('edge')){
    await fetch(SERVER,{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({url:t[0].url,title:t[0].title})});}}catch(e){}}
    chrome.tabs.onActivated.addListener(s);chrome.tabs.onUpdated.addListener((i,c,t)=>{if(c.status==='complete')s()});
    setInterval(s,3000);
    