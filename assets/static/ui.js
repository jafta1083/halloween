(function(){
  // ui.js: lightweight UI behavior for Halloween Quiz (Flask template)
  const cfg = window.GAME_CONFIG || {};
  const getAudio = (id)=>document.getElementById(id);
  const muteKey = 'halloween_mute_v1';

  function isMuted(){
    try { return localStorage.getItem(muteKey) === '1'; } catch(e){ return false }
  }
  function setMuted(v){ try{ localStorage.setItem(muteKey, v? '1':'0'); }catch(e){} }

  // Insert a mute toggle button
  function makeToggle(){
    if(document.getElementById('sound-toggle')) return;
    const btn = document.createElement('button');
    btn.id = 'sound-toggle';
    btn.className = 'sound-toggle';
    btn.innerText = isMuted() ? '🔈' : '🔊';
    btn.onclick = ()=>{ const m = !isMuted(); setMuted(m); btn.innerText = m ? '🔈' : '🔊'; applyMute(); };
    document.body.appendChild(btn);
  }

  function applyMute(){
    const muted = isMuted();
    ['audio-start','audio-background','audio-congrats','audio-correct','audio-incorrect'].forEach(id=>{
      const a = getAudio(id);
      if(!a) return;
      try{ a.muted = muted; }catch(e){}
    });
  }

  function playIf(id){
    const a = getAudio(id);
    if(!a) return;
    try{ a.currentTime = 0; a.play().catch(()=>{}); }catch(e){}
  }

  // confetti: tiny implementation
  function fireConfetti(){
    try{
      if(window.__confettiActive) return;
      const c = document.createElement('canvas');
      c.id = 'confetti-canvas';
      document.body.appendChild(c);
      c.width = window.innerWidth; c.height = window.innerHeight;
      const ctx = c.getContext('2d');
      const pieces = [];
      const colors = ['#ff6b00','#ffdd66','#8b5cff','#6bffb3','#ff6bb5'];
      for(let i=0;i<80;i++){
        pieces.push({x:Math.random()*c.width,y:Math.random()*c.height*0.2, vx:(Math.random()-0.5)*6, vy:2+Math.random()*6, r:2+Math.random()*6, c: colors[Math.floor(Math.random()*colors.length)], rot:Math.random()*360});
      }
      let t=0; window.__confettiActive = true;
      function step(){
        ctx.clearRect(0,0,c.width,c.height);
        t+=1;
        for(let p of pieces){
          p.x+=p.vx; p.y+=p.vy; p.vy+=0.05; p.rot+=p.vx*0.5;
          ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot*Math.PI/180);
          ctx.fillStyle=p.c; ctx.fillRect(-p.r, -p.r*0.6, p.r*2, p.r*1.2);
          ctx.restore();
        }
        if(t<360){ requestAnimationFrame(step); } else { document.body.removeChild(c); window.__confettiActive=false; }
      }
      requestAnimationFrame(step);
    }catch(e){console.error(e)}
  }

  // Apply initial mute state
  makeToggle(); applyMute();

  // Handle start/background/congrats/feedback
  if(cfg.play_start){ playIf('audio-start'); }
  if(cfg.play_background){ const b = getAudio('audio-background'); if(b) try{ b.play().catch(()=>{}); }catch(e){} }
  if(cfg.feedback === 'correct'){ playIf('audio-correct'); }
  if(cfg.feedback === 'incorrect'){ playIf('audio-incorrect'); }
  if(cfg.play_congrats){ playIf('audio-congrats'); /* stop background */ const b=getAudio('audio-background'); if(b){ try{ b.pause(); b.currentTime=0; }catch(e){} } fireConfetti(); }

  // Countdown timer behavior (moved here from template)
  (function(){
    try{
      const timerEl = document.getElementById('timer');
      const progressEl = document.getElementById('timer-progress');
      const announcer = document.getElementById('timer-announcer');
      const initial = (window.GAME_CONFIG && typeof window.GAME_CONFIG.timer !== 'undefined') ? Number(window.GAME_CONFIG.timer) : null;
      if(timerEl && Number.isFinite(initial)){
        let timeLeft = initial;
        // initialize UI
        timerEl.textContent = timeLeft;
        if(progressEl){ progressEl.style.width = '100%'; }

        // announce initial time for assistive tech
        if(announcer){ announcer.textContent = `Time remaining: ${timeLeft} seconds`; }

        let lastAnnounce = Date.now();
        const iv = setInterval(()=>{
          timeLeft -= 1;
          if(timeLeft < 0) timeLeft = 0;
          timerEl.textContent = timeLeft;

          // update progress bar (percentage)
          if(progressEl){
            const pct = Math.max(0, Math.min(100, Math.round((timeLeft / initial) * 100)));
            progressEl.style.width = pct + '%';
          }

          // announce periodically: every 5s, and every second during last 5s
          const now = Date.now();
          const shouldAnnounce = (timeLeft <= 5) || (now - lastAnnounce > 4800);
          if(shouldAnnounce && announcer){ announcer.textContent = `Time remaining: ${timeLeft} seconds`; lastAnnounce = now; }

          if(timeLeft <= 0){
            clearInterval(iv);
            try{ if(document.forms && document.forms[0]) document.forms[0].submit(); }catch(e){}
          }
        }, 1000);
      }
    }catch(e){ console.error('timer error', e); }
  })();

  // When the page is interacted with (click), allow audio autoplay attempts again
  document.addEventListener('click', function once(){ applyMute(); document.removeEventListener('click', once); }, {once:true});
})();
