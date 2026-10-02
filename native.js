(() => {
  const isCard = location.hostname.startsWith('card.') || document.getElementById('card');
  const ios = /iPhone|iPad|iPod/.test(navigator.userAgent) || navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1;
  const standalone = () => matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  let installEvent, subscription, config, busy = false, syncedLang;
  const copy = {
    en: { title:'Want exclusive offers?', install:'Add to Home Screen', offers:'Enable exclusive offer notifications', stop:'Turn off offer notifications', consent:'Optional. Only OFA offers; turn them off here at any time.', ios:'On iPhone: open Share, choose Add to Home Screen, then open the saved app to enable notifications. Save your card link below first so you can restore the same stamps.', manual:'Use your browser menu and choose Install app or Add to Home Screen.', denied:'Notifications are blocked. You can allow them in your browser or device settings.', error:'Could not save your preference. Check your connection and try again.', on:'Offer notifications are on.', off:'Offer notifications are off.', unsupported:'This browser does not support notifications. Try Chrome on Android or the Home Screen app on iPhone (iOS 16.4 or later).', open:'Open your stamp card to enable offers', installing:'Open the saved app from your Home Screen.' },
    ar: { title:'حابب توصلك عروض حصرية', install:'أضف للشاشة الرئيسية', offers:'فعّل إشعارات العروض الحصرية', stop:'أوقف إشعارات العروض', consent:'اختياري. بس عروض ون فور اول؛ بتقدر توقفها من هون بأي وقت.', ios:'على الآيفون: افتح مشاركة، واختار إضافة إلى الشاشة الرئيسية. افتح التطبيق المحفوظ لتفعّل الإشعارات. احفظ رابط بطاقتك أولاً لتقدر ترجع نفس الأختام.', manual:'من قائمة المتصفح اختار تثبيت التطبيق أو إضافة للشاشة الرئيسية.', denied:'الإشعارات محظورة. بتقدر تسمح فيها من إعدادات المتصفح أو التلفون.', error:'ما قدرنا نحفظ اختيارك. تأكد من الإنترنت وجرّب مرة ثانية.', on:'إشعارات العروض مفعّلة.', off:'إشعارات العروض متوقفة.', unsupported:'المتصفح ما بدعم الإشعارات. جرّب كروم على أندرويد أو التطبيق المحفوظ على شاشة الآيفون (iOS 16.4 أو أحدث).', open:'افتح بطاقة الأختام لتفعّل العروض', installing:'افتح التطبيق المحفوظ من الشاشة الرئيسية.' }
  };
  const section = document.createElement('section'); section.className='native-prompt plain';
  const title=document.createElement('h2'), install=document.createElement('button'), offer=document.createElement('button'), note=document.createElement('p'), status=document.createElement('p');
  for (const b of [install,offer]) { b.type='button'; b.className='ghost'; }
  note.className='muted'; status.setAttribute('role','status'); section.append(title,install,offer,note,status);
  (document.querySelector('main') || document.body).append(section);
  const style=document.createElement('style'); style.textContent='.native-prompt{max-width:480px;width:calc(100% - 32px);margin:32px auto;padding-bottom:calc(90px + env(safe-area-inset-bottom));text-align:start}.native-prompt h2{font-size:1.15rem;margin-bottom:12px}.native-prompt button{display:block;min-height:44px;width:100%;margin:10px 0;padding:12px 16px;border:1px solid currentColor;border-radius:12px;background:transparent;color:inherit;font:inherit;cursor:pointer}.native-prompt p{font-size:.9rem;line-height:1.6;margin-top:10px}.native-prompt [hidden]{display:none!important}'; document.head.append(style);
  const say=key=>{status.dataset.message=key;status.textContent=t()[key];};
  const lang=()=>document.documentElement.lang==='ar'?'ar':'en', t=()=>copy[lang()];
  function render() {
    if(status.dataset.message)status.textContent=t()[status.dataset.message];
    title.textContent=t().title; install.textContent=t().install; install.hidden=!!standalone(); offer.textContent=isCard?(subscription?t().stop:t().offers):t().offers;
    offer.hidden=!standalone() || (isCard && !config?.publicKey);
    note.hidden=!standalone();
    note.textContent=t().consent;
    if (subscription && syncedLang!==lang()) sync().catch(()=>{ say('error'); });
  }
  const api=async(path,body)=>{ const r=await fetch('/api/push/'+path,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)}); if(!r.ok) throw new Error('save'); };
  async function sync() { const l=lang(); syncedLang=l; try { await api('subscribe',{subscription:subscription.toJSON(),lang:l,consent:true}); } catch(e) { syncedLang=null; throw e; } }
  install.onclick=async()=>{ if(installEvent){const e=installEvent;installEvent=null;await e.prompt();const choice=await e.userChoice;if(choice.outcome==='accepted')say('installing');}else say(ios?'ios':'manual'); };
  offer.onclick=async()=>{
    if(!standalone())return;
    if (!isCard) { location.href='https://card.oneforalljo.com/?lang='+lang(); return; }
    if(busy)return; busy=true; offer.disabled=true;
    try {
      if(subscription){ await api('unsubscribe',{endpoint:subscription.endpoint}); await subscription.unsubscribe(); subscription=null; say('off'); }
      else if(ios&&!standalone())say('ios');
      else if(!('PushManager' in window)&&!('pushManager' in ServiceWorkerRegistration.prototype))say('unsupported');
      else if(Notification.permission==='denied')say('denied');
      else {
        // Permission must start inside this click, before any network or service-worker wait (Safari).
        const permission=await Notification.requestPermission();
        if(permission!=='granted'){say('denied');return;}
        const reg=await navigator.serviceWorker.ready;
        const key=Uint8Array.from(atob(config.publicKey.replace(/-/g,'+').replace(/_/g,'/')),c=>c.charCodeAt(0));
        subscription=await reg.pushManager.subscribe({userVisibleOnly:true,applicationServerKey:key});
        try { await sync(); } catch(e){ await subscription.unsubscribe();subscription=null;throw e; }
        say('on');
      }
    }catch{say('error');}finally{busy=false;offer.disabled=false;render();}
  };
  window.addEventListener('beforeinstallprompt', e=>{e.preventDefault();installEvent=e;render();});
  window.addEventListener('appinstalled',()=>{install.hidden=true;});
  matchMedia('(display-mode: standalone)').addEventListener('change',render);
  new MutationObserver(render).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  render();
  if('serviceWorker' in navigator){
    const script=document.currentScript;
    const base=new URL('.',script?.src||location.href);
    navigator.serviceWorker.register(new URL('sw.js',base)).then(async reg=>{
      if(!isCard)return;
      config=await fetch('/api/push/config').then(r=>r.json());
      const active=await navigator.serviceWorker.ready;
      if(active.pushManager)subscription=await active.pushManager.getSubscription();
      render();
    }).catch(()=>{if(isCard)say('error');});
  }
})();
